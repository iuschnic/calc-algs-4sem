def read_data(file_name):
    data = [[[0 for i in range(5)] for j in range(5)] for k in range(5)]
    try:
        file = open(file_name, "r")
    except Exception:
        return None
    for z in range(5):
        for y in range(5):
            line = file.readline()
            x_s = line.split()
            for x in range(5):
                data[x][y][z] = int(x_s[x])
        file.readline()
    return data


# Функция поиска коэффициентов Ai, Bi, Ci, Fi канонической записи системы
def find_canonic_coefs(data):
    table = [[0, 0, 0, 0], [0, 0, 0, 0]]     #индексация начинается с 2, заполним два буферных элемента для простоты
    # Ai, Bi, Ci, Fi  i = [2....N] делаем буфер чтобы было прорще отслеживать индексацию
    for i in range(2, len(data)):
        hi_1 = data[i - 1][0] - data[i - 2][0]
        hi = data[i][0] - data[i - 1][0]
        yi_2 = data[i - 2][1]
        yi_1 = data[i - 1][1]
        yi = data[i][1]

        Ai = hi_1
        Di = hi
        Bi = -2 * (hi_1 + hi)
        Fi = -3 * ((yi - yi_1) / hi - (yi_1 - yi_2) / hi_1)

        table.append([Ai, Bi, Di, Fi])
    return table

# Функция поиска прогоночных коэффициентов по коэффициентам канонической записи
def find_run_coefs(canonic_table, fir_ksi, fir_nu):
    run_coefs = [[0, 0], [0, 0], [fir_ksi, fir_nu]]     # первый два индекса использоваться не будут, тоже буферные
    # начальные значения, в лекции имеют индекс 2
    ksi = fir_ksi
    nu = fir_nu
    for i in range(2, len(canonic_table)):
        Ai = canonic_table[i][0]
        Bi = canonic_table[i][1]
        Di = canonic_table[i][2]
        Fi = canonic_table[i][3]
        #print(Ai, Bi, Di, Fi)
        temp_ksi = Di / (Bi - Ai * ksi)
        temp_nu = (Fi + Ai * nu) / (Bi - Ai * ksi)
        ksi = temp_ksi
        nu = temp_nu
        run_coefs.append([ksi, nu])
    return run_coefs


def find_ci(run_coefs, canonic_table, c1, cn1):
    C = [0, cn1]     # CN+1 = 0
    c_last = cn1
    for i in range(len(canonic_table) - 1, 1, -1):
        Ai = canonic_table[i][0]
        Bi = canonic_table[i][1]
        Di = canonic_table[i][2]
        Fi = canonic_table[i][3]
        ksi = run_coefs[i][0]
        nu = run_coefs[i][1]
        c = Di * c_last / (Bi - Ai * ksi) + (Fi + Ai * nu) / (Bi - Ai * ksi)
        c_last = c
        C.append(c)
    C.append(c1)
    C = C[::-1]
    C = C[:-1]
    return C

def find_all_coefs(data, c_table):
    coefs = [[0, 0, 0, 0]]     # буферные данные
    for i in range(1, len(c_table)):
        yi = data[i][1]
        yi_1 = data[i - 1][1]
        hi = data[i][0] - data[i - 1][0]
        ci = c_table[i - 1]
        ci_next = c_table[i]

        ai = yi_1
        di = (ci_next - ci) / (3 * hi)
        bi = ((yi - yi_1) / hi) - (hi * (ci_next + 2 * ci) / 3)
        coefs.append([ai, bi, ci, di])
    return coefs


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
    return array[middle - amount // 2: middle + (amount - amount // 2)]


# Функция по введенному массиву узлов и значению аргументу x
# Интерполирует функцию по этим узлам и считает ее значение в точке x методом Ньютона
def newton_alg(nodes, x):
    split_diffs = []     # массив разделенных разностей
    arg_arr = [elem[0] for elem in nodes]     # отдельный массив аргументов x
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

def f_x_y_z(data, nx, ny, nz, x0, y0, z0, modex, modey, modez):
    # modex, modey, modez - режимы построения ньютоном или сплайном по x, y, z
    # Дана таблица по трем переменным - x, y, z (от 0 до 4 каждая)
    # Сначала проведем интерполяцию по z
    # На каждом шаге принимаем x = x1, y = y1 из таблицы data
    # По этой конкретной строке интерполируем по z в точке z0 и заносим в новую таблицу
    # Новая таблица - таблица по f(x, y, z0)
    f_x_y = [[0 for i in range(5)] for j in range(5)]
    for x in range(5):
        for y in range(5):
            table = []
            for i in range(len(data[x][y])):
                table.append([i, data[x][y][i]])
            if modez == 0:
                interval = find_optimal_newton(table, z0, nz)
                ans = newton_alg(interval, z0)
                f_x_y[x][y] = ans
            else:
                canonic = find_canonic_coefs(table)
                c1 = 0
                cn1 = 0
                fir_ksi = 0
                fir_nu = 0
                run = find_run_coefs(canonic, fir_ksi, fir_nu)
                C = find_ci(run, canonic, c1, cn1)
                coefs = find_all_coefs(table, C)
                if z0 >= 5:
                    return -1
                index = int(z0)
                a = coefs[index][0]
                b = coefs[index][1]
                c = coefs[index][2]
                d = coefs[index][3]

                f_x_y[x][y] = a + b * z0 + c * z0 ** 2 + d * z0 ** 3


    # Теперь проведем интерполяцию по y
    # На каждом шаге x = x1 из таблицы f_x_y, при этом z = z0 для этой таблицы из прошлой интерполяции
    # По конкретной строке интерполируем по y в точке y0
    # Новая таблица - массив f(x, y0, z0)
    f_x = [0 for i in range(5)]
    for x in range(5):
        table = []
        for i in range(len(f_x_y[x])):
            table.append([i, f_x_y[x][i]])
        if modey == 0:
            interval = find_optimal_newton(table, y0, ny)
            ans = newton_alg(interval, y0)
            f_x[x] = ans
        else:
            canonic = find_canonic_coefs(table)
            c1 = 0
            cn1 = 0
            fir_ksi = 0
            fir_nu = 0
            run = find_run_coefs(canonic, fir_ksi, fir_nu)
            C = find_ci(run, canonic, c1, cn1)
            coefs = find_all_coefs(table, C)
            if y0 >= 5:
                return -1
            index = int(y0)
            a = coefs[index][0]
            b = coefs[index][1]
            c = coefs[index][2]
            d = coefs[index][3]

            f_x[x] = a + b * y0 + c * y0 ** 2 + d * y0 ** 3
    # Теперь проведем интерполяцию по x и получим окончательный ответ
    # Это простая линейная интерполяция
    table = []
    for i in range(len(f_x)):
        table.append([i, f_x[i]])
    if modex == 0:
        interval = find_optimal_newton(table, x0, nx)
        ans = newton_alg(interval, x0)
    else:
        canonic = find_canonic_coefs(table)
        c1 = 0
        cn1 = 0
        fir_ksi = 0
        fir_nu = 0
        run = find_run_coefs(canonic, fir_ksi, fir_nu)
        C = find_ci(run, canonic, c1, cn1)
        coefs = find_all_coefs(table, C)
        if x0 >= 5:
            return -1
        index = int(x0)
        a = coefs[index][0]
        b = coefs[index][1]
        c = coefs[index][2]
        d = coefs[index][3]
        ans = a + b * x0 + c * x0 ** 2 + d * x0 ** 3
    return ans
