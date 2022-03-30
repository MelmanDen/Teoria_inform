import tkinter as tk
import tkinter.messagebox as mb
import binascii

window = tk.Tk()
window.title('Encoder+Decoder')
window.geometry('500x600+700+400')
window.resizable(False, False)
window.configure(bg='black')
summators_str = []


def encoding():
    global spisok_text_to_bit
    primal_text = text3.get(1.0, 'end')

    def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
        bits = bin(int(binascii.hexlify(text.encode(encoding, errors)), 16))[2:]
        return bits.zfill(8 * ((len(bits) + 7) // 8))

    spisok_text_to_bit = text_to_bits(primal_text)
    print(spisok_text_to_bit)
    # вводим элементы которые потребуются

    spisok_polinomov = []
    spisok_polinov_do_sumpomod2 = []
    spisok_indeksov_edinic = []

    # Из списка битов вытаскиваем индексы единиц для кодирования полиномами
    for i in range(len(spisok_text_to_bit)):
        if spisok_text_to_bit[i] == '1':
            spisok_indeksov_edinic.append(i)

    print(spisok_indeksov_edinic)
    print(summators)

    # делам "умножение полиномов"
    for i in range(len(summators)):
        for j in range(len(summators[i])):
            for m in range(len(spisok_indeksov_edinic)):
                spisok_polinomov.append(spisok_indeksov_edinic[m] + summators[i][j])
        spisok_polinov_do_sumpomod2.append(spisok_polinomov)
        spisok_polinomov = []

    # сложение по модулю 2 полиномов
    for i in range(len(spisok_polinov_do_sumpomod2)):
        f = []
        for j in spisok_polinov_do_sumpomod2[i]:
            if (spisok_polinov_do_sumpomod2[i].count(j) % 2) != 0:
                f.append(j)
        f = list(set(f))
        spisok_polinomov.append(f)
    print(spisok_polinomov)

    # нахождение макс элемента из массива полиномов
    encoded_string = []
    max_el = 0
    for i in spisok_polinomov:
        if max_el < max(i):
            max_el = max(i)
    i = 0
    # Если в одном из вложенных массивов встречается i-тое число то добавляем 1, иначе 0
    while i <= max_el:
        encoded_list = []
        for j in range(len(spisok_polinomov)):
            if i in spisok_polinomov[j]:
                encoded_list += ''.join('1')
            elif i not in spisok_polinomov[j]:
                encoded_list += ''.join('0')
        i += 1
        encoded_string.append(encoded_list)
    # Собираем в красивую конструкцию и выводим из под функции
    global encoded_string_finished
    encoded_string_finished = ''
    print(encoded_string)
    for j in range(len(encoded_string)):
        encoded_string_finished += ''.join(encoded_string[j]) + '.'
    # каждый символ заносим в функцию возращая список закодированных символов
    encoded_string_finished = encoded_string_finished[:-1]
    print(encoded_string_finished)
    encoded_string_finished = encoded_string_finished.split('.')
    print(encoded_string_finished)
    lblansw = tk.Label(text=encoded_string_finished, font=('Roboto', 10, 'bold'), bg='orange', fg='white')
    lblansw.pack()
    lblansw.place(x=20, y=310)
    return encoded_string_finished


def decoding():
    # обьявляем переменные
    global registrs
    registrs = []
    kol_registrov = 0
    global decoded_string
    decoded_string = ''
    # находим кол-во регистров по максимальному элементу в сумматоре и обнуляем их
    for i in summators:
        if kol_registrov < max(i):
            kol_registrov = max(i)

    for i in range(kol_registrov + 1):
        registrs.append(0)

    # функция сдвига регистров в парво
    def append_zero():
        for i in reversed(range(len(registrs))):
            registrs[i] = registrs[i - 1]
        registrs[0] = 0
        return registrs

    # функция создание проверочных битов
    def calc_prov_bits():
        global proverochnie_bits
        proverochnie_bits = ''
        for j in range(len(summators)):
            c = 0
            for m in range(len(summators[j])):
                c += registrs[summators[j][m]]
            if c % 2 == 1:
                proverochnie_bits += ''.join('1')
            elif c % 2 == 0:
                proverochnie_bits += ''.join('0')
        return proverochnie_bits

    # функция декодирование строки
    for i in range(len(encoded_string_finished)):
        append_zero()
        calc_prov_bits()
        if proverochnie_bits != encoded_string_finished[i]:
            registrs[0] = 1
            decoded_string += ''.join('1')
        elif proverochnie_bits == encoded_string_finished[i]:
            decoded_string += ''.join('0')

    print(decoded_string)

    # функции перевода двоичной строки обратно в текст
    if decoded_string != spisok_text_to_bit:
        dlina = len(decoded_string) - len(spisok_text_to_bit)
        decoded_string = decoded_string[:-dlina]

    def text_from_bits(binstring, encoding='utf-8', errors='surrogatepass'):
        n = int(binstring, 2)
        return int2bytes(n).decode(encoding, errors)

    def int2bytes(i):
        hex_string = '%x' % i
        n = len(hex_string)
        return binascii.unhexlify(hex_string.zfill(n + (n & 1)))

    decoded_primal_text = text_from_bits(decoded_string)

    print(decoded_primal_text)
    lblansw_decod = tk.Label(text=decoded_primal_text, font=('Roboto', 10, 'bold'), bg='orange', fg='white')
    lblansw_decod.pack()
    lblansw_decod.place(x=20, y=370)
    return decoded_primal_text


def get_kol_sum():
    global b
    b = 0
    lable1 = text1.get()
    if len(lable1) == 0:
        mb.showwarning("Warning", "Заполните строку ввода")
    if not lable1.isdigit():
        mb.showwarning("Warning", "Используйте только цифры")
    global kol_sum
    kol_sum = int(text1.get())
    print(kol_sum)
    text1.config(state="readonly")
    text2.config(state="normal")
    btn1["state"] = "disabled"
    lbl2.config(text="Введите " + str(b + 1) + " сумматор")


def get_summators():
    lable2 = text2.get()
    if len(lable2) == 0:
        mb.showwarning("Warning", "Введены не все данные")
    elif not lable2.isdigit():
        mb.showwarning("Warning", "Используйте только цифры")

    else:
        global b
        global summators
        summators_str.append(text2.get())
        text2.delete(0, last='end')
        b += 1
        lbl2.config(text="Введите " + str(b + 1) + " сумматор")
        if b == kol_sum:
            text2.config(state="readonly")
            btn2.config(state="disabled")
            lbl2.config(text="Все сумматоры введены")
        summators = []
        for i in range(len(summators_str)):
            summators_list = []
            for j in range(len(summators_str[i])):
                summators_list.append(int(summators_str[i][j]))
            summators.append(summators_list)
        text3.config(state="normal")
        return summators


lbl = tk.Label(text="Кодировщик сверточных полей", font=('Roboto', 10, 'bold'), bg='orange', fg='white')
lbl.place(x=130, y=20)

lbl1 = tk.Label(text="Введите количесвто сумматоров", font=('Roboto', 10, 'bold'), bg='orange', fg='white')
lbl1.place(x=20, y=50)
text1 = tk.Entry(width=2, state="normal", font=('Roboto', 13, 'bold'), bg='red', fg='black')
text1.pack()
text1.place(x=250, y=49)
btn1 = tk.Button(text="Ввод", width=10, font=('Roboto', 8, 'bold'), bg='green', fg='white', command=get_kol_sum)
btn1.pack()
btn1.place(x=300, y=50)

lbl2 = tk.Label(text="Введите сумматоры (начиная с нуля) без запятых", font=('Roboto', 10, 'bold'), bg='orange',
                fg='white')
lbl2.place(x=80, y=80)

lbl2 = tk.Label(text="Введите  сумматор", font=('Roboto', 10, 'bold'), bg='orange', fg='white')
lbl2.place(x=20, y=110)
text2 = tk.Entry(width=10, state="readonly", font=('Roboto', 13, 'bold'), bg='red', fg='white')
text2.pack()
text2.place(x=200, y=110)
btn2 = tk.Button(text="Ввод", width=10, font=('Roboto', 8, 'bold'), bg='green', fg='white', command=get_summators)
btn2.pack()
btn2.place(x=300, y=110)

lbl3 = tk.Label(text="Введите текст который надо закодировать", font=('Roboto', 10, 'bold'), bg='orange', fg='white')
lbl3.place(x=80, y=140)
text3 = tk.Text(width=50, heigh=5, state="disable", font=('Roboto', 13, 'bold'), bg='red', fg='white')
text3.pack()
text3.place(x=20, y=170)

btn3 = tk.Button(text="Закодировать", font=('Roboto', 10, 'bold'), bg='green', fg='white', command=encoding)
btn3.pack()
btn3.place(x=195, y=280)

btn4 = tk.Button(text="Разкодировать", font=('Roboto', 10, 'bold'), bg='green', fg='white', command=decoding)
btn4.pack()
btn4.place(x=195, y=340)


window.mainloop()
