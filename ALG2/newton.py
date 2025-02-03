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
    middle = -1  # в этой переменной будет храниться индекс центрального элемента интервала
    left_border = amount // 2  # левая граница поиска серединного элемента интервала
    right_border = len(array) - 1 - amount // 2  # правая граница
    # находим срединный индекс нужного нам интервала
    for i in range(left_border, right_border + 1):
        if array[i][0] > x:
            middle = i
            break
    # если не нашли подходящий серединный, нужно брать конец таблицы
    if middle == -1:
        middle = right_border
    # print(array[middle - amount // 2 : middle + (amount - amount // 2)])
    #print(len(array[middle - amount // 2: middle + (amount - amount // 2)]))
    return array[middle - amount // 2: middle + (amount - amount // 2)]


# Функция по введенному массиву узлов и значению аргументу x
# Интерполирует функцию по этим узлам и считает ее значение в точке x методом Ньютона
def newton_alg(nodes):
    split_diffs = []     # массив разделенных разностей
    arg_arr = [elem[0] for elem in nodes]     # отдельный массив аргументов x
    #print(arg_arr)
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
    '''print(koefs)
    # теперь считаем ответ в указанной точке
    answer = 0
    # свободный член
    answer += koefs[0]
    for i in range(1, len(koefs)):
        elem = koefs[i]
        for j in range(i):
            elem *= (x - arg_arr[j])
        answer += elem
    return answer'''
    return koefs

def newton_answer(nodes, coefs, x):
    answer = 0
    arg_arr = [elem[0] for elem in nodes]  # отдельный массив аргументов x
    # свободный член
    answer += coefs[0]
    for i in range(1, len(coefs)):
        elem = coefs[i]
        for j in range(i):
            elem *= (x - arg_arr[j])
        answer += elem
    return answer


def newton_prepare_plot(data, deg):
    graphx = []
    graphy = []
    dx = data[-1][0] - data[0][0]
    step = dx / 300
    start = data[0][0]
    end = data[-1][0]
    while start < end:
        nodes = find_optimal_newton(data, start, deg)
        coefs = newton_alg(nodes)
        y = newton_answer(nodes, coefs, start)
        graphx.append(start)
        graphy.append(y)
        start += step
    return graphx, graphy
