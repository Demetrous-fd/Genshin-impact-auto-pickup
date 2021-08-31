from pyautogui import getActiveWindowTitle, getWindowsWithTitle
from directinput import PressKey, ReleaseKey
from PySide2.QtCore import QThread, Slot, Signal
from PySide2.QtWidgets import QApplication
from ScanKeys import get_code, get_key
from random import random
from PIL import ImageGrab
from pathlib import Path
import numpy as np
import time
import cv2

PATH = Path(__file__).parent.absolute()
PATH_NAMES = Path(PATH, r"model\classes.names")
PATH_WEIGHTS = Path(PATH, r"model\gi_actions.weights")
PATH_MODEL_CFG = Path(PATH, r"model\yolov4-tiny.cfg")

CONFIDENCE_THRESHOLD = 0.2
NMS_THRESHOLD = 0.4

COLORS = {
    0: (255, 203, 203),
    1: (70, 70, 150),
    2: (100, 180, 0),
    3: (0, 180, 120),
    4: (0, 80, 200),
    5: (180, 70, 100),
    6: (200, 0, 170),
    7: (255, 203, 203),
    8: (70, 70, 150),
    9: (100, 180, 0),
    10: (0, 180, 120),
    11: (0, 80, 200),
    12: (180, 70, 100),
    13: (200, 0, 170)
}


class Model:
    def __init__(self, path_weights: Path or str = PATH_WEIGHTS, path_cfg: Path or str = PATH_MODEL_CFG,
                 path_names: Path or str = PATH_NAMES, colors_names=None,
                 dnn_target: str = "CPU"):
        if colors_names is None:
            colors_names = COLORS
        self.__path_weights = str(path_weights)
        self.__path_cfg = str(path_cfg)

        self.__net = self.__get_net(self.__path_weights, self.__path_cfg)
        self.__model = self.__get_model(self.__net)
        self.__set_dnn_target(dnn_target)

        with open(path_names) as f:
            self.classes_name = {index: cname.strip() for index, cname in enumerate(f.readlines())}
        self.classes_color = colors_names

        print(f"Model init, DNN_Target: {dnn_target}")

    def __get_net(self, weights, cfg):
        return cv2.dnn.readNet(weights, cfg)

    def __get_model(self, net):
        model = cv2.dnn_DetectionModel(net)
        model.setInputParams(size=(416, 416), scale=1 / 255, swapRB=True)
        return model

    def __set_dnn_target(self, dnn_target: str):
        if dnn_target.lower() == "cpu":
            self.__model.setPreferableBackend(cv2.dnn.DNN_BACKEND_DEFAULT)
            self.__model.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
        elif dnn_target.lower() == "cuda":
            self.__model.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
            self.__model.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
        elif dnn_target.lower() == "opencl":
            self.__model.setPreferableTarget(cv2.dnn.DNN_TARGET_OPENCL)
        else:
            raise ValueError(f"Target: {dnn_target} is not exists")

    def set_dnn_target(self, dnn_target: str):
        self.__set_dnn_target(dnn_target)

    def detect(self, frame, conf_threshold: float = .2, nms_threshold: float = .4):
        classes, scores, boxes = self.__model.detect(frame, conf_threshold, nms_threshold)
        return classes, scores, boxes

    def find_class(self, classes: tuple, current_class: str or int):
        if isinstance(current_class, int):
            return True if current_class in classes else False

        elif isinstance(current_class, str):
            classes = [self.classes_name[class_name[0]] for class_name in classes]
            return True if current_class in classes else False

        else:
            raise ValueError("current_class should be str or int")

    def draw_bbox(self, frame, detect):
        classes, scores, boxes = detect

        for (classid, score, box) in zip(classes, scores, boxes):
            color = self.classes_color[int(classid)]
            label = f"{self.classes_name[classid[0]]}"

            cv2.rectangle(frame, box, color, 3)
            cv2.rectangle(frame, (box[0] - 2, box[1] - 36, 13 * len(label), 36), color, -1)
            cv2.putText(frame, label, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, .7, (0, 0, 0), 2)

        return frame


