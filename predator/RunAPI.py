from Commons import *
from logger import Logger
from MLController import *
from Statistics import Stats
from DataHolder import Holder
from File_Reader import FileReader
from DataExtractor import Extractor
from DataProcessor import Processor
from DB_Reader import DBReader
from CouchController import CouchAPI

import flask_restful
from flask_cors import CORS, cross_origin
from flask import Flask, request, jsonify
from flask_restful import Api
from werkzeug.utils import secure_filename


logger = Logger()
file_reader = FileReader()
db_reader = DBReader()
extractor = Extractor()
holder = Holder()
stats = Stats()
processor = Processor()
couch = CouchAPI('Administrator', 'password', '0.0.0.0')
couch.open_bucket()

app = Flask(__name__)
api = Api(app)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
CORS(app)


class CustomApi(flask_restful.Api):
    def handle_error(self, e):
        user_exception, log_exception = logger.get_exception()
        logger.log(str(log_exception) + "" + str(user_exception), logger.ERROR)
        flask_restful.abort(str(e))


@app.errorhandler(500)
def internal_server_error(error):
    user_exception, log_exception = logger.get_exception()
    logger.log(str(log_exception) + "" + str(user_exception), logger.ERROR)
    print(user_exception)
    print(log_exception)
    return jsonify({'error': user_exception})


@app.errorhandler(Exception)
def unhandled_exception(e):
    user_exception, log_exception = logger.get_exception()
    logger.log(str(log_exception) + "" + str(user_exception), logger.ERROR)
    print(user_exception)
    print(log_exception)
    return jsonify({'error': user_exception})


@app.route('/auth', methods=['GET', 'POST'])
def auth():
    try:
        logger.log('auth()')
        request_obj = request.get_json(silent=True)
        if 'username' in request_obj and 'password' in request_obj:
            holder.user_id = str(request_obj['username'])
            holder.user_pass = str(request_obj['password'])
            logger.log('user id: ' + str(holder.user_id))
            result = couch.authenticate(holder.user_id, holder.user_pass)
            response = jsonify(result)
            logger.log('Authentication results: ' + str(response))
            if result == 'Login Successful':
                logger.set_log_dir(holder.user_id)
            return response
        else:
            response = 'User & password can not be empty'
            logger.log(response)
            return response
    except:
        user_exception, log_exception = logger.get_exception()
        logger.log(str(log_exception) + "" + str(user_exception), logger.ERROR)
        logger.log('ERROR: Exception raised in auth()')
        raise


