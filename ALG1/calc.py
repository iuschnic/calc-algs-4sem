import math as m
def read_data(file_name, arr):
    try:
        file = open(file_name, "r")
    except Exception:
        return -1
    file.readline()     # пропуск шапки файла
    while True:
        line = file.readline()
        if not line:
            break
        try:
            x, y, y_der1, y_der2 = map(float, line.split())     # чтение очередной строки данных и ее преобразование
        except ValueError:
            return -2
        elem = [x, y, y_der1, y_der2]
        arr.append(elem)
    return 0


# Функция ищет оптимальные узлы(интервал) для построения многочлена
# Ньютона для данной таблицы, данного x, данной степени
# Таблица должна быть отсортирована
def find_optimal_newton(array, x, deg):
    amount = deg + 1
    # если узлов не хватает, сразу выходим
    if len(array) < amount:
        return None
    # если узлов ровно сколько нужно - возвращаем весь массив
    if len(array) == amount:
        return array
    middle = -1     # в этой переменной будет храниться индекс центрального элемента интервала
    left_border = amount // 2     # левая граница поиска серединного элемента интервала
    right_border = len(array) - 1 - amount // 2     # правая граница
    # находим срединный индекс нужного нам интервала
    for i in range(left_border, right_border + 1):
        if array[i][0] > x:
            middle = i
            break
    # если не нашли подходящий серединный, нужно брать конец таблицы
    if middle == -1:
        middle = right_border + 1
    #print(array[middle - amount // 2 : middle + (amount - amount // 2)])
    print(len(array[middle - amount // 2 : middle + (amount - amount // 2)]))
    return array[middle - amount // 2 : middle + (amount - amount // 2)]


# Функция по введенному массиву узлов и значению аргументу x
# Интерполирует функцию по этим узлам и считает ее значение в точке x методом Ньютона
def newton_alg(nodes, x):
    split_diffs = []     # массив разделенных разностей
    arg_arr = [elem[0] for elem in nodes]     # отдельный массив аргументов x
    print(arg_arr)
    # сначала в массив заносим исходные значение y(x)
    split_diffs.append([elem[1] for elem in nodes])
    # нужно просчитать на один меньше столбцов, чем есть узлов
    # в каждом столбце при этом будет новая разделенная разность
    for i in range(len(nodes) - 1):
        #  каждом столбце на один элемент меньше чем в предыдущем
        diffs = []
        for j in range(len(nodes) - i - 1):
            new_diff = split_diffs[i][j + 1] - split_diffs[i][j]
            new_diff /= (arg_arr[j + i + 1] - arg_arr[j])
            diffs.append(new_diff)
        split_diffs.append(diffs)
    # получили список коэффициентов многочлена Ньютона
    koefs = [elem[0] for elem in split_diffs]
    print(koefs)
    # теперь считаем ответ в указанной точке
    answer = 0
    # свободный член
    answer += koefs[0]
    for i in range(1, len(koefs)):
        elem = koefs[i]
        for j in range(i):
            elem *= (x - arg_arr[j])
        answer += elem
    return answer


# Функция ищет оптимальные узлы(интервал) для построения многочлена
# Эрмита для данной таблицы, данного x, данной степени
# Таблица должна быть отсортирована
def find_optimal_hermit(array, x, deg):
    amount = deg + 1
    # если условий не хватает(производные считаются полноценным условием), сразу выходим
    if len(array) * 3 < amount:
        return None
    # если узлов ровно сколько нужно - возвращаем весь массив
    if len(array) * 3 == amount:
        return array
    nodes_cnt = int(m.ceil(amount / 3))     # находим количество узлов, включающих нужное количество условий
    middle = -1     # в этой переменной будет храниться индекс центрального элемента интервала
    left_border = nodes_cnt // 2     # левая граница поиска серединного элемента интервала
    right_border = len(array) - 1 - nodes_cnt // 2     # правая граница
    # находим срединный индекс нужного нам интервала
    for i in range(left_border, right_border + 1):
        if array[i][0] > x:
            middle = i
            break
    # если не нашли подходящий серединный, нужно брать конец таблицы
    if middle == -1:
        middle = right_border + 1
    # получаем интервал нужных нам узлов
    interval = array[middle - nodes_cnt // 2 : middle + (nodes_cnt - nodes_cnt // 2)]
    #print(interval)
    # из этого интервала строим массив кратных узлов
    answer = []
    cnt = 0
    for i in range(nodes_cnt):
        for j in range(3):     # кратный узел входит в массив столько, сколько в нем условий
            if cnt < amount:
                answer.append(interval[i])
            cnt += 1
    #print(answer)
    return answer


# Функция по введенному массиву узлов и значению аргументу x
# Интерполирует функцию по этим узлам и считает ее значение в точке x методом Эрмита
def hermit_alg(nodes, x):
    split_diffs = []  # массив разделенных разносте
    arg_arr = [elem[0] for elem in nodes]  # отдельный массив аргументов x
    # сначала в массив заносим исходные значение y(x)
    split_diffs.append([elem[1] for elem in nodes])
    # нужно просчитать на один меньше столбцов, чем есть узлов
    # в каждом столбце при этом будет новая разделенная разность
    for i in range(len(nodes) - 1):
        #  каждом столбце на один элемент меньше чем в предыдущем
        diffs = []
        for j in range(len(nodes) - i - 1):
            # в алгоритме эрмита из-за кратных узлов будут появляться разности вида y(xi, xi....xi)
            # каждая такая разность содержащая m членов xi будет равна m - 1 производной в точке xi
            # деленной на факториал (m - 1)! (выведено математически)
            # если рассматриваемая y(xi, xj...) содержит различные xi, xj то считается она как в алгоритме Ньютона
            new_diff = split_diffs[i][j + 1] - split_diffs[i][j]
            start = arg_arr[j]
            flag = 0
            # проверяем равны ли все xi  данной разделенной разности
            for k in range(j, j + i + 2):
                if arg_arr[k] > start:
                    flag = 1
                    break
            # если они не равны, считаем как при обычном алгоритме
            if flag == 1:
                new_diff /= (arg_arr[j + i + 1] - arg_arr[j])
            # иначе берем производную деленную на факториал
            else:
                length = i + 2     # j + i + 2 - j = i + 2
                new_diff = nodes[j][length] / m.factorial(length - 1)
            diffs.append(new_diff)
        split_diffs.append(diffs)
    # получили список коэффициентов многочлена Ньютона
    koefs = [elem[0] for elem in split_diffs]
    # теперь считаем ответ в указанной точке
    answer = 0
    # свободный член
    answer += koefs[0]
    for i in range(1, len(koefs)):
        elem = koefs[i]
        for j in range(i):
            elem *= x - arg_arr[j]
        answer += elem
    return answer


# По таблице состоящей из x, y, y', y'' функция составляет новую таблицу, меняя аргументы местами
# То есть составляется таблица x(y) , где в том числе пересчитываются производные обратных функций
def invert_table(array):
    new = []
    for elem in array:
        #new_fir_der = 1 / elem[2]     # первая производная x' по y
        #new_sec_der = - (elem[3]) / ((elem[2]) ** 3)     # вторая производная x'' по y
        new_fir_der = 0
        new_sec_der = 0
        new.append([elem[1], elem[0], new_fir_der, new_sec_der])
    new.sort(key=lambda el: el[0])
    return new
