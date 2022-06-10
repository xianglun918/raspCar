import cv2
import os
import logging


class ObjDetector:

    def __init__(self, model_file: str = "./haarcascade_models/haarcascade_frontalface_default.xml"):
        model_file = os.path.realpath(model_file)
        self._verify_file(model_file)
        self._model_file = model_file
        self._model = cv2.CascadeClassifier(self._model_file)

    def update_model(self, model_file):
        model_file = os.path.realpath(model_file)
        self._verify_file(model_file)
        self._model_file = model_file
        self._model = cv2.CascadeClassifier(self._model_file)

    def detect_objects(self, gray_image):
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
    plt.title('Original')
    plt.subplot(1, 2, 2)
    plt.imshow(imutils.opencv2matplotlib(roi))
    plt.title('Detected')

    print(result)
    while 1:
        cv2.imshow('Result', roi)
        cv2.imshow('Original', img)

        k = cv2.waitKey(1) & 0xff
        if k == 27:
            # cv2.imwrite("canny_test_future.jpg", result)
            break
    cv2.destroyAllWindows()
