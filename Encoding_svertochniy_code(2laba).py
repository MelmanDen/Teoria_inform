# import tkinter as tk
# import tkinter.messagebox as mb

primal_text = "1011"
# summators = []
spisok_text_to_bit = []
abc = []
encoded_string_finished = ''
print(primal_text, type(primal_text))
for i in primal_text:
    spisok_text_to_bit.append(bin(ord(i))[2:])
print(spisok_text_to_bit)
spisok_text_to_bit = "".join(spisok_text_to_bit)
print(spisok_text_to_bit)


# # вводим сумматоры Доделать!!!!
# kol_summators = int(input("введите колво сумматоров "))
# # сдлеать вывод месседжбоксов для ввода сумматоров
# for i in range(kol_summators):
#     # сделать ошибку ввода для чисел больше количества регистров!!!
#     summators.append(list(input('введите сумматоры ')))
#
# for i in range(len(summators)):
#     for j in range(len(summators[i])):
#         summators[i][j] = int(summators[i][j])
# print(summators, type(summators[0][0]))

def encoding(spisok_text_to_bit):
    # вводим элементы которые потребуются
    summators = [[0, 1], [1, 2]]
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
    return encoded_string_finished


# каждый символ заносим в функцию возращая список закодированных символов

encoding(spisok_text_to_bit)
print(encoded_string_finished)
