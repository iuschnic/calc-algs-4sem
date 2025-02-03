import calc as c
#import matplotlib.pyplot as plt
import plot as plt
import newton as nw

data = c.read_data("data.txt")
if not data:
    print("Invalid data")

#print(data)
graph_data = []
graph_names = []

canonic = c.find_canonic_coefs(data)
inter_beg = nw.find_optimal_newton(data, data[0][0], 3)
inter_end = nw.find_optimal_newton(data, data[-1][0], 3)
koefs_beg = nw.newton_alg(inter_beg)
koefs_end = nw.newton_alg(inter_end)

y0 = koefs_beg[0]
y1 = koefs_beg[1]
y2 = koefs_beg[2]
y3 = koefs_beg[3]
x0 = inter_beg[0][0]
x1 = inter_beg[1][0]
x2 = inter_beg[2][0]
x = data[0][0]
sec_der_beg = (2 * y2 * x - x1 * y2 + 3 * y3 * x * x - 2 * x2 * x - 2 * x1 * y3 * x + x1 * x2 * y3 - 2 * x0 * y3 * x + 
               x0 * x2 * y3 + x0 * x1 * y3)

y0 = koefs_end[0]
y1 = koefs_end[1]
y2 = koefs_end[2]
y3 = koefs_end[3]
x0 = inter_end[0][0]
x1 = inter_end[1][0]
x2 = inter_end[2][0]
x = data[0][0]
sec_der_end = (2 * y2 * x - x1 * y2 + 3 * y3 * x * x - 2 * x2 * x - 2 * x1 * y3 * x + x1 * x2 * y3 - 2 * x0 * y3 * x + 
               x0 * x2 * y3 + x0 * x1 * y3)

#print(sec_der_beg, sec_der_end)

# График с естественными краевыми условиями
graph_names.append("Естественные краевые условия")
c1 = 0
cn1 = 0
fir_ksi = 0
fir_nu = 0
run = c.find_run_coefs(canonic, fir_ksi, fir_nu)
C = c.find_ci(run, canonic, c1, cn1)
coefs = c.find_all_coefs(data, C)

intervalsx = [elem[0] for elem in data]
intervalsy = [elem[1] for elem in data]

graphx, graphy = c.spline_prepare_plot(coefs, intervalsx)
graph_data.append([graphx, graphy])

# График при равенстве сторой производной сплайна в x0 второй производной многочлена Ньютона 3-й степени
graph_names.append("f''(x0) = P3''(x0)")
c1 = sec_der_beg
cn1 = 0
fir_ksi = 0
fir_nu = c1
run = c.find_run_coefs(canonic, fir_ksi, fir_nu)
C = c.find_ci(run, canonic, c1, cn1)
coefs = c.find_all_coefs(data, C)

intervalsx = [elem[0] for elem in data]
intervalsy = [elem[1] for elem in data]

graphx, graphy = c.spline_prepare_plot(coefs, intervalsx)
graph_data.append([graphx, graphy])

# График при равенстве сторой производной сплайна в x0 и xN второй производной многочлена Ньютона 3-й степени
graph_names.append("f''(x0) = P3''(x0); f''(xN) = P3''(xN)")
c1 = sec_der_beg
cn1 = sec_der_end
fir_ksi = 0
fir_nu = c1
run = c.find_run_coefs(canonic, fir_ksi, fir_nu)
C = c.find_ci(run, canonic, c1, cn1)
coefs = c.find_all_coefs(data, C)

intervalsx = [elem[0] for elem in data]
intervalsy = [elem[1] for elem in data]

graphx, graphy = c.spline_prepare_plot(coefs, intervalsx)
graph_data.append([graphx, graphy])

# График с полиномами Ньютона 3-й степени
graph_names.append("Полином Ньютона")
graphx, graphy = nw.newton_prepare_plot(data, 3)
graph_data.append([graphx, graphy])

plt.draw_plots(graph_data, graph_names, 2, 2)
