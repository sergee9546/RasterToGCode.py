import tkinter as tk
from tkinter import Tk, ttk, Button, Label, IntVar, StringVar, Canvas
from tkinter import messagebox, Scale, DoubleVar
from tkinter import filedialog as fd
from PIL import Image, ImageTk, ImageOps


class GUI:

    def __init__(self, window):

        self.window = window
        window.title('Pixelizer')
        window.geometry('600x450')
        window.resizable(False, False)

        window.columnconfigure(0, weight=3)
        window.columnconfigure(1, weight=3)
        window.columnconfigure(2, weight=4)
        window.columnconfigure(3, weight=4)

        window.rowconfigure(0, weight=1)
        window.rowconfigure(1, weight=1)
        window.rowconfigure(2, weight=1)
        window.rowconfigure(3, weight=1)
        window.rowconfigure(4, weight=1)
        window.rowconfigure(5, weight=1)
        window.rowconfigure(6, weight=1)
        window.rowconfigure(7, weight=1)

        self.MarginsVariable = tk.IntVar()
        self.ResizeVariable = tk.IntVar()
        self.InvertVariable = tk.IntVar()
        self.EntryVariable = tk.StringVar()
        self.InitialFilenameButton = ttk.Button(
            window, text='Исходный файл')
        self.InitialFilenameLabel = ttk.Label(window, text='')
        self.Resize_Check_Button = tk.Checkbutton(
            window, text='Изменить размер, в пикселях',
            variable=self.ResizeVariable,
            onvalue=True, offvalue=False, command=self.Resize)
        self.Invert_Check_Button = tk.Checkbutton(
             window, text='Инвертировать изображение',
             variable=self.InvertVariable,
             onvalue=True, offvalue=False, command=self.Invert)
        self.Invert_Check_Button_Label = ttk.Label(window, text='Нет')
        self.ResizeX = ttk.Label(window, width=10, state='disabled')
        self.ResizeY = ttk.Label(window, width=10, state='disabled')
        self.ResizeScale = tk.Scale(window, orient='horizontal', resolution=1,
                                    from_=1, to=100, command=self.Scaled)
        self.Margins_Check_Button = tk.Checkbutton(
             window, text='Иcпользовать поля',
             variable=self.MarginsVariable,
             onvalue=True, offvalue=False, command=self.Margins)
        self.Margins_Check_Button_Label = ttk.Label(window, text='Нет')
        self.SizeOfPixel = tk.Entry(window, width=10, state='normal')
        self.SizeOfPixel.insert(0, '0.2')
        self.SizeOfPixel_label = ttk.Label(window, text="Размер Пикселя,мм")
        self.SizeOfImage = ttk.Label(window, text="Размер изображения")
        self.Start_Button = ttk.Button(window, text='Запуск')

        self.InitialFilenameButton.grid(column=0, row=0,
                                        sticky=tk.W, padx=5, pady=5)
        self.Resize_Check_Button.grid(column=0, row=1,
                                      sticky=tk.W, padx=5, pady=5)
        self.Margins_Check_Button.grid(column=0, row=2,
                                       sticky=tk.W, padx=5, pady=5)
        self.Invert_Check_Button.grid(column=0, row=3,
                                      sticky=tk.W, padx=5, pady=5)
        self.SizeOfPixel_label.grid(column=0, row=4,
                                    sticky=tk.W, padx=5, pady=5)
        self.SizeOfImage.grid(column=0, row=5,
                              columnspan=2, sticky=tk.W, padx=5, pady=5)
        self.Start_Button.grid(column=0, row=6,
                               sticky=tk.W, padx=5, pady=5)
        self.InitialFilenameLabel.grid(column=1, row=0, columnspan=2,
                                       sticky=tk.W, padx=5, pady=5)
        self.ResizeScale.grid(column=1, row=1,
                              sticky=tk.N, padx=5, pady=1)
        self.Margins_Check_Button_Label.grid(column=1, row=2,
                                             sticky=tk.W, padx=5, pady=5)
        self.Invert_Check_Button_Label.grid(column=1, row=3, sticky=tk.W,
                                            padx=5, pady=5)
        self.ResizeX.grid(column=2, row=1, sticky=tk.W, padx=5, pady=5)
        self.ResizeY.grid(column=3, row=1, sticky=tk.W, padx=5, pady=5)
        self.SizeOfPixel.grid(column=1, row=4, sticky=tk.W, padx=5, pady=5)

        self.InitialFilenameButton.bind("<Button-1>",
                                        self.InitialFilenameButton_click)
        self.Start_Button.bind("<Button-1>", self.Start_Button_click)

    def InitialFilenameButton_click(self, event):
        filetypes = (
                    ('JPG', '*.jpg'),
                    ('Все типы', '*.*')
                    )
        self.Initial_filename = fd.askopenfilename(
            title='Открыть файл',
            initialdir='/',
            filetypes=filetypes)
        self.InitialFilenameLabel.config(text=self.Initial_filename)
        self.im = Image.open(self.Initial_filename)
        self.ResizeX.config(state='disabled', text=self.im.width)
        self.ResizeY.config(state='disabled', text=self.im.height)

        self.SizeOfImage.config(
            text='Размер Изображения: ' +
            str(round(self.im.width*float(self.SizeOfPixel.get()), 1)) +
            ' X ' +
            str(round(self.im.height*float(self.SizeOfPixel.get()), 1)))

        self.window.update()

        Canv_Width = self.window.grid_bbox(2, 1, 3, 6)[2]-10
        Canv_Height = self.window.grid_bbox(2, 1, 3, 6)[3]-10
        self.Preview_Canvas = Canvas(self.window, width=Canv_Width,
                                     height=Canv_Height)
        self.Preview_Canvas.grid(column=2, row=2, rowspan=5, columnspan=2,
                                 sticky=tk.SE, padx=10)
        self.Preview_Canvas.update()

        ratio = round(self.im.width/self.im.height, 1)

        if ratio > 1:
            new_width = Canv_Width
            new_height = int(new_width/ratio)
        else:
            new_height = Canv_Height
            new_width = int(new_height*ratio)
        size = (new_width, new_height)
        Preview = self.im.resize(size, 3)
        self.window.update()
        self.photo = ImageTk.PhotoImage(Preview, 3)

        self.Preview_Canvas.create_image(
            self.Preview_Canvas.winfo_reqwidth()/2,
            self.Preview_Canvas.winfo_reqheight()/2, image=self.photo)

        self.window.update()

    def Resize(self):
        if self.ResizeVariable.get() == 1:
            self.ResizeX.config(
                state='normal', text='Х= ' +
                str(round(self.im.width*self.ResizeScale.get()/100, 1)))
            self.ResizeY.config(
                 state='normal', text='Y= ' +
                 str(round(self.im.height*self.ResizeScale.get()/100, 1)))
        else:
            self.ResizeX.config(state='disabled', text=self.im.width)
            self.ResizeY.config(state='disabled', text=self.im.height)
            self.SizeOfImage.config(
                text='Размер Изображения: ' +
                str(round(self.im.width*float(self.SizeOfPixel.get()), 1)) +
                ' X ' +
                str(round(self.im.height*float(self.SizeOfPixel.get()), 1)))

    def Invert(self):

        if self.InvertVariable.get():
            self.Invert_Check_Button_Label.config(text='Да')
        else:
            self.Invert_Check_Button_Label.config(text='Нет')

    def Margins(self):

        if self.MarginsVariable.get():
            self.Margins_Check_Button_Label.config(text='Да')
        else:
            self.Margins_Check_Button_Label.config(text='Нет')

    def Scaled(self, event):

        self.scl = int(self.ResizeScale.get())
        self.X = int(round((self.im.width*self.scl)/100, 0))
        self.Y = int(round((self.im.height*self.scl)/100, 0))
        if self.ResizeVariable.get() == 1:
            self.ResizeX.config(state='normal', text='Х= ' + str(self.X))
            self.ResizeY.config(state='normal', text='Y= ' + str(self.Y))
            self.SizeOfImage.config(
                text='Размер Изображения: ' +
                str(round(self.X*float(self.SizeOfPixel.get()), 1)) +
                ' X ' + str(round(self.Y*float(self.SizeOfPixel.get()), 1)))
        else:
            self.ResizeX.config(state='disabled')
            self.ResizeY.config(state='disabled')
            self.SizeOfImage.config(
               text='Размер Изображения: ' +
               str(round(self.im.width*float(self.SizeOfPixel.get()), 1)) +
               ' X ' +
               str(round(self.im.height*float(self.SizeOfPixel.get()), 1)))

    def Start_Button_click(self, event):

        Destination_filename = fd.asksaveasfilename(
            title='Сохранить как',
            filetypes=(('LCC', '*.lcc'), ('nc', '*.nc')),
            initialdir='/')

        f = open(Destination_filename.replace('.lcc', '') + '.lcc', 'w')
