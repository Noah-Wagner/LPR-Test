import os
import sys

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit

base_directory = r"N:\User\NAWagner\LPR\Curated"
directory = os.fsencode(base_directory)


def get_image_list():
    image_files = []
    for folder_name in os.listdir(directory):
        folder_name = os.fsdecode(folder_name)
        if folder_name.endswith(".db"):
            continue
        folder_path = os.path.join(base_directory, folder_name)
        for image_name in os.listdir(folder_path):
            if image_name.endswith('.jpg'):
                image_files.append(os.path.join(folder_path, image_name))
    return image_files


def get_plate(file):
    return file[file.rfind('_') + 1:file.rfind('.')]


def new_file_name(file_path, new_lp):
    file_path = file_path[:1 - len(file_path) + file_path.rfind('_')] + new_lp + file_path[
                                                                                 file_path.rfind('.') - len(file_path):]
    return file_path


def get_percent(completed, total):
    return "{0:.2f}".format(100 * completed / total) + '%'


class LPChecker(QWidget):
    image_idx = 298

    def __init__(self):
        super().__init__()
        self.title = 'License Plate Checker'
        self.setWindowTitle(self.title)
        self.resize(1100, 570)
        self.move(300, 300)

        print("Getting image list...")
        self.image_list = get_image_list()
        print("Image list retrieved!")

        self.image_view = QLabel(self)
        self.pixmap = QPixmap(self.image_list[self.image_idx])
        self.image_view.setPixmap(self.pixmap)

        self.lp_view = QLabel(self)
        self.lp_view.setText(get_plate(self.image_list[self.image_idx]))
        self.lp_view.move(920, 20)
        self.lp_view.resize(200, 20)

        self.completion = QLabel(self)

        self.completion.setText(get_percent(self.image_idx, len(self.image_list)))
        self.completion.move(920, 120)

        self.textbox = QLineEdit(self)
        self.textbox.move(870, 80)

        button = QPushButton("Yes", self)
        button.setToolTip("Match")
        button.move(850, 50)
        button.clicked.connect(self.on_yes)

        button = QPushButton("No", self)
        button.setToolTip("Doesn't match")
        button.move(940, 50)
        button.clicked.connect(self.on_no)

        self.show()

    def next_pic(self):
        self.image_idx += 1
        self.pixmap = QPixmap(self.image_list[self.image_idx])
        self.image_view.setPixmap(self.pixmap)
        self.lp_view.setText(get_plate(self.image_list[self.image_idx]))
        self.completion.setText(get_percent(self.image_idx, len(self.image_list)))

    @pyqtSlot()
    def on_yes(self):
        self.next_pic()

    @pyqtSlot()
    def on_no(self):
        if len(self.textbox.text()) < 4:
            print("Text not long enough!")
            return
        new_fp = new_file_name(self.image_list[self.image_idx], self.textbox.text())
        try:
            os.rename(self.image_list[self.image_idx], new_fp)
        except OSError as e:
            os.remove(self.image_list[self.image_idx])
        self.textbox.clear()
        self.next_pic()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = LPChecker()

    sys.exit(app.exec_())
