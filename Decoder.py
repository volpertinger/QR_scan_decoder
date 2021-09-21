import sys

from pyzbar import pyzbar
import cv2
import os
import shutil
import time


def get_ext(file):
    file_str = str(file)
    if len(file_str) < 4:
        return False
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
    def __init__(self, master_dir, rename_dir, is_coping, sleep_time, iterations_count):
        self.master_dir = str(master_dir)
        self.rename_dir = str(rename_dir)
        self.folder = []
        self.is_coping = bool(is_coping)
        self.sleep_time = int(sleep_time)
        self.iterations_count = int(iterations_count)
        self.get_folder()
        if iterations_count == -1:
            self.is_need_to_stop = False
        else:
            self.is_need_to_stop = True

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
            os.rename(self.master_dir + str(file), self.master_dir + str(barcodeData) + get_ext(file))
            if self.is_coping:
                shutil.copy(self.master_dir + str(barcodeData) + get_ext(file), self.rename_dir)
                print('copied: ' + self.rename_dir + str(barcodeData) + get_ext(file))
            else:
                shutil.move(self.master_dir + str(barcodeData) + get_ext(file), self.rename_dir)
                print('moved: ' + self.rename_dir + str(barcodeData) + get_ext(file))

    def get_folder(self):
        # это генератор и повторно из него данные не получить, поэтому сохраним в переменную
        # каждый элемент обхода будет содержать 3 элемента:
        # [Адрес каталога] [Список поддиректорий первого уровня] [Список файлов]
        tree = os.walk(self.master_dir)
        for i in tree:
            self.folder.append(i)

    def start(self):
        if not self.is_need_to_stop:
            while not self.is_need_to_stop:
                for address, dirs, files in self.folder:
                    for file in files:
                        self.decode_move(file)
                print('go to sleep for ' + str(self.sleep_time) + 'secs on endless iterations')
                time.sleep(self.sleep_time)

        else:
            for i in range(self.iterations_count):
                for address, dirs, files in self.folder:
                    for file in files:
                        self.decode_move(file)
                if i == self.iterations_count - 1:
                    break
                print('go to sleep for ' + str(self.sleep_time) + ' secs on iteration ' + str(i + 1))
                time.sleep(self.sleep_time)
        print('finished all ' + str(self.iterations_count) + ' iterations')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('{Master directory} {Rename directory} {is_coping} {sleep_time}')
        print('commands: help')
        exit(1)
    if len(sys.argv) == 2 and sys.argv[1] == 'help':
        print('Master directory - directory where scanning')
        print('Rename_directory - directory with renamed files')
        print('is_coping: if True, files are coping. If False, files are moving')
        print('sleep_time - time in secs. Scanning loop iteration every sleep_time')
        print('iteration_count - count of scanning iterations. If == -1 - infinite iterations')
        exit(1)
    if len(sys.argv) == 6:
        decoder = ScanDecoder(sys.argv[1], sys.argv[2], bool(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]))
        decoder.start()
        exit(0)
    print('wrong input\ntype "help" to see commands')
    exit(2)
