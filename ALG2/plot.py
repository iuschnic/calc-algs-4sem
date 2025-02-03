import matplotlib.pyplot as plt

def draw_plot(graphx, graphy):
    fig = plt.figure(figsize=(6, 6))
    plt.plot(graphx, graphy)
    plt.show()

def draw_plots(data, graph_names, nrows, ncols):
    fig, ax = plt.subplots(nrows, ncols, figsize=(15, 10))
    num = 0
    for i in range(nrows):
        for j in range(ncols):
            ax[i][j].set_title(graph_names[num])
            ax[i][j].plot(data[num][0], data[num][1], )
            num += 1
    plt.show()

