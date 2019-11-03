import os

UPLOAD_FOLDER = 'user_files/'
ALLOWED_EXTENSIONS = set(['csv', 'xls', 'xlsx'])
ALLOWED_EXTENSIONS_HSA = set(['jpg', 'jpeg', 'pdf', 'docx', 'xlsx', 'ppt', 'png'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_extension(file_path):
    filename, file_extension = os.path.splitext(file_path)
    return file_extension


def allowed_file_HSA(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_HSA
