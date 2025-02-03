def one_side_left_dif_derivative(h, yi, yi_1):
    if not h or not yi or not yi_1:
        return "None"
    return '{0:.3f}'.format((yi - yi_1) / h)


def center_dif_derivative(h, ys_p_1, ys_m_1):
    if not h or not ys_p_1 or not ys_m_1:
        return "None"
    return '{0:.3f}'.format((ys_p_1 - ys_m_1) / 2 / h)


'''
f"(x) = (Yi+1 - 2Yi + Yi-1) / h^2 + ((Yi+1 - 2Yi + Yi-1)/h^2 - (Yi+2 - 2Yi + Yi-2)/4h^2)/(2^2 - 1)
'''
def second_runge_formula(left_dif_derivative_s_1, left_dif_derivative_s_2,  m, p):
    return '{0:.3f}'.format(left_dif_derivative_s_1 + (left_dif_derivative_s_1 - left_dif_derivative_s_2) / (m ** p - 1))


def derivative_with_align_vars(teta1, teta2, xsi1, xsi2, y1, x1):
    return '{0:.3f}'.format(((teta2 - teta1) / (xsi2 - xsi1) - 1 / y1) / (- x1 / (y1 ** 2)))


def second_dif_derivative(h, ys_p_1 = None, ys = None, ys_m_1 = None):
    if ys_p_1 != None and ys_m_1 != None:
        return '{0:.3f}'.format((ys_p_1 - 2 * ys + ys_m_1) / (h ** 2))
    else:
        return "None"