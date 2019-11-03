import os
from imageai.Detection import ObjectDetection
from logger import Logger

logger = Logger()



def detectHumanSubj(image_path):
    try:
        execution_path = os.getcwd()
        detector = ObjectDetection()
        detector.setModelTypeAsRetinaNet()
        detector.setModelPath(os.path.join(execution_path, "resnet50_coco_best_v2.0.1.h5"))
        detector.loadModel()
        custom_objects = detector.CustomObjects(person=True, car=False)
        print(os.path.join(execution_path, image_path))
        detections = detector.detectCustomObjectsFromImage(input_image=os.path.join(execution_path, image_path),
                                                          output_image_path=os.path.join(execution_path, "image_new1.jpg"),
                                                          custom_objects=custom_objects, minimum_percentage_probability=65)

        if len(detections) > 0:
            return 1
        else:
            return 0
    except Exception as e:
        print(logger.get_exception())
        print(e)
        raise
