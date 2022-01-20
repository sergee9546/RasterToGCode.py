Simple utility to convert raster images into G-code for  laser engraving purpose.
It's no vectorise of image, but only provide "pixel to dot" transfer.
Suitable to hardware that have not ability to work with raster images at all.

Simple GUI is provided.

Installation:

pip install PIL

How to use:  Run script, select file to be processed. Resize your image if needed.
Use Margins to compensate
stat/stop velocities. Set up a proper size of pixel. Dont use a big images,
because engraving time is too high on it.

Простая утилита для перевода растровой графики в G код для лазерных станков с чпу.
Тупо поточечно переводит изображение в G-код. Используется для станков,
которые не умеют принимать для обработки изображения от природы.
Запустите скрипт, выберите изображение, измените его размеры если надо.
Для компенсации эффектов разгона/торможения используйте опцию "Использовать поля".
Большие изображения гравируются очень долго. Не стоит брать размер более 250х250.

Установите пакет PIL

pip install PIL

