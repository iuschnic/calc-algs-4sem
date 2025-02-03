import math as m

def laplas_func(left: float, right: float, steps: int):
    # F(x) = 2/sqrt(2 * PI) * integral(t0 = 0; t1 = x)(exp(-t^2 / 2)dt) - Функция Лапласа
    summ = 0
    if left >= right:
        return 0
    # h - длина отрезка интегрирования
    h = (right - left) / steps
    # Интегрировать будем методом трапеций из-за его простоты и относительно хорошей точности
    x = left
    while x < right:
        # Вычисляем площадь очередной трапеции
        summ += h * (m.exp(-x**2 / 2) + m.exp(-(x + h)**2 / 2)) / 2
        x += h
    summ /= m.sqrt(m.pi * 2)
    return summ

def find_x(f_x: float, eps: float):
    # Предел функции Лапласа на +inf = 0.5
    if f_x >= 0.5:
        return None
    '''
    По заданному значению функции Лапласа f_x требуется нацти аргумент x с точностью eps
    методом половинного деления
    F(x) = 1/sqrt(2 * PI) * integral(t0 = 0; t1 = x)(exp(-t^2 / 2)dt) - Функция Лапласа
    Чтобы использовать метод половинного деления, сначала найдем такой х, F(x) для которого будет больше
    поданного на вход. Далее в этом интервале методом половинного деления с заданной точностью найдем x
    '''
    x_big = 1
    f_big = laplas_func(0, x_big, 1000)
    while f_big < f_x:
        x_big *= 2
        f_big = laplas_func(0, x_big, 1000)
    # Получаем x_big заведомо больший искомого x
    x_r = x_big
    x_l = 0
    f = laplas_func(0, (x_r + x_l) / 2, 1000)
    max_iter = 1000
    iterations = 1
    # Сужаем диапазон до получения заданной точности
    while abs((f - f_x) / f_x) > eps and iterations < max_iter:
        if f > f_x:
            x_r = (x_r + x_l) / 2
        else:
            x_l = (x_r + x_l) / 2
        f = laplas_func(0, (x_r + x_l) / 2, 1000)
        iterations += 1
    print("Задание 2:")
    print(f"Найденный x = {(x_r + x_l) / 2}")
    print(f"Значение F(x) = {f}")
    print(f"Произведено {iterations} итераций")
    print()
    return (x_r + x_l) / 2
