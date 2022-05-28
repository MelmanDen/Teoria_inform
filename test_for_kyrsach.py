import random
import binascii


def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int(binascii.hexlify(text.encode(encoding, errors)), 16))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))


def text_from_bits(binstring, encoding='utf-8', errors='surrogatepass'):
    n = int(binstring, 2)
    return int2bytes(n).decode(encoding, errors)


def int2bytes(i):
    hex_string = '%x' % i
    n = len(hex_string)
    return binascii.unhexlify(hex_string.zfill(n + (n & 1)))


def calc_izbitochnie_bits(m):
    # Формула для подсчета количество избыточных битов: 2 ^ r >= m + r + 1

    for i in range(m):
        if 2 ** i >= m + i + 1:
            return i


def pos_zero_bits(data, r):
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


def calc_proverochnie_bits(arr, r):
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


def detecterror(arr, nr):
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


def encode_hemming(primal_text):
    data = text_to_bits(primal_text)
    print(data)
    # вычислить количество избыточных битов
    r = calc_izbitochnie_bits(len(data))

    # Обнулить метса для проверочных битов
    arr = pos_zero_bits(data, r)

    # Вычислить проверочные биты
    arr = calc_proverochnie_bits(arr, r)

    # Внести ошибку
    print(arr)
    num_bit = random.randint(1, len(arr))
    arr = '{0}{1}{2}'.format(arr[:num_bit - 1], int(arr[num_bit - 1]) ^ 1, arr[num_bit:])
    print(arr)
    return arr


def decode_hemming(arr):
    global spisok
    r = calc_izbitochnie_bits(len(arr))

    correction = detecterror(arr, r)
    if correction != 0:
        arr = arr[:correction - 1] + str(int(arr[correction - 1]) ^ 1) + arr[correction:]
        spisok = list(arr)
    for i in reversed(range(r)):
        spisok.pop(2 ** i - 1)
    arr = ''.join(spisok)
    arr = text_from_bits(arr)

    return arr


def encoding_svertoch(primal_text):
    global spisok_text_to_bit

    print(primal_text)
    summators = [[0, 1], [1, 2]]

    def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
        bits = bin(int(binascii.hexlify(text.encode(encoding, errors)), 16))[2:]
        return bits.zfill(8 * ((len(bits) + 7) // 8))

    primal_text += '\n'
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

    return encoded_string_finished


def decoding_svertoch(encoded_string_finished):
    # обьявляем переменные

    registrs = []
    kol_registrov = 0

    summators = [[0, 1], [1, 2]]
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

    decoded_string = decoded_string[:-1]

    decoded_primal_text = text_from_bits(decoded_string)
    print(decoded_primal_text)
    return decoded_primal_text


def encoding_matrix():
    pass


def decoding_matrix():
    pass


aaaa = encode_hemming('привет')
print(aaaa)
bbbb = decode_hemming(aaaa)
print(bbbb)

aaaa1 = encoding_svertoch('попа')
bbbb1 = decoding_svertoch(aaaa1)
print(aaaa1)
print(bbbb1)
