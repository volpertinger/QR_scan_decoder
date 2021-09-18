from pyzbar import pyzbar
import cv2
import os
import shutil
import time


def get_ext(file):
    file_str = str(file)
    if len(file_str) < 4:
        return
    return file_str[len(file_str) - 4:len(file_str)]


def is_correct_file(file):
    file_str = str(file)
    if len(file_str) < 4:
        return False
    file_ext = get_ext(file)
    if not (file_ext == '.jpg' or file_ext == '.png'):
        return False
    return True


class ScanDecoder:
    def __init__(self, master_dir, rename_dir, is_coping=False, sleep_time=300):
        self.master_dir = master_dir
        self.rename_dir = rename_dir
        self.folder = []
        self.is_coping = is_coping
        self.is_need_to_stop = False
        self.sleep_time = sleep_time
        self.get_folder()

    def decode_move(self, file):
        if not is_correct_file(file):
            return
            # загружаем нужную картинку
        image = cv2.imread(self.master_dir + str(file))

        # Находим qr коды в изображении и декодируем их (а вдруг сразу много в одной картинке)
        barcodes = pyzbar.decode(image)
        # цикл по всем qr кодам
        for barcode in barcodes:
            barcodeData = barcode.data.decode("utf-8")
            if self.is_coping:
                shutil.copyfile(self.master_dir + str(file), self.rename_dir + str(barcodeData) + get_ext(file))
            else:
                shutil.move(self.master_dir + str(file), self.rename_dir + str(barcodeData) + get_ext(file))

    def get_folder(self):
        # это генератор и повторно из него данные не получить, поэтому сохраним в переменную
        # каждый элемент обхода будет содержать 3 элемента:
        # [Адрес каталога] [Список поддиректорий первого уровня] [Список файлов]
        tree = os.walk(self.master_dir)
        for i in tree:
            self.folder.append(i)

    def start(self):
        while not self.is_need_to_stop:
            for address, dirs, files in self.folder:
                for file in files:
                    self.decode_move(file)
            time.sleep(self.sleep_time)


if __name__ == '__main__':
    directory_master = 'Test/'
    directory_renamed = 'Renamed/'
    decoder = ScanDecoder(directory_master, directory_renamed, True)
    decoder.start()