# Определение финального размера изображения
        if self.ResizeVariable.get() == 1:
            self.Dim = (self.X, self.Y)
        elif self.ResizeVariable.get() == 0:
            self.Dim = (self.im.width, self.im.height)

# Проверка правильности ввода размера пиксела
# В поле должно быть что то введено,
# в строке должны быть только цифры, за исключением разделителя(точка)

        if len(self.SizeOfPixel.get()) != 0 \
           and self.SizeOfPixel.get().replace('.', '', 1).isdigit()\
                and self.SizeOfPixel.get()[1] == '.'\
                and float(self.SizeOfPixel.get()) != 0:

            PixelSize = float(self.SizeOfPixel.get())

        else:

            Message = tk.messagebox.showwarning(
                'Ошибка Ввода', 'Неккоректный ввод размера пиксела')
            Message.grid(column=1, row=2, sticky=tk.W, padx=5, pady=5)

# Учет оффсета

        if self.MarginsVariable.get() == 1:
            Offset = 25
        else:
            Offset = 0

        # Изменение размеров изображения
        b = self.im.resize(self.Dim, 1)

        if self.InvertVariable.get() == 1:
            c1 = PIL.ImageOps.invert(b)
        else:
            c1 = b

        c = c1.convert("1")
        Bitmap = []
        Stroka = []
        d = c
        Height = self.Dim[1]
        Width = self.Dim[0]

        for y in range(0, Height):
            for x in range(0, Width):
                Stroka.append(c.getpixel((x, y)))
            Bitmap.append(Stroka)
            Stroka = []

        # Программы лазерного раскроя не принимают точку
        #  в качестве рабочего примитива. Используем вместо неё
        #  линию с малой длиной Pix
        Pix = 0.05
        #  Открываем файл на запись,
        # объявляем рабочими единицами измерения миллиметры.
        f.write('G21' + '\n')

        for y in range(0, len(Bitmap)):
            # для четных строк проход слева на право
            if y % 2 == 0:
                # Прорисовка полей слева
                f.write('G00 ' + 'X0' + ' Y' +
                        str(Height*PixelSize-y*PixelSize) + '\n')
                f.write('G01 ' + 'X0.05' + ' Y' +
                        str(Height*PixelSize-y*PixelSize) + '\n')

                # Прорисовка строки
                for x in range(0, len(Bitmap[0])):
                    if Bitmap[y][x] == 0:
                        f.write('G00 ' + 'X' +
                                str(round(x*PixelSize + Offset*PixelSize, 4)) +
                                ' Y' + str(round(Height*PixelSize-y*PixelSize, 4)) +
                                '\n')

                        f.write('G01 ' + 'X' +
                                str(round(x*PixelSize + Offset*PixelSize + Pix, 4)) +
                                ' Y' + str(round(Height*PixelSize-y*PixelSize, 4)) +
                                '\n')
                # Прорисовка полей справа

                f.write('G00 ' + 'X' +
                        str(round(Width*PixelSize + Offset*2*PixelSize, 4)) +
                        ' Y' + str(round(Height*PixelSize-y*PixelSize, 4)) + '\n')
                f.write('G01 ' + 'X' +
                        str(round(Width*PixelSize + Offset*2*PixelSize + Pix, 4)) +
                        ' Y' + str(round(Height*PixelSize-y*PixelSize, 4)) + '\n')

            # для нечетных строк проход справа налево
            else:
                # Прорисовка полей справа
                f.write('G00 ' + 'X' +
                        str(round(Width*PixelSize + Offset*2*PixelSize + Pix, 4)) +
                        ' Y' + str(round(Height*PixelSize-y*PixelSize, 4)) + '\n')
                f.write('G01 ' + 'X' +
                        str(round(Width*PixelSize + Offset*2*PixelSize, 4)) +
                        ' Y' + str(round(Height*PixelSize-y*PixelSize, 4)) + '\n')

                for x in range(len(Bitmap[0])-1, 0, -1):
                    if Bitmap[y][x] == 0:
                        f.write('G00 ' + 'X' +
                                str(round(x*PixelSize + Offset*PixelSize + Pix, 4)) +
                                ' Y' + str(round(Height*PixelSize-y*PixelSize, 4)) + '\n')
                        f.write('G01 ' + 'X' +
                                str(round(x*PixelSize + Offset*PixelSize, 4)) +
                                ' Y' + str(round(Height*PixelSize-y*PixelSize, 4)) + '\n')
                # Прорисовка полей слева
                f.write('G00 ' + 'X0.05' + ' Y' +
                        str(round(Height*PixelSize-y*PixelSize, 4)) + '\n')
                f.write('G01 ' + 'X0' + 'Y' +
                        str(round(Height*PixelSize-y*PixelSize, 4)) + '\n')

        f.close()
        Message_Done = tk.messagebox.showinfo('Работа закончена', 'Готово')


root = Tk()
MyGUI = GUI(root)

root.mainloop()
