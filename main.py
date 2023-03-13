# pyuic5 main_window.ui -o main_window_ui.py
# import os
# from ctypes import windll
from PyQt6.QtWidgets import QMainWindow, QApplication, QFileDialog, QMenu
from PyQt6.QtCore import QStandardPaths  # , QFile, QFileInfo, Qt
from PyQt6.QtGui import QPixmap, QCursor, QAction
from main_window_ui import Ui_MainWindow
import params
import logging

logging.basicConfig(level=logging.DEBUG)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Create an instance of the UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # # ДАЛЕЕ ИДЕТ ОСТАЛЬНОЙ КОД:
        # инициируем переменную для записи пути к файлу фото
        self.image_file_path = None
        # инициируем переменную для хранения объекта фото
        self.pil_image = None
        # инициируем объект для встраивания в интерфейс
        # self.image_pixmap = None
        # Find the "Open File" button and connect its clicked signal to a function
        self.ui.pb_open.clicked.connect(self.load_picture)
        # определим значения для параметров по умолчанию
        self.clear_values()

        # определим папку с изображениями по умолчанию
        self.default_folder_location = QStandardPaths.standardLocations(
            QStandardPaths.StandardLocation.PicturesLocation)
        # определяем кнопку проверки
        self.ui.pb_check.clicked.connect(self.check)
        # инициализируем контекстное меню
        self.ui.image_label.customContextMenuRequested.connect(self.show_context_menu)

        # # выполнение после закрытия окна программы
        # self.closeEvent = self.close_event

    def update_viewer_size(self):
        if self.ui.image_label.width() < self.ui.image_label.height():
            self.ui.image_label.setFixedSize(self.ui.image_label.width(), self.ui.image_label.width())
        else:
            self.ui.image_label.setFixedSize(self.ui.image_label.height(), self.ui.image_label.height())

    def load_picture(self):
        # self.default_folder_location[0]
        source_file, _ = QFileDialog.getOpenFileName(self, "Открыть фотографию в формате JPG",
                                                     "materials/",
                                                     "Формат JPG (*.jpg)")
        if source_file:
            self.clear_values()
            # обновить размер окна просмотра
            self.update_viewer_size()
            # создаем объект изображения
            image_pil = params.get_image_object(source_file)
            # image_qt = params.get_image_qt(image_pil)
            image_qt = params.get_image_qt(image_pil)
            image_pixmap = QPixmap.fromImage(image_qt).copy()
            # выводим изображение на экран
            self.ui.image_label.setPixmap(image_pixmap)
            # делаем кнопку проверить активной
            self.ui.pb_check.setEnabled(True)
            # записываем пути для файла изображения
            self.image_file_path = source_file
            self.pil_image = image_pil
            # self.image_pixmap = image_pixmap
            # выводим сообщение в статус бар
            self.ui.statusbar.showMessage('Загружена фотография', 5000)
        else:
            print('error')

    def clear_values(self):
        # определим значения для параметров по умолчанию
        self.ui.v_foto_height.setText('')
        self.ui.p_foto_height.clear()
        self.ui.v_foto_width.setText('')
        self.ui.p_foto_width.clear()
        self.ui.v_ratio.setText('')
        self.ui.p_ratio.clear()
        self.ui.v_file_size.setText('')
        self.ui.p_file_size.clear()
        self.ui.v_res_h.setText('')
        self.ui.p_res_h.clear()
        self.ui.v_res_v.setText('')
        self.ui.p_res_v.clear()
        self.ui.v_head_top.setText('')
        self.ui.p_head_top.clear()
        self.ui.v_head_down.setText('')
        self.ui.p_head_down.clear()
        self.ui.v_head_size.setText('')
        self.ui.p_head_size.clear()
        self.ui.v_eye_line.setText('')
        self.ui.p_eye_line.clear()
        self.ui.v_eye_h.setText('')
        self.ui.p_eye_h.clear()
        self.ui.v_eye_open.setText('')
        self.ui.p_eye_open.clear()
        self.ui.v_red_eye.setText('')
        self.ui.p_red_eye.clear()
        self.ui.v_head_tilt_turn.setText('')
        self.ui.p_head_tilt_turn.clear()
        self.ui.v_face_in_centre.setText('')
        self.ui.p_face_in_centre.clear()
        self.ui.v_is_shadows.setText('')
        self.ui.p_is_shadows.clear()
        self.ui.v_foto_frmt.setText('')
        self.ui.p_foto_frmt.clear()
        self.ui.v_icc.setText('')
        self.ui.p_icc.clear()
        self.ui.v_color_depth.setText('')
        self.ui.p_color_depth.clear()
        self.ui.v_back_is_even.setText('')
        self.ui.p_back_is_even.clear()
        self.ui.v_neutral_color.setText('')
        self.ui.p_neutral_color.clear()
        self.ui.v_is_light.setText('')
        self.ui.p_is_light.clear()
        self.ui.v_is_changed.setText('')
        self.ui.p_is_changed.clear()
        self.ui.v_foto_date.setText('')
        self.ui.p_foto_date.clear()
        self.ui.v_is_correct_filename.setText('')
        self.ui.p_is_correct_filename.clear()
        self.ui.v_compression_ratio.setText('')
        self.ui.p_compression_ratio.clear()

    def set_image(self):
        # Convert the PIL image to a QPixmap and set it as the label's pixmap
        qt_img = params.get_image_qt(self.pil_image)
        pix_image = QPixmap.fromImage(qt_img)

        self.ui.image_label.setPixmap(pix_image.copy())

    def rotate_right(self):
        # pil_img = self.pil_image
        # Rotate the image by 90 degrees
        self.pil_image = self.pil_image.rotate(-90)
        # self.pil_image.save('1.jpg')
        self.set_image()
        self.ui.statusbar.showMessage('Изображение повернуто по часовой стрелке', 2000)
        logging.debug('Изображение повернуто на 90 градусов')

    def rotate_left(self):
        pil_img = self.pil_image
        pil_img = pil_img.rotate(90.0)
        image_qt = params.get_image_qt(pil_img)
        image_pixmap = QPixmap.fromImage(image_qt).copy()
        # выводим изображение на экран
        self.ui.image_label.setPixmap(image_pixmap)
        self.pil_image = pil_img
        self.ui.statusbar.showMessage('Изображение повернуто против часовой стрелки', 2000)
        logging.debug('Изображение повернуто на --90 градусов')

    def rotate_horizontal(self):
        pil_img = self.pil_image
        pil_img = params.get_mirror_image(pil_img)
        image_qt = params.get_image_qt(pil_img)
        image_pixmap = QPixmap.fromImage(image_qt).copy()
        # выводим изображение на экран
        self.ui.image_label.setPixmap(image_pixmap)
        self.pil_image = pil_img
        self.ui.statusbar.showMessage('Изображение зеркально отражено', 2000)
        logging.debug('Изображение зеркально отражено')

    def rotate_vertical(self):
        pil_img = self.pil_image
        pil_img = pil_img.rotate(180.0)
        image_qt = params.get_image_qt(pil_img)
        image_pixmap = QPixmap.fromImage(image_qt).copy()
        # выводим изображение на экран
        self.ui.image_label.setPixmap(image_pixmap)
        self.pil_image = pil_img
        self.ui.statusbar.showMessage('Изображение повернуто', 2000)
        logging.debug('Изображение повернуто на 180 градусов')

    def show_context_menu(self):
        if self.image_file_path is None:
            return

        menu = QMenu(self)

        turn_right = QAction('Повернуть по часовой', self)
        turn_right.triggered.connect(self.rotate_right)
        menu.addAction(turn_right)

        turn_left = QAction('Повернуть против часовой', self)
        turn_left.triggered.connect(self.rotate_left)
        menu.addAction(turn_left)

        turn_horizontal = QAction('Зеркально отразить', self)
        turn_horizontal.triggered.connect(self.rotate_horizontal)
        menu.addAction(turn_horizontal)

        turn_vertical = QAction('Перевернуть', self)
        turn_vertical.triggered.connect(self.rotate_vertical)
        menu.addAction(turn_vertical)

        # # Map the position to global coordinates
        # global_pos = self.mapToGlobal(pos)
        # print(global_pos)
        # # Show the context menu at the global position
        menu.exec(QCursor.pos())

    def get_check(self, function, p_par, v_par, suffix: str = ''):
        # function = params.image_height(image_object)
        # parameter = "foto_height"
        # suffix: str = ""
        # инициализация изображений проверки
        # self.pixmap_true = QPixmap('true.svg')
        # self.pixmap_false = QPixmap('false.svg')

        answer, value = function
        # print(answer, value) # True 600
        if answer:
            p_par.setPixmap(QPixmap('res/true.svg'))
        elif answer is None:
            p_par.setPixmap(QPixmap('res/warn.svg'))
        else:
            p_par.setPixmap(QPixmap('res/false.svg'))
        v_par.setText(value + ' ' + suffix)

    def check(self):
        # определяем объект изображения
        ui = self.ui
        img_obj = self.pil_image
        img_path = self.image_file_path
        chk = self.get_check
        # print(self.image_file)
        self.ui.statusbar.showMessage("Нажата кнопка 'Проверить'", 2000)

        chk(params.image_width(img_obj), ui.p_foto_width, ui.v_foto_width, 'px')
        chk(params.image_height(img_obj), ui.p_foto_height, ui.v_foto_height, 'px')
        chk(params.get_aspect_ratio(img_obj), ui.p_ratio, ui.v_ratio)
        chk(params.file_size(img_path), ui.p_file_size, ui.v_file_size, 'Kb')
        chk(params.image_format(img_obj), ui.p_foto_frmt, ui.v_foto_frmt)
        chk(params.icc_profile(img_obj), ui.p_icc, ui.v_icc)
        chk(params.image_color_depth(img_obj), ui.p_color_depth, ui.v_color_depth, 'bit')
        chk(params.file_date(img_path), ui.p_foto_date, ui.v_foto_date)
        chk(params.compression_ratio(img_path, img_obj), ui.p_compression_ratio, ui.v_compression_ratio, '')
        chk(params.is_valid_filename(img_path), ui.p_is_correct_filename, ui.v_is_correct_filename, '')


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


"""
destination_file = "/".join(source_file.split('/')[:-1])
# Load the picture at the specified location
destination_file = destination_file + '/temp'
# print(destination_file)
try:
    os.remove(destination_file)
except FileNotFoundError:
    logging.log(1, 'файла нет')
# Copy the file as hidden
QFile.copy(source_file, destination_file)
windll.kernel32.SetFileAttributesW(destination_file, 2)
#  os.flags(destination_file, os.stat(destination_file).st_flags | 0x00000002)
        
# def close_event(event):
#     # Delete the file when the window is closed
#     os.remove(self.image_file)
#     event.accept()
"""