class CaptureLoop:
    def __init__(self, model: Model, config, show_capture: bool = False, app_title: str = "Genshin Impact"):
        self.__model = model
        self.__frame_rate = 1000 // config["FPS"] if config["FPS"] != 0 else 0
        self.__click_rate = config["Click rate"]
        self.__key = get_code(config["Key"]) if isinstance(config["Key"], str) else config["Key"]
        self.__app_title = app_title
        self.__show_capture = show_capture

        print(f"CaptureLoop init, FPS: {config['FPS']}, Click rate: {config['Click rate']}, Key: {get_key(self.__key)}")

    def run(self):
        fps = 0
        fps_count = 0
        pickup_counter = 0
        counter1 = time.perf_counter()
        counter2 = time.perf_counter()

        while 1:
            if getActiveWindowTitle() == self.__app_title:
                if (time.perf_counter() - counter1) * 1000 >= self.__frame_rate:
                    start = time.time()

                    fps_count += 1
                    bbox = get_actions_rect(self.__app_title)
                    frame = get_frame(bbox)
                    classes, scores, boxes = self.__model.detect(frame)

                    if self.__model.find_class(classes, "selected_item"):
                        print(f"Find selected item, time spend: {time.time() - start:.3f} ms")
                        start_pickup = time.time()
                        pickup_item(self.__key, self.__click_rate)
                        pickup_counter += 1
                        print(f"#{pickup_counter} Pickup item, time spend: {time.time() - start_pickup:.3f} ms")

                    if self.__show_capture:
                        frame = self.__model.draw_bbox(frame, (classes, scores, boxes))
                        frame = cv2.putText(frame, f"FPS: {fps}", (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

                        show_frame(frame)

                    counter1 = time.perf_counter()

                if (time.perf_counter() - counter2) * 1000 >= 10000 and self.__show_capture:
                    fps = fps_count
                    fps_count = 0
                    counter2 = time.perf_counter()
            else:
                time.sleep(1)


class QCaptureLoop(QThread):
    sendEvent = Signal(object)

    def __init__(self, parent, model: Model, config,
                 app_title: str = "Genshin Impact", show_capture: bool = False):
        super(QCaptureLoop, self).__init__(parent)

        self.__model = model
        self.__frame_rate = 1000 // config["FPS"] if config["FPS"] != 0 else 0
        self.__click_rate = config["Click rate"]
        self.__key = get_code(config["Key"]) if isinstance(config["Key"], str) else config["Key"]
        self.__app_title = app_title

        self.__show_capture = show_capture
        self.__isRunning = True
        self.__disable = False
        self.__cap = True

        self.sendEvent.connect(Slot())

        print(f"QCaptureLoop init, FPS: {config['FPS']}, Click rate: {config['Click rate']}, Key: {get_key(self.__key)}")

    @Slot()
    def switchHandler(self, data):
        if data == "Enable":
            self.__disable = False
        else:
            self.__disable = True

    @Slot()
    def updateHandler(self, data):
        key = data[0]
        value = data[1]
        if key == "Target":
            self.__model.set_dnn_target(value)
        elif key == "Click rate":
            self.__click_rate = value
        elif key == "FPS":
            self.__frame_rate = 1000 // value if value != 0 else 0
        elif key == "Key":
            self.__key = value

    def stop(self):
        self.__isRunning = False

    def __gicap(self):
        if self.__cap:
            self.sendEvent.emit("Genshin impact is captured")
            self.__cap = False

    def run(self):
        fps = 0
        fps_count = 0
        pickup_counter = 0
        counter1 = time.perf_counter()
        counter2 = time.perf_counter()

        while self.__isRunning:
            QApplication.processEvents()

            if getActiveWindowTitle() == self.__app_title and not self.__disable:
                self.__gicap()
                if (time.perf_counter() - counter1) * 1000 >= self.__frame_rate:
                    start = time.time()
                    fps_count += 1
                    bbox = get_actions_rect(self.__app_title)
                    frame = get_frame(bbox)
                    classes, scores, boxes = self.__model.detect(frame)

                    if self.__model.find_class(classes, "selected_item"):
                        print(f"Find selected item, time spend: {time.time() - start:.3f} ms")
                        start_pickup = time.time()
                        pickup_item(self.__key, self.__click_rate)
                        pickup_counter += 1
                        print(f"#{pickup_counter} Pickup item, time spend: {time.time() - start_pickup:.3f} ms")
                        self.sendEvent.emit(f"Pickup counter: {pickup_counter}")

                    if self.__show_capture:
                        frame = self.__model.draw_bbox(frame, (classes, scores, boxes))
                        frame = cv2.putText(frame, f"FPS: {fps}", (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

                        show_frame(frame)

                    counter1 = time.perf_counter()

                if (time.perf_counter() - counter2) * 1000 >= 1000 and self.__show_capture:
                    fps = fps_count
                    fps_count = 0
                    counter2 = time.perf_counter()

            else:
                QThread.msleep(1000)
                self.__cap = True


def get_actions_rect(app):
    hwnd = getWindowsWithTitle(app)[0]
    centerx, centery = hwnd.center

    x1 = centerx + centerx // 8 if hwnd.left <= 0 else (centerx - hwnd.left) + (centerx - hwnd.left) // 8 + hwnd.left
    y1 = centery - centery // 2.5
    x2 = centerx + centerx // 1.75 if hwnd.left <= 0 else (centerx - hwnd.left) + (centerx - hwnd.left) // 1.75 + hwnd.left
    y2 = centery + centery // 2.5

    return x1, y1, x2, y2


def get_frame(bbox):
    frame = ImageGrab.grab(bbox, all_screens=True)
    frame = np.array(frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    return frame


def pickup_item(key: int, rate_mode: str):
    PressKey(key)

    if rate_mode == "Normal":
        sleep = float(f"{random() / 10:.3f}")
        sleep = int(sleep * 1000 if sleep > 0.1 else (0.1 - sleep) * 1000)
        QThread.msleep(sleep if sleep > 50 else 125 - sleep)

    elif rate_mode == "Fast":
        sleep = float(f"{random() / 10:.3f}")
        QThread.msleep(int(sleep * 1000 if sleep > 0.05 else (0.07 - sleep) * 1000))

    ReleaseKey(key)


def show_frame(frame):
    cv2.imshow("", frame)
    cv2.waitKey(1)
