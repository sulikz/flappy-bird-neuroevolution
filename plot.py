import matplotlib.pyplot as plt
import pygetwindow
from IPython import display

plt.ion()


def init_plot():
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.clf()


def plot(scores):
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.clf()
    plt.title('Training...')
    plt.xlabel('Generation')
    plt.ylabel('Score')
    plt.plot(scores)
    plt.ylim(ymin=0)
    plt.text(len(scores) - 1, scores[-1], str(scores[-1]))
    plt.show(block=False)
    plt.pause(.1)
