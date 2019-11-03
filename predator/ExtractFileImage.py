import os
import cv2
import shutil
import ntpath
import docx2txt
import subprocess
import numpy as np

class ImageExtractor():
    def ExtractImageFromPDF(self, pdf_path):
        cmd = 'pdfimages ' + pdf_path + ' fileimage'
        os.system(cmd)
        extracted_images = []
        for file in os.listdir(os.getcwd()):
            if file.endswith(".ppm"):
                extracted_images.append(os.path.join(os.getcwd(), file))

        return extracted_images


    def ExtractImageFromWord(self, file_path):

        file_name, file_ext = os.path.splitext(file_path)

        if file_ext == '.odt':
            subprocess.call('libreoffice  --invisible -convert-to docx --headless "{}"'.format(file_name+file_ext), shell=True)

        text = docx2txt.process(file_path, "word_img/")
        extracted_images = []
        for file in os.listdir(os.getcwd()+'/word_img/'):
            if file.endswith(".jpeg") or file.endswith('.png') or file.endswith('.jpg'):
                extracted_images.append(os.path.join(os.getcwd()+'/word_img/', file))

        return extracted_images

    def ExtractImageFromPPT(self, file_path):
        file_n = ntpath.basename(file_path)
        print(file_n)
        file_name, file_ext = os.path.splitext(file_n)
        cmd = 'libreoffice --headless --invisible --convert-to pdf '+file_path
        os.system(command=cmd)
        print(file_name)
        cmd = 'pdfimages ' + file_name + '.pdf image'
        os.system(cmd)
        extracted_images = []
        for file in os.listdir(os.getcwd()):
            if file.endswith(".ppm"):
                extracted_images.append(os.path.join(os.getcwd(), file))

        return extracted_images


    def ExtractImageFromExcel(self, file_path):
        file_n = ntpath.basename(file_path)
        print(file_n)
        file_name, file_ext = os.path.splitext(file_n)
        print(os.getcwd())
        if file_ext == '.xlsx':
            #libreoffice  --invisible -convert-to pdf --headless "excel_example.xlsx"

            subprocess.call('libreoffice  --invisible -convert-to pdf --headless "{}"'.format(file_path), shell=True)
            #pdfimages excel_example.pdf fileimage
            print(file_name)
            subprocess.call('pdfimages "{}" fileimage'.format(file_name+'.pdf'), shell=True)
            extracted_images = []
            for file in os.listdir(os.getcwd()):
                if file.endswith(".ppm"):
                    extracted_images.append(os.path.join(os.getcwd(), file))

            return extracted_images

    def ExtractImagesFromVideo(self, file_path):
        file_name, file_ext = os.path.splitext(file_path)

        # set video file path of input video with name and extension
        vid = cv2.VideoCapture(file_path)

        if not os.path.exists('images'):
            os.makedirs('images')

        # for frame identity
        index = 0
        while (True):
            # Extract images
            ret, frame = vid.read()
            # end of frames
            if not ret:
                break
            # Saves images
            name = './images/frame' + str(index) + '.jpg'
            print('Creating...' + name)
            cv2.imwrite(name, frame)

            # next frame
            index += 1

        extracted_images = []
        for file in os.listdir(os.getcwd()+'/images/'):
            if file.endswith(".jpg"):
                extracted_images.append(os.path.join(os.getcwd()+'/images/', file))

        shutil.rmtree(os.getcwd()+'/images/')

        return extracted_images
