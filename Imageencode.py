from PIL import Image
import tkinter as tk
from tkinter import filedialog as fd
import tkinter.messagebox as mb
import random
import numpy as np
import copy

window = tk.Tk()
window.title('Encoder+Decoder')
window.geometry('400x300+700+400')
window.resizable(False, False)
window.configure(bg='black')
Izbitochnie_bits = 4


def task_entry():
    global a
    global b
    global im
    tipimage = [('картинка', '*.jpg')]
    imagin = fd.askopenfilename(filetypes=tipimage)
    if imagin is not None:
        im = Image.open(imagin).resize((400, 400))
        a = np.array(im)
        b = copy.deepcopy(a)
        btn2.config(state="normal")
    else:
        mb.showwarning("Warning", "Выберите картинку")


def zashumlenie(matrica):
    shumka = random.randint(1, 255)
    oshibka = bin(matrica ^ shumka)
    return int(oshibka, 2)


def Pos_zero_Bits(data, r=Izbitochnie_bits):
    # Обнуляем места для проверочных битов
    # Позиции степени двойки
    j = 0
    k = 0
    m = len(data)
    res = ''

    # Если позиция равна степени двойки добавляем ноль
    # Иначе берем символ кодового слова
    for i in range(1, m + r + 1):
        if i == 2 ** j:
            res = res + '0'
            j += 1
        else:
            res = res + data[k]
            k += 1

    return res


def calc_Proverochnie_Bits(arr, r=Izbitochnie_bits):
    n = len(arr)

    # Считаем проверочные биты
    for i in range(r):
        val = 0
        for j in range(1, n + 1):

            # По строке с 1 через 1 со 2 через 2 и тд
            # складывая значения по модулю 2
            if j & (2 ** i) == (2 ** i):
                val = val ^ int(arr[j - 1])

        # Заменяем проверочные биты
        arr = arr[:(2 ** i) - 1] + str(val) + arr[(2 ** i):]
    return arr


def detectError(arr, nr):
    n = len(arr)
    res = 0

    # Снова считаем проверочные биты
    for i in range(nr):
        val = 0
        for j in range(1, n + 1):
            if j & (2 ** i) == (2 ** i):
                val = val ^ int(arr[j - 1])

        res = res + val * (10 ** i)

    return int(str(res), 2)


def encode(rgb):
    data = format(int(rgb), 'b').zfill(8)
    # вычислить количество избыточных битов
    r = Izbitochnie_bits

    # Обнулить метса для проверочных битов
    arr = Pos_zero_Bits(data, r)

    # Вычислить проверочные биты
    arr = calc_Proverochnie_Bits(arr, r)

    # Внести ошибку

    num_bit = random.randint(1, len(arr))
    arr = '{0}{1}{2}'.format(arr[:num_bit - 1], int(arr[num_bit - 1]) ^ 1, arr[num_bit:])

    return arr


def decode(arr, r=Izbitochnie_bits):
    correction = detectError(arr, r)
    if correction != 0:
        arr = arr[:correction - 1] + str(int(arr[correction - 1]) ^ 1) + arr[correction:]

    arr = arr[2] + arr[4:7] + arr[8:]

    return int(arr, 2)


def task_main():
    im.show()

    for i in range(len(a)):
        for j in range(len(a[i])):
            for m in range(len(a[i][j])):
                a[i][j][m] = zashumlenie(a[i][j][m])

    im2 = Image.fromarray(a, mode="RGB")
    im2.save('shumka.jpg')
    im2.show()

    for RED in range(len(b)):
        for GREEN in range(len(b[RED])):
            for BLUE in range(len(b[RED][GREEN])):
                b[RED][GREEN][BLUE] = decode(encode(b[RED][GREEN][BLUE]))

    im3 = Image.fromarray(b, mode="RGB")
    im3.save('myimg.jpg')
    im3.show()


lbl = tk.Label(text="Кодировщик изображений", font=('Roboto', 10, 'bold'), bg='orange', fg='white')
lbl.place(x=120, y=20)

lbl1 = tk.Label(text="Выбирите картинку", font=('Roboto', 10, 'bold'), bg='orange', fg='white')
lbl1.place(x=20, y=50)

btn1 = tk.Button(text="Выбрать", width=10, font=('Roboto', 8, 'bold'), bg='green', fg='white', command=task_entry)
btn1.pack()
btn1.place(x=200, y=50)

btn2 = tk.Button(text="Запуск", width=10, font=('Roboto', 8, 'bold'), bg='green', fg='white', state="disabled", command=task_main)
btn2.pack()
btn2.place(x=200, y=110)

window.mainloop()
