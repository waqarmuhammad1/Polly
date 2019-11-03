# import os
# from Commons import *
# from flask_cors import CORS
# from flask import Flask, render_template, request, json
# from werkzeug.utils import secure_filename
#
# app = Flask(__name__)
#
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
# CORS(app)
#
#
# @app.route('/uploader', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         try:
#             file = request.files['file']
#         except:
#             return 'File not found'
#         if file.filename == '':
#             return 'No File Selected'
#
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             print(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             return 'File Uploaded Successfully'
#         else:
#             return 'Unsupported File Format'
#
#
# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
#
# import pandas as pd
# from Statistics import Stats
# from DataExtractor import Extractor
#
# stats = Stats()
# extractor = Extractor()
# df = pd.read_excel('/home/waqar/PycharmProjects/predator/user_files/data.xlsx', sheet_name='plot_parameter', index_col=False)
# desc = stats.get_data_description(df)
# desc['Statistics'] = desc.index
# cols = desc.columns.tolist()
# cols = cols[-1:] + cols[:-1]
# desc = desc[cols]
# desc.reset_index()
# desc_dict = desc.to_dict()
# internal_keys = list(desc_dict[list(desc_dict.keys())[0]].keys())
# # print internal_keys
#
#
# reversed_dict = {}
#
# for x in internal_keys:
#     temp_dict = {}
#     for y in desc_dict:
#         temp_dict[y] = desc_dict[y][x]
#
#     reversed_dict[x] = temp_dict
#
# print(reversed_dict)
# print(desc_dict)
#
# print extractor.extract_user_data(desc)
# print desc

# print list(df.columns)
# sheet_columns = list(df.columns)
# updated_columns = [u'B', u'DB', u'G', u'GNDVI', u'Green', u'Height', u'IKAW']
# final = set(sheet_columns).intersection(set(updated_columns))
# print list(final)



# import pandas as pd
# import mysql.connector as sql
#
# # db_connection = sql.connect(host='204.48.26.70', user='root', password='admin1234')
# db_connection = sql.connect(host="204.48.26.70", port=3306, user='root', passwd='admin1234')
# print(list(pd.read_sql('SHOW databases', db_connection)['Database']))
# sql_select_Query = "use Titanic"
# cursor = db_connection.cursor()
# cursor.execute(sql_select_Query)
# print (pd.read_sql('USE Titanic', db_connection))
# print (list(pd.read_sql('SHOW tables', db_connection)['Tables_in_Titanic']))
# df = pd.read_sql('SELECT * FROM titanic', db_connection)
# print(list(df.columns))
#
# import pandas as pd
#
# algos = {u'Support Vector': {u'kernel': u'rbf', u'C': 1, u'verbose': False, u'probability': False, u'degree': 3,
#                              u'coef0': 0, u'max_iter': -1, u'decision_function_shape': 'ovr', u'random_state': None,
#                              u'tol': 0.001, u'cache_size': 200, u'shrinking': True, u'gamma': u'auto_deprecated',
#                              u'class_weight': u'None'},
#          u'Bernoulli Naive Bayes': {u'binarize': 0, u'alpha': 1, u'fit_prior': True, u'class_prior': None},
#          u'Linear SVC': {u'kernel': u'linear', u'C': 1, u'verbose': False, u'probability': False, u'degree': 3,
#                          u'coef0': 0, u'max_iter': -1, u'decision_function_shape': u'ovr', u'random_state': None,
#                          u'tol': 0.001, u'cache_size': 200, u'shrinking': True, u'gamma': u'auto_deprecated',
#                          u'class_weight': u'None'},
#          u'Gausian Naive Bayes': {u'priors': None, u'var_smoothing': 1e-09}}
# import sklearn
# print(sklearn.__version__)
#
# df = pd.read_excel('/home/waqar/Downloads/data_titanic.xlsx')
# print (df.columns)
#
# train = ['Age', 'Fare', 'Pclass', 'Sex']
# target = ['Survived']
#
# from ClassificationController import *
#
#
# print(Perform_Classification(df, train, target, algos))


class upload(Resource):
    def post(self):
        request_data = json.loads(request.data.decode())
        return Controller.upload_data(request_data)

class auth:
    def post(self):
        try:
            logger.log('auth()')
            request_obj = json.loads(request.data.decode())
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


import flask_restful
from flask_cors import CORS, cross_origin
from flask import Flask, request, jsonify
from flask_restful import Api
from werkzeug.utils import secure_filename