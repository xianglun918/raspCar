import cv2
import os
import logging

from os.path import dirname

_DEFAULT_MODEL_FILE = os.path.join(dirname(__file__), "haarcascade_models/haarcascade_frontalface_default.xml")


class ObjDetector:

    def __init__(self, model_file: str = _DEFAULT_MODEL_FILE):
        model_file = os.path.realpath(model_file)
        self._verify_file(model_file)
        self._model_file = model_file
        self._model = cv2.CascadeClassifier(self._model_file)

    def update_model(self, model_file: str):
        """
        Update the model used by ObjDetector as a Haar Cascade Classifier.

        Args:
            model_file: str
                The path to the model file used. (xml structure file expected.)

        Returns:
            None
        """
        model_file = os.path.realpath(model_file)
        self._verify_file(model_file)
        self._model_file = model_file
        self._model = cv2.CascadeClassifier(self._model_file)

    def detect_objects(self, gray_image):
        """Detect the objects within input gray-scale image."""
        try:
            objects = self._model.detectMultiScale(gray_image)
        except Exception as e:
            logging.error("is the input a gray-scale image?")
            raise e

        return objects

    @staticmethod
    def _verify_file(file_path):
        if not os.path.isfile(file_path):
            logging.error("model file not exist, update failed.")
            raise FileNotFoundError(f"file: `{file_path}` not found")


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import imutils

    my_detector = ObjDetector()
    img = cv2.imread(os.path.realpath('../assets/images/that_girl.jpg'))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    print(type(gray), len(gray), len(gray[0]))
    result = my_detector.detect_objects(gray)
    (x, y, w, h) = result[0]
    roi = img[y:y + h, x:x + w]
    plt.figure(figsize=(400, 300), dpi=300)
    plt.subplot(1, 2, 1)
    plt.imshow(imutils.opencv2matplotlib(img))
    plt.subplot(1, 2, 2)
    plt.imshow(imutils.opencv2matplotlib(roi))
    print("detected x, y, w, h is: ", result)
    while 1:
        cv2.imshow('Result, Press <esc> to exit', roi)
        cv2.imshow('Original, Press <esc> to exit', img)

        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break
    cv2.destroyAllWindows()
