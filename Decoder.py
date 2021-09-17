from pyzbar import pyzbar
import cv2
import os

if __name__ == '__main__':

    directory = 'Test/'
    # загружаем нужную картинку
    image = cv2.imread("Test/test_pdf-1.png")

    # Находим qr коды в изображении и декодируем их (а вдруг сразу много в одной картинке)
    barcodes = pyzbar.decode(image)
    # цикл по всем qr кодам
    for barcode in barcodes:
        barcodeData = barcode.data.decode("utf-8")
        print(barcodeData)
