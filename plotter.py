import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy

# http://www.colorcombos.com/color-schemes/6656/ColorCombo6656.html
# mint = '#218C8D'
# cyan = '#6CCECB'
# yellow = '#F9E559'
# orange = '#EF7126'
# green = '#8EDC9D'
# dark = '#473E3F'

# http://blog.bharatbhole.com/creating-boxplots-with-matplotlib/
mint = '#1b9e77'
blue = '#7570b3'
yellow = '#b2df8a'
red = '#e7298a'
coal= "#555555"

color_array = ["r", "y", "g", "c", "b", "w"]

def mean(values): return sorted(values)[(len(values)+1)/2]
def avg(values): return sum(values) / len(values)

def aggregate_stacked(data, function=avg):
    aggregated = [None] * len(data[0])
    for i in range(len(data[0])):
        aggregated[i] = function([values[i] for values in data])
    return aggregated

def multibar(fig, x_keys, multi_keys, values, y_min=0, y_max=0):
    ax = fig.add_subplot(111)

    N = len(x_keys)
    ind = numpy.arange(N)
    width = 0.9 / N

    i = 0
    rects = []
    for row in values:
        rects.append(ax.bar(ind + width + (i * width)-0.03 , row[1:], width, color=color_array[i], alpha=0.5))
        i += 1

    ax.set_ylabel("Energy Consumption Peer A (Ws)")
    ax.set_xticks(ind + 3.5 * width - 0.03)
    ax.set_xticklabels(x_keys)
    ax.set_xlabel("Announcement Interval Peer B (s)")

    ax.legend(rects, multi_keys, title="Announcement Interval Peer A (s)", ncol=5)

    def autolabel(rects):
        # attach some text labels
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()/2., 1.05*height, '%d' % int(height), ha='center', va='bottom')

    # autolabel(rects1)
    # autolabel(rects2)
    ax.tick_params(axis="x", bottom="off", top="off")

    if y_min != 0: ax.set_ylim(bottom=y_min)
    if y_max != 0: ax.set_ylim(top=y_max)


def boxplot(fig, keys, values, bottom=None, top=None):
    '''Creates a boxplot: keys -> x-axis ticks; values -> arrays of values'''
    ax = fig.add_subplot(111)

    # Create the boxplot
    bp = ax.boxplot(values, patch_artist=True)
    ax.set_xticklabels(keys)

    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    if bottom != None and top != None: ax.set_ylim(bottom, top)
    plt.xticks(rotation=70)

    plt.setp(bp['boxes'], color=blue, linewidth=2)
    plt.setp(bp['boxes'], facecolor=mint)
    plt.setp(bp['whiskers'], color=blue)
    plt.setp(bp['caps'], color=blue)
    plt.setp(bp['medians'], color=yellow, linewidth=2)
    plt.setp(bp['fliers'], marker='+')

def multibox(fig, keys, values, modul, bottom=None, top=None):
    ax = fig.add_subplot(111)

    # Create the boxplot
    bp = ax.boxplot(values, patch_artist=True)
    ax.set_xticklabels(keys)
    ax.set_yscale('log')
    from matplotlib.ticker import FuncFormatter
    ax.yaxis.set_major_formatter(FuncFormatter(lambda y,pos: ('{{:.{:1d}f}}'.format(int(numpy.maximum(-numpy.log10(y),0)))).format(y)))

    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    if bottom != None and top != None: ax.set_ylim(bottom, top)
    plt.xticks(rotation=90)
    xticklabels = ax.xaxis.get_ticklabels()
    # for i in range(len(xticklabels)):
        # if i % (modul+1) != 0: xticklabels[i].set_visible(False)

    # plt.setp(bp['boxes'], facecolor=mint)
    lw = 0.5
    plt.setp(bp['medians'], color="black", linewidth=0.5, alpha=0.5)
    plt.setp(bp['fliers'], marker='+', markerfacecolor='black', markersize=3, alpha=0.5)
    plt.setp(bp['whiskers'], ls="solid")

    for i in range(len(bp["boxes"])):
        i1 = (i) * 2
        i2 = (i+1) * 2 - 1

        # box = bp['boxes'][i]

        stroke_color = color_array[i % (modul+1)]
        plt.setp(bp['boxes'][i], color=stroke_color, linewidth=lw, alpha=0.5)
        plt.setp(bp['whiskers'][i1], color=stroke_color, linewidth=lw, alpha=1)
        plt.setp(bp['whiskers'][i2], color=stroke_color, linewidth=lw, alpha=1)
        plt.setp(bp['caps'][i1], color="black", linewidth=lw, alpha=0.5)
        plt.setp(bp['caps'][i2], color="black", linewidth=lw, alpha=0.5)

    # ax.set_ylim([0.2,11])


def heatmap(fig, x, y, intensity, rotate=False):
    '''Creates a heatmap: x -> x-axis ticks; y -> y-axis ticks; intensity -> array of array of intensity-values.'''
    if rotate:
        x, y = y, x
        intensity = list(reversed(zip(*intensity)))

    plt.pcolormesh(range(len(x) + 1), range(len(y) + 1), intensity)
    plt.axis('tight')
    plt.xticks(range(len(x)), x, rotation=90)

    # add a colorbar to show the intensity scale
    plt.colorbar()


def num_color(i, count, inverse=True, basecolor="#CC33%0.2X"):
    '''creates colours based for a given number (0 <= i < count)'''
    if inverse: i = count - i - 1
    color = basecolor % (i * (256 / count))
    return color

def stackedArea(ax, data, basecolor="#AAFF%0.2X", linewidth=0.0, alpha=0.3):
    '''Creates a stacked area: data -> 2d-array[node][time]'''

    # create scale for data
    x = numpy.arange(len(data[0]))
    # add empty array for "baseline graph"
    data = [[0] * len(data[0])] + data
    stacked_data = numpy.cumsum(data, axis=0)

    for i in range(1, len(stacked_data)):
        ax.fill_between(x, stacked_data[i-1], stacked_data[i], facecolor=num_color(i, len(stacked_data), basecolor=basecolor), alpha=alpha, color="black", linewidth=linewidth)

    # if linewith is 0.0 add a single top line.
    if linewidth == 0.0:
        ax.plot(x, stacked_data[-1], linewidth=0.5, color=coal, alpha=0.5)

def event(fig, x_value, description):
    '''Creates a vertical line: x_value -> position; description -> text to write'''
    ax = fig.add_subplot(111)
    ax.axvline(x_value, color=coal, linewidth=0.2)
    x_bounds = ax.get_xlim()
    ax.annotate(s=description, xy =(((x_value-x_bounds[0])/(x_bounds[1]-x_bounds[0])-0.012), 1.01), xycoords='axes fraction', verticalalignment='right', horizontalalignment='right bottom', rotation=90)

def line(ax, data, color="red", linewidth=0.5, alpha=0.5):
    '''Creates a line: data -> f(x)'''
    # create scale for data
    x = numpy.arange(len(data))
    ax.plot(x, data, color=color, linewidth=linewidth, alpha=alpha)
