from captureloop import Model, CaptureLoop
from ui_main import MainWindow
from config import read_config
from PySide2 import QtWidgets
import argparse
import sys


parser = argparse.ArgumentParser(description="Extra options")
parser.add_argument("-show-capture", action="store_const", default=False, const=True, help="Show capture frames")
parser.add_argument("-console", action="store_const", default=False, const=True, help="Start auto pickup on console")

if __name__ == '__main__':
    args = parser.parse_args()

    if args.console:
        config = read_config()
        model = Model(dnn_target=config["Target"])
        loop = CaptureLoop(model, config, show_capture=args.show_capture)
        
    else:
        app = QtWidgets.QApplication([])
        main = MainWindow(None, show_capture=args.show_capture)
        sys.exit(app.exec_())
