import matplotlib.pyplot as plt

def scatter_plot(points, labels):
    xs, ys = zip(*points)
    fig, ax = plt.subplots()
    ax.scatter(xs, ys)

    for label, x, y in zip(labels, xs, ys):
        ax.annotate(label, (x, y))
