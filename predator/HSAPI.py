from Commons import *
from logger import Logger
from HSAController import *


import flask_restful
from flask_cors import CORS, cross_origin
from flask import Flask, request, jsonify
from flask_restful import Api
from werkzeug.utils import secure_filename


logger = Logger()

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


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    logger.log('upload_file()')
    logger.log('reset data')

    if request.method == 'POST':
        try:
            user_file = request.files['file']
            print(user_file)
        except:
            user_exception, log_exception = logger.get_exception()
            logger.log(log_exception, logger.ERROR)
            return 'File not found'

        data_source_type = get_extension(user_file.filename)
        logger.log('upload file name: ' + str(user_file.filename))
        logger.log('data_source_type: ' + str(data_source_type))

        if user_file.filename == '':
            user_exception, log_exception = logger.get_exception()
            logger.log(log_exception, logger.ERROR)
            return 'Error: File not found'

        logger.log('Check if allowed file')
        if user_file and allowed_file_HSA(user_file.filename):
            filename = secure_filename(user_file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            logger.log('saving user file in upload folder')
            user_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            logger.log('user file path: ' + str(file_path))
            try:
                logger.log('Analyzing file')
                result = ExtractAnalyzeImageFromFile(file_path)
                print(result)
                logger.log('Analyzation successful')
                logger.log(result)
            except Exception as e:
                user_exception, log_exception = logger.get_exception()
                logger.log(str(log_exception) + "" + str(user_exception), logger.ERROR)
                return str(e)

            logger.log('file uploaded successfully')
            return result
        else:
            user_exception, log_exception = logger.get_exception()
            logger.log(str(log_exception) + "" + str(user_exception), logger.ERROR)
            logger.log('ERROR: Exception raised in upload_file()')
            return 'Unsupported File Format'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001, threaded=True)
