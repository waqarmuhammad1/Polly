from HumanSubDetection import *
from ExtractFileImage import *


def ExtractAnalyzeImageFromFile(file_path):
    image_ext = ImageExtractor()

    file_name, file_ext = os.path.splitext(file_path)
    if file_ext == '.xlsx':
        extracted_images = image_ext.ExtractImageFromExcel(file_path)
    elif file_ext == '.pdf':
        extracted_images = image_ext.ExtractImageFromPDF(file_path)
    elif file_ext == '.docx':
        extracted_images = image_ext.ExtractImageFromWord(file_path)
    elif file_ext == '.ppt':
        extracted_images = image_ext.ExtractImageFromPPT(file_path)
    elif file_ext == '.jpg' or file_ext == '.png' or file_ext == '.jpeg' or file_ext == '.ppm':
        detection_result = detectHumanSubj(file_path)
        if detection_result == 1:
            return 'Uploaded file has human subject'
        else:
            'File upload successful'
    else:
        return 'File format not supported'

    for images in extracted_images:
        detection_result = detectHumanSubj(images)

        if detection_result == 1:
            return 'Uploaded file has human subject'

    return 'File upload successful'


# print(ExtractImageFromFile('HSA_input_files/sample.ppt'))