@app.route('/register', methods=['GET', 'POST'])
def register():
    try:
        logger.log('register()')
        request_obj = request.get_json(silent=True)
        if 'username' in request_obj and 'password' in request_obj and\
            'email' in request_obj and 'first_name' in request_obj and\
                'last_name' in request_obj:

            logger.log('registering user')
            username = request_obj['username']
            password = request_obj['password']
            email = request_obj['email']
            first_name = request_obj['first_name']
            last_name = request_obj['last_name']

            user_auth = {'first_name': first_name, 'last_name': last_name, 'email_id': email, 'pwd': password}
            email_auth = {'first_name': first_name, 'last_name': last_name, 'user_name': username, 'pwd': password}

            logger.log('user data: '+str(user_auth))

            user_resp = couch.store_user_auth(username, user_auth)
            email_resp = couch.store_email_auth(email, email_auth)
            logger.log('register response: '+ str(user_resp))
            return user_resp
        else:
            response = 'Invalid registration info'
            logger.log(response)
            return response
    except:
        user_exception, log_exception = logger.get_exception()
        logger.log(str(log_exception) + "" + str(user_exception), logger.ERROR)
        logger.log('ERROR: Exception raised in register()')
        raise


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    logger.log('upload_file()')
    logger.log('reset data')
    holder.reset_data()
    if request.method == 'POST':
        try:
            user_file = request.files['file']
        except:
            user_exception, log_exception = logger.get_exception()
            logger.log(log_exception, logger.ERROR)
            return 'File not found'

        delimiter = None
        data_source_type = get_extension(user_file.filename)
        logger.log('upload file name: '+ str(user_file.filename))
        logger.log('check if csv')
        if data_source_type == '.csv':
            delimiter = request.form['delimiter']
            logger.log('csv delimiter found: ' + str(delimiter))

        if user_file.filename == '':
            user_exception, log_exception = logger.get_exception()
            logger.log(log_exception, logger.ERROR)
            return 'Error: File not found'

        logger.log('Check if allowed file')
        if user_file and allowed_file(user_file.filename):
            filename = secure_filename(user_file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            logger.log('saving user file in upload folder')
            user_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            file_reader.file_name = filename
            file_reader.file_path = file_path
            holder.db_name = filename
            holder.data_source_type = data_source_type
            logger.log('user file path: ' + str(file_reader.file_path))
            logger.log('user file name: ' + str(holder.db_name))
            logger.log('data source type: ' + str(holder.data_source_type))
            try:
                logger.log('reading data')
                data_df = file_reader.read_file(file_path, delimiter)
                holder.data_df = data_df
                logger.log('reading data successful')
            except Exception as e:
                user_exception, log_exception = logger.get_exception()
                logger.log(str(log_exception) + "" + str(user_exception), logger.ERROR)
                return str(e)

            logger.log('file uploaded successfully')
            return 'File Uploaded Successfully'
        else:
            user_exception, log_exception = logger.get_exception()
            logger.log(str(log_exception) + "" + str(user_exception), logger.ERROR)
            logger.log('ERROR: Exception raised in upload_file()')
            return 'Unsupported File Format'


@app.route('/read_database', methods=['GET', 'POST'])
def read_database():
    request_obj = request.get_json(silent=True)
    try:
        logger.log('Checking database parameters')
        if 'host' in request_obj and 'port' in request_obj and 'user' in request_obj and 'password' in request_obj:
            logger.log('reading database params from request')
            db_reader.host = request_obj['host']
            db_reader.port = request_obj['port']
            db_reader.username = request_obj['user']
            db_reader.password = request_obj['password']
            logger.log('host: ' + db_reader.host)
            logger.log('port: ' + db_reader.port)
            logger.log('username: ' + db_reader.username)

            logger.log('reading available databases for user')
            available_dbs = db_reader.read_databases()
            response = jsonify({'available_dbs': available_dbs})
            logger.log('available dbs found: ' + str(response))
            return response
        else:
            response = 'Error: Please provide connection details'
            logger.log(response)
            return response
    except:
        user_exception, log_exception = logger.get_exception()
        logger.log(str(log_exception) + "" + str(user_exception), logger.ERROR)
        logger.log('ERROR: Exception raised in read_database()')
        raise


@app.route('/get_database_tables', methods=['GET', 'POST'])
def get_database_tables():
    try:
        logger.log('get_database_tables()')
        request_obj = request.get_json(silent=True)
        if 'db_name' in request_obj:
            logger.log('reading db_name')
            db_reader.db_name = request_obj['db_name']
            logger.log('db_name: ' + str(db_reader.db_name))

            logger.log('reading db tables')
            db_reader.select_database()
            response = jsonify({'available_tables': db_reader.read_tables()})
            logger.log('tables found: ' + response)
            return response
        else:
            response = 'Error: Please select valid database'
            logger.log(response)
            return response
    except:
        user_exception, log_exception = logger.get_exception()
        logger.log(str(log_exception) + "" + str(user_exception), logger.ERROR)
        logger.log('ERROR: Exception raised in get_database_tables()')
        raise


@app.route('/read_table', methods=['GET', 'POST'])
def read_table():
    try:
        logger.log('read_table()')
        request_obj = request.get_json(silent=True)
        if 'table_name' in request_obj:
            logger.log('reading table_name from request')
            holder.table_name = request_obj['table_name']
            logger.log('table_name: ' + str(holder.table_name))
            db_reader.table_name = holder.table_name

            logger.log('reading table data from database')
            holder.data_df = db_reader.read_table()
            logger.log('read complete')
            logger.log('converting data for user')
            form_data = extractor.extract_user_data(holder.data_df)

            holder.user_data = form_data
            response = jsonify({'data': holder.user_data})
            logger.log('data returned to user')
            return response
        else:
            response = 'Error: Please select valid table'
            logger.log(response)
            return response
    except:
        user_exception, log_exception = logger.get_exception()
        logger.log(str(log_exception) + "" + str(user_exception), logger.ERROR)
        logger.log('ERROR: Exception raised in read_table()')
        raise


@app.route('/get_download_file_name', methods=['GET', 'POST'])
def get_download_file_name():
    try:
        logger.log('get_download_file_name()')
        file_name = file_reader.file_name
        ext = get_extension(file_name)
        file_name = file_name.replace(ext, '')
        response = file_name

        logger.log('file_name: ' + response)
        return response
    except:
        user_exception, log_exception = logger.get_exception()
        logger.log(str(log_exception) + "|" + str(user_exception), logger.ERROR)
        logger.log('ERROR: Exception raised in get_download_file_name()')
        raise


@app.route('/get_data', methods=['GET', 'POST'])
def get_data():
    try:
        logger.log('get_data()')
        request_obj = request.get_json(silent=True)
        if holder.data_df is None:
            response = jsonify({'Error': 'No data set found'})
            logger.log(response)
            raise Exception(response)

        logger.log('reading request_data')
        if 'selected_table' in request_obj:
            selected_table = request_obj['selected_table']
            logger.log('selected_table: ' + str(selected_table))
            holder.table_name = selected_table

        logger.log('extracting user data')
        form_data = extractor.extract_user_data(holder.data_df, holder.data_source_type,
                                                holder.table_name, holder.db_name)
        holder.user_data = form_data
        response = {'data': holder.user_data}
        logger.log('returning user data')
        return jsonify(response)
    except Exception as e:
        user_exception, log_exception = logger.get_exception()
        logger.log(str(log_exception) + "" + str(user_exception), logger.ERROR)
        logger.log("ERROR: Exception raised in get_data()")
        raise


@app.route('/get_columns', methods=['GET', 'POST'])
def get_columns():
    try:
        logger.log('get_columns()')
        if holder.data_df is None:
            response = jsonify({'Error': 'No data set found'})
            logger.log(response)
            return response
        request_obj = request.get_json(silent=True)
        logger.log('reading request data')
        if 'selected_table' in request_obj:
            selected_table = request_obj['selected_table']
            logger.log('selected_table: ' + str(selected_table))
            holder.table_name = selected_table
        logger.log('extracting data columns')
        columns = extractor.extract_column_names(holder.data_df, holder.data_source_type,
                                                 holder.table_name, holder.db_name)

        response = jsonify({'columns': columns})
        logger.log(response)
        return response
    except:
        user_exception, log_exception = logger.get_exception()
        logger.log(str(log_exception) + "" + str(user_exception), logger.ERROR)
        logger.log('ERROR: Exception raised in get_columns()')
        raise


@app.route('/get_sheets', methods=['GET', 'POST'])
def get_sheets():
    logger.log('get_sheets()')
    logger.log('validating sheet_names not null')
    if file_reader.sheet_names is not None:
        sheet_names = file_reader.sheet_names
        logger.log('sheets: ' + str(sheet_names))
    else:
        response = jsonify({'Error': 'Please upload valid data set'})
        logger.log(response)
        return response
    print('here1')
    if type(sheet_names) is type(str):
        sheet_names = [sheet_names]
        print('here2')
    if file_reader.file_name is not None:
        print('here3')
        response = jsonify({'sheets': {file_reader.file_name: sheet_names}})
        print(response)
        print('here4')
        logger.log(response)
        print('here5')
        return response
    else:
        user_exception, log_exception = logger.get_exception()
        logger.log(str(log_exception) + "" + str(user_exception), logger.ERROR)
        error_resp = jsonify({'Error': 'Please upload valid data set'})
        logger.log(error_resp)
        raise Exception(error_resp)


@app.route('/update_train_vars', methods=['GET', 'POST'])
def update_train_vars():
    try:
        logger.log('update_train_vars()')
        request_obj = request.get_json(silent=True)

        logger.log('reading training variables from request')
        if 'train_vars' in request_obj and holder.data_df is not None:
            train_vars = request_obj['train_vars']
            holder.train_vars = train_vars
            logger.log('train_vars: ' + str(holder.train_vars))
            logger.log('extracting training columns data')
            train_df = extractor.extract_column_data(holder.data_df, train_vars, holder.data_source_type,
                                                     holder.table_name, holder.db_name)
            logger.log('extraction complete')
            holder.train_user_data, holder.train_df = train_df
            response = 'Training Variables updated successfully'
            logger.log(response)
            return response
        else:
            response = jsonify({'Error': 'Please upload valid data set'})
            logger.log(response)
            return response
    except:
        user_exception, log_exception = logger.get_exception()
        logger.log(str(log_exception) + "" + str(user_exception), logger.ERROR)
        logger.log('ERROR: Exception raised in update_train_vars()')
        raise


@app.route('/update_target_vars', methods=['GET', 'POST'])
def update_target_vars():
    try:
        logger.log('update_target_vars()')
        request_obj = request.get_json(silent=True)
        logger.log('reading request data')
        if 'target_var' in request_obj and holder.data_df is not None:
            target_var = request_obj['target_var']
            holder.target_var = target_var
            logger.log('target_var: ' + str(target_var))

            logger.log('extracting test data')
            target_df = extractor.extract_column_data(holder.data_df, target_var, holder.data_source_type,
                                                      holder.table_name, holder.db_name)

            logger.log('extraction complete')
            holder.target_user_data, holder.target_df = target_df
            response = 'Target Variable updated successfully'
            logger.log(response)
            return response
        else:
            response = jsonify({'Error': 'Please upload valid data set'})
            logger.log(response)
            return response
    except:
        user_exception, log_exception = logger.get_exception()
        logger.log(str(log_exception) + "" + str(user_exception), logger.ERROR)
        logger.log('ERROR: Exception raised in update_target_vars()')
        raise


@app.route('/get_train_vars', methods=['GET', 'POST'])
def get_train_vars():
    try:
        logger.log('get_train_vars()')
        logger.log('checking if train vars not null')
        if holder.train_vars is not None:
            response = jsonify({'train_vars': holder.train_vars})
            logger.log(response)
            return response
        else:
            response = jsonify({'Error': 'You must select training variables'})
            logger.log(response)
            return response
    except:
        user_exception, log_exception = logger.get_exception()
        logger.log(str(log_exception) + "" + str(user_exception), logger.ERROR)
        logger.log('ERROR: Exception raised in get_train_vars()')
        raise


@app.route('/get_target_vars', methods=['GET', 'POST'])
def get_target_vars():
    try:
        logger.log('get_target_vars()')
        logger.log('checking if target var not null')
        if holder.target_var is not None:
            response = jsonify({'target_vars': holder.target_var})
            logger.log(response)
            return response
        else:
            response = jsonify({'Error': 'You must select target variable'})
            logger.log(response)
            return response
    except:
        user_exception, log_exception = logger.get_exception()
        logger.log(str(log_exception) + "" + str(user_exception), logger.ERROR)
        logger.log('ERROR: Exception raised in get_target_vars()')
        raise


@app.route('/get_training_data', methods=['GET', 'POST'])
def get_training_data():
    try:
        logger.log('get_training_data()')
        if holder.train_user_data is not None:
            response = jsonify({'train_data': holder.train_user_data})
            logger.log('returning training data to user')
            return response
        else:
            response = jsonify({'Error': 'No data set found for training'})
            logger.log(response)
            return response
    except:
        user_exception, log_exception = logger.get_exception()
        logger.log(str(log_exception) + "" + str(user_exception), logger.ERROR)
        logger.log('ERROR: Exception raisedi n get_training_data()')
        raise


@app.route('/set_selected_data', methods=['GET', 'POST'])
def set_selected_data():
    try:
        logger.log('set_selected_data()')
        logger.log('checking if train and target data is empty')
        if holder.train_df is not None and holder.target_df is not None:
            selected_df = extractor.merge_data_by_col([holder.train_df, holder.target_df])
            holder.selected_df = selected_df
            holder.selected_user_data = extractor.extract_user_data(holder.selected_df)
            logger.log('train and target data is available to show user')
            return jsonify(True)
        else:
            response = "Training or Target Variable selection isn't completed"
            logger.log(response)
            return response
    except:
        user_exception, log_exception = logger.get_exception()
        logger.log(str(log_exception) + "" + str(user_exception), logger.ERROR)
        logger.log('ERROR: Exception raised in set_selected_data()')
        raise


@app.route('/get_selected_data', methods=['GET', 'POST'])
def get_selected_data():
    try:
        logger.log('get_selected_data()')
        if holder.train_df is not None and holder.target_df is not None:
            response = jsonify({'selected_data': holder.selected_user_data})
            logger.log('data found and sending back to user')
            return response
        else:
            response = jsonify({'Error': 'You must select training & target variables from uploaded dataset'})
            logger.log(response)
            return response
    except:
        user_exception, log_exception = logger.get_exception()
        logger.log(str(log_exception) + "" + str(user_exception), logger.ERROR)
        logger.log('ERROR: Exception raised in get_selected_data()')
        raise


@app.route('/get_selected_columns', methods=['GET', 'POST'])
def get_selected_columns():
    try:
        logger.log('get_selected_columns()')
        if holder.processed_data is not None:
            selected_columns = list(holder.processed_data.columns)
            response = jsonify({'selected_columns': selected_columns})
            logger.log(response)
            return response

        if holder.selected_df is not None:
            selected_columns = list(holder.selected_df.columns)
            response = jsonify({'selected_columns': selected_columns})
            logger.log(response)
            return response
        else:
            response = jsonify({'Error': 'Training and Target Variables not selected'})
            logger.log(response)
            return response
    except:
        user_exception, log_exception = logger.get_exception()
        logger.log(str(log_exception) + "" + str(user_exception), logger.ERROR)
        logger.log('ERROR: Exception raised in get_selected_columns()')
        raise


@app.route('/get_data_description', methods=['GET', 'POST'])
def get_data_description():
    try:
        logger.log('get_data_description()')
        if holder.selected_df is None:
            response = jsonify({'Error': 'You must select training & target variables'})
            logger.log(response)
            return response
        logger.log('extracting stats description')
        holder.desc_df = stats.get_data_description(holder.selected_df)
        logger.log('extracting user_data')
        holder.desc_user_data = extractor.extract_user_data(holder.desc_df)
        response = jsonify({'desc_data': holder.desc_user_data})
        logger.log('sending user_data')
        return response

    except:
        user_exception, log_exception = logger.get_exception()
        logger.log(str(log_exception) + "" + str(user_exception), logger.ERROR)
        logger.log('ERROR: Exception raised in get_data_description()')
        raise


@app.route('/get_data_correlation', methods=['GET', 'POST'])
def get_data_correlation():
    try:
        logger.log('get_data_correlation()')
        if holder.selected_df is None:
            response = jsonify({'Error': 'You must select training & target variables'})
            logger.log(response)
            return response
        logger.log('extracting correlation matrix')
        holder.correlation_df = stats.get_correlation(holder.selected_df)
        logger.log('extracting user_data')
        holder.correlation_user_data = extractor.extract_user_data(holder.correlation_df)
        response = jsonify({'corr_data': holder.correlation_user_data})
        logger.log('sending user_data')
        return response
    except:
        user_exception, log_exception = logger.get_exception()
        logger.log(str(log_exception) + "" + str(user_exception), logger.ERROR)
        logger.log('ERROR: Exception raised in get_data_correlation()')
        raise


@app.route('/get_columns_to_filter', methods=['GET', 'POST'])
@cross_origin()
def get_columns_to_filter():
    try:
        logger.log('get_columns_to_filter()')
        request_obj = request.get_json(silent=True)
        if holder.selected_df is None:
            response = jsonify({'Error': 'You must select training & target variables'})
            logger.log(response)
            return response

        if 'selected_method' in request_obj:
            selected_method = request_obj['selected_method']
            logger.log('selected_method: ' + selected_method)
            columns_to_filter = extractor.extract_columns_to_filter(holder.selected_df, selected_method)
            response = jsonify({'columns_to_filter': columns_to_filter})
            logger.log(response)
            return response
        else:
            response = jsonify({'Error': 'You must select method to apply'})
            logger.log(response)
            return response
    except:
        user_exception, log_exception = logger.get_exception()
        logger.log(str(log_exception) + "" + str(user_exception), logger.ERROR)
        logger.log('ERROR: Exception raised in get_columns_to_filter()')
        raise


@app.route('/get_graph_data', methods=['GET', 'POST'])
def get_graph_data():
    try:
        logger.log('get_graph_data()')
        if holder.selected_df is None:
            response = jsonify({'Error': 'You must select training & target variables'})
            logger.log(response)
            return response

        request_obj = request.get_json(silent=True)
        if 'column_names' in request_obj:
            column_names = request_obj['column_names']
            logger.log('column_names: ' + str(column_names))
            graph_data = extractor.extract_data_for_graph(holder.selected_df, column_names)
            response = jsonify({'graph_data': graph_data})
            logger.log(response)
            return response
        else:
            response = jsonify({'Error': 'You must select column(s) to draw graph'})
            logger.log(response)
            return response

    except:
        user_exception, log_exception = logger.get_exception()
        logger.log(str(log_exception) + "" + str(user_exception), logger.ERROR)
        logger.log('ERROR: Exception raised in get_graph_data()')
        raise


@app.route('/get_string_columns', methods=['GET', 'POST'])
def get_string_columns():
    try:
        logger.log('get_string_columns()')
        if holder.selected_df is None:
            response = jsonify({'Error': 'You must select training & target variables'})
            logger.log(response)
            return response
        logger.log('extracting string columns')
        string_columns = extractor.extract_string_columns(holder.selected_df)
        response = jsonify({'string_columns': string_columns})
        logger.log(response)
        return response

    except:
        user_exception, log_exception = logger.get_exception()
        logger.log(str(log_exception) + "" + str(user_exception), logger.ERROR)
        logger.log('ERROR: Exception raised in get_string_columns')
        raise


@app.route('/process_null_columns', methods=['GET', 'POST'])
def process_null_columns():
    try:
        logger.log('process_null_columns()')
        if holder.selected_df is None:
            response = jsonify({'Error': 'You must select training & target variables'})
            logger.log(response)
            return response

        request_obj = request.get_json(silent=True)
        if 'selected_method' in request_obj and 'selected_column' in request_obj:
            selected_method = request_obj['selected_method']
            selected_column = request_obj['selected_column']
            logger.log('selected_method: ' + selected_method)
            logger.log('selected_column: ' + selected_column)
            if selected_method not in holder.available_methods:
                response = "Error: Selected method isn't available"
                logger.log(response)
                return response
            if selected_column in holder.target_var and selected_method == 'drop_missing_column':
                response = "Error: Can't apply drop missing on target variable, please select different method to deal " \
                           "with null values in selected target variable"
                logger.log(response)
                return response

            if holder.processed_data is not None:
                columns = list(holder.processed_data.columns)
                if holder.target_var in columns:
                    columns = columns.remove(holder.target_var)
                if selected_column in columns and len(columns) <= 1 and selected_method == 'drop_missing_column':
                    response = "Error: Unable to apply drop column on selected method, Reason: Training variable's" \
                               "lenght can't be less than 0"
                    logger.log(response)
                    return response
            logger.log('processing null columns')
            holder.processed_data = processor.process_null_columns(holder.selected_df, selected_column, selected_method)
            logger.log('extracting user data')
            holder.processed_user_data = extractor.extract_user_data(holder.processed_data)
            holder.append_methods_applied(selected_method + ' [ ' + selected_column + ' ]')
            logger.log('methods_applied: ' + str(holder.get_methods_applied()))
            response = selected_method.upper() + ' applied successfully on column [' + selected_column + ']'
            logger.log(response)
            return response
        else:
            response = 'No options selected'
            logger.log(response)
            return response
    except:
        user_exception, log_exception = logger.get_exception()
        logger.log(str(log_exception) + "" + str(user_exception), logger.ERROR)
        logger.log('ERROR: Exception raised in process_null_columns()')
        raise


@app.route('/process_attribute_encoding', methods=['GET', 'POST'])
def process_attribute_encoding():
    try:
        logger.log('process_attribute_encoding()')
        if holder.selected_df is None:
            response = jsonify({'Error': 'You must select training & target variables'})
            logger.log(response)
            return response

        request_obj = request.get_json(silent=True)
        if 'selected_column' in request_obj:
            selected_column = request_obj['selected_column']
            logger.log('selected_column: ' + str(selected_column))
            logger.log('processing attribute encoding')
            holder.processed_data = processor.process_attribute_encoding(holder.selected_df, selected_column)
            logger.log('extracting user data')
            holder.processed_user_data = extractor.extract_user_data(holder.processed_data)
            holder.append_attributes_encoded(selected_column)
            logger.log('attributes_encoded: ' + str(holder.get_attributes_encoded()))
            response = 'Attribute encoding applied to column [' + selected_column + ']'
            logger.log(response)
            return response
        else:
            response = 'No column selected'
            logger.log(response)
            return response
    except:
        user_exception, log_exception = logger.get_exception()
        logger.log(str(log_exception) + "" + str(user_exception), logger.ERROR)
        logger.log('ERROR: Exception raised in process_attribute_encoding')
        raise


@app.route('/get_applied_methods', methods=['GET', 'POST'])
def get_applied_methods():
    try:
        logger.log('get_applied_methods()')
        response = jsonify({'applied_methods': holder.get_methods_applied()})
        logger.log(response)
        return response
    except:
        user_exception, log_exception = logger.get_exception()
        logger.log(str(log_exception) + "" + str(user_exception), logger.ERROR)
        logger.log('ERROR: Exception raised in get_applied_methods()')
        raise


@app.route('/get_attributes_encoded', methods=['GET', 'POST'])
def get_attributes_encoded():
    try:
        logger.log('get_attributes_encoded()')
        response = jsonify({'attributes_encoded': holder.get_attributes_encoded()})
        logger.log(response)
        return response
    except:
        user_exception, log_exception = logger.get_exception()
        logger.log(str(log_exception) + "" + str(user_exception), logger.ERROR)
        logger.log('ERROR: Exception raised in get_attributes_encoded()')
        raise


@app.route('/get_processed_data', methods=['GET', 'POST'])
def get_processed_data():
    try:
        logger.log('get_processed_data()')
        logger.log('checking if processed data df is not null')
        if holder.processed_data is not None:
            response = jsonify({'processed': holder.processed_user_data})
            return response
        else:
            logger.log('returning selected_user_data')
            response = jsonify({'processed': holder.selected_user_data})
            return response
    except:
        user_exception, log_exception = logger.get_exception()
        logger.log(str(log_exception) + "" + str(user_exception), logger.ERROR)
        raise


@app.route('/overwrite_existing_data', methods=['GET', 'POST'])
def overwrite_existing_data():
    try:
        logger.log('overwrite_existing_data')
        if holder.processed_data is not None:
            holder.selected_df = holder.processed_data
            holder.selected_user_data = holder.processed_user_data

            data_columns = list(holder.processed_data.columns)
            updated_train_columns = list(set(data_columns).intersection(holder.train_vars))
            updated_target_columns = list(set(data_columns).intersection(holder.target_var))

            holder.train_vars = updated_train_columns
            holder.target_var = updated_target_columns

            response = jsonify({'msg': 'Data, training variables and target variable updated successfully', 'success': True})
            logger.log(response)
            return response
        else:
            response = jsonify({'msg': 'No changes to overwrite', 'success': False})
            logger.log(response)
            return response
    except:
        user_exception, log_exception = logger.get_exception()
        logger.log(str(log_exception) + "" + str(user_exception), logger.ERROR)
        logger.log('ERROR: Exception raised in overwrite_existing_data()')
        raise


###########################################################################################     MACHINE LEARNING APIS   #############################################################################


@app.route('/set_analysis_mode', methods=['GET', 'POST'])
def set_analysis_mode():
    try:
        logger.log('set_analysis_mode()')
        request_obj = request.get_json(silent=True)
        if 'analysis_mode' in request_obj:
            analysis_mode = request_obj['analysis_mode']
            holder.analysis_mode = analysis_mode.strip().lower()
            logger.log('analysis_mode: ' + str(analysis_mode))
            return 'navigate'
    except:
        user_exception, log_exception = logger.get_exception()
        logger.log(str(log_exception) + "" + str(user_exception), logger.ERROR)
        logger.log('ERROR: Exception raised in set_analysis_mode()')
        raise


@app.route('/get_analysis_mode', methods=['GET', 'POST'])
def get_analysis_mode():
    try:
        logger.log('get_analysis_mode()')
        response = jsonify({'analysis_mode': holder.analysis_mode})
        logger.log(response)
        return response
    except:
        user_exception, log_exception = logger.get_exception()
        logger.log(str(log_exception) + "" + str(user_exception), logger.ERROR)
        logger.log('ERROR: Exception raised in get_analysis_mode()')
        raise


@app.route('/get_available_algorithms', methods=['GET', 'POST'])
def get_available_algorithms():
    logger.log('get_available_algorithms()')
    if holder.analysis_mode == 'regression':
        response = jsonify({'available_algorithms': holder.regression_algorithms})
        logger.log(response)
        return response
    elif holder.analysis_mode == 'classification':
        response = jsonify({'available_algorithms': holder.classification_algorithms})
        logger.log(response)
        return response
    else:
        response = 'No analysis mode selected'
        logger.log(response)
        return response


@app.route('/set_selected_algorithms', methods=['GET', 'POST'])
def set_selected_algorithms():
    try:
        logger.log('set_selected_algorithms()')
        request_obj = request.get_json(silent=True)
        if 'selected_algorithms' in request_obj:
            selected_algorithms = request_obj['selected_algorithms']
            logger.log('selected_algorithms: ' + str(selected_algorithms))
            holder.selected_algorithms = selected_algorithms
            holder.selected_algorithms_params = {}
            logger.log('extracting algorithms parameters')
            if holder.selected_algorithms is None:
                response = 'ERROR: Please select algorithms to execute'
                logger.log(response)
                return response

            if holder.analysis_mode == 'regression':
                for algorithm in holder.selected_algorithms:
                    holder.selected_algorithms_params[algorithm] = holder.regression_params[algorithm]
            elif holder.analysis_mode == 'classification':
                for algorithm in holder.selected_algorithms:
                    holder.selected_algorithms_params[algorithm] = holder.classification_params[algorithm]
            else:
                response = 'No analysis mode selected'
                logger.log(response)
                return response

            response = 'Algorithm selection updated'
            logger.log(response)
            return response
        else:
            response = 'No algorithms selected to update'
            logger.log(response)
            return response
    except:
        user_exception, log_exception = logger.get_exception()
        logger.log(str(log_exception) + "" + str(user_exception), logger.ERROR)
        logger.log('ERROR: Exception raised in set_selected_algorithms()')
        raise


@app.route('/get_selected_algorithms', methods=['GET', 'POST'])
def get_selected_algorithms():
    try:
        logger.log('get_selected_algorithms()')
        if holder.selected_algorithms is None:
            logger.log('no algorithms selected')
        response = jsonify({'selected_algorithms': holder.selected_algorithms})
        logger.log(response)
        return response
    except:
        user_exception, log_exception = logger.get_exception()
        logger.log(str(log_exception) + "" + str(user_exception), logger.ERROR)
        logger.log('ERROR: Exception raised in get_selected_algorithms')
        raise


@app.route('/get_algorithm_params', methods=['GET', 'POST'])
def get_algorithm_params():
    try:
        logger.log('get_algorithm_params()')
        response = jsonify({'algorithm_params': holder.selected_algorithms_params})
        logger.log(response)
        return response
    except:
        user_exception, log_exception = logger.get_exception()
        logger.log(str(log_exception) + "" + str(user_exception), logger.ERROR)
        logger.log('ERROR: Exception raised in get_algorithm_params()')
        raise


@app.route('/set_test_size', methods=['GET', 'POST'])
def set_training_size():
    try:
        logger.log('set_training_size()')
        request_obj = request.get_json(silent=True)
        if 'test_size' in request_obj:
            holder.test_size = request_obj['test_size']
            logger.log('test_size: ' + str(holder.test_size))
            response = 'Test size updated successfully'
            logger.log(response)
            return response
        else:
            response = 'Test size not specified using default: [80:20] split'
            logger.log(response)
            return response

    except:
        user_exception, log_exception = logger.get_exception()
        logger.log(str(log_exception) + "" + str(user_exception), logger.ERROR)
        logger.log('ERROR: Exception raised in set_training_size()')
        raise


@app.route('/get_test_size', methods=['GET', 'POST'])
def get_test_size():
    try:
        logger.log('get_test_size()')
        response = jsonify({'test_size': holder.test_size})
        logger.log(response)
        return response
    except:
        user_exception, log_exception = logger.get_exception()
        logger.log(str(log_exception) + "" + str(user_exception), logger.ERROR)
        logger.log('ERROR: Exception raised in get_test_size()')
        raise


@app.route('/apply_selected_algorithms', methods=['GET', 'POST'])
def apply_selected_algorithms():
    try:
        logger.log('apply_selected_algorithms()')
        request_obj = request.get_json(silent=True)
        if 'updated_algorithms' in request_obj:
            request_obj = json.loads(request.data.decode())
            updated_algorithms = request_obj['updated_algorithms']
            logger.log('updated_algorithms: ' + str(updated_algorithms))
            holder.algorithm_results, holder.training_data, \
            holder.test_data, holder.predicted_data = apply_algorithms(holder.analysis_mode, holder.selected_df,
                                                                       holder.train_vars, holder.target_var,
                                                                       updated_algorithms, holder.test_size)

            holder.train_user_data = extractor.extract_user_data(holder.training_data)
            holder.test_user_data = extractor.extract_user_data(holder.test_data)
            holder.predicted_data = extractor.extract_user_data(holder.predicted_data)

            response = 'Algorithms successfully executed'
            logger.log(response)
            return response
    except:
        user_exception, log_exception = logger.get_exception()
        logger.log(str(log_exception) + "" + str(user_exception), logger.ERROR)
        logger.log('ERROR: Exception raised in apply_selected_algorithms()')
        raise


@app.route('/get_algorithm_results', methods=['GET', 'POST'])
def get_algorithm_results():
    try:
        logger.log('get_algorithm_results()')
        response = jsonify({'algorithm_results': holder.algorithm_results})
        logger.log(response)
        return response
    except:
        user_exception, log_exception = logger.get_exception()
        logger.log(str(log_exception) + "" + str(user_exception), logger.ERROR)
        logger.log('ERROR: Exception raised in get_algorithm_results()')
        raise


@app.route('/get_train_split_data', methods=['GET', 'POST'])
def get_train_split_data():
    try:
        logger.log('get_train_split_data()')
        response = jsonify({'training_data': holder.training_user_data})
        logger.log('returning training user_data')
        return response
    except:
        user_exception, log_exception = logger.get_exception()
        logger.log(str(log_exception) + "" + str(user_exception), logger.ERROR)
        logger.log('ERROR: Exception raised in get_train_split_data()')
        raise


@app.route('/get_test_split_data', methods=['GET', 'POST'])
def get_test_split_data():
    try:
        logger.log('get_test_split_data()')
        response = jsonify({'test_data': holder.test_user_data})
        logger.log('returning test_split user_data')
        return response
    except:
        user_exception, log_exception = logger.get_exception()
        logger.log(str(log_exception) + "" + str(user_exception), logger.ERROR)
        logger.log('ERROR: Exception raised in get_test_split_data()')
        raise


@app.route('/get_predicted_data', methods=['GET', 'POST'])
def get_predicted_data():
    try:
        logger.log('get_predicted_data()')
        response = jsonify({'predicted_data': holder.predicted_user_data})
        logger.log('returning predicted_user_data')
        return response
    except:
        user_exception, log_exception = logger.get_exception()
        logger.log(str(log_exception) + "" + str(user_exception), logger.ERROR)
        logger.log('ERROR: Exception raised in get_predicted_data()')
        raise


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
