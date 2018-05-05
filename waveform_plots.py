import numpy as np
import matplotlib.pyplot as plt
import os

def create_subplot(ar_len, col, row):

    fig = plt.Figure(figsize=(20,20))
    ylim = [-4, 4]

    ax = plt.subplot(ar_len, col, row)
    ax.set_ylim(ylim)


    return ax

def no_cols(ar_len):

    cols = 1 if ar_len % 2 else 2
    if ar_len % 2 == 0 :
        rows = ar_len /2
    else:
        rows = ar_len


    return(cols, rows)

def create_group_plot(ar_len, i, h1, h2, t1, t2, slip, gauge_depth, cols, rows):
    plot_number = i + 1

    ax = create_subplot(rows, cols , plot_number)

    # stuff to make the plots look pretty
    additional_increments = 1
    units_per_tick = 15
    seconds_per_increment = 15 * 60
    num_ticks = int(np.floor(max(t1) / seconds_per_increment) + additional_increments)

    # Actual plot items
    #plt.figure(1, figsize=(10, 5))  # open the plot figure, declare size
    plt.subplots_adjust(hspace=0.35, wspace=0.15)

    ax.plot(t2, h2, 'b', label='{}m slip'.format(slip))  # plot compare gauge
    ax.plot(t1, h1 * slip, 'r', label='1m slip * {}'.format(slip))  # plot 1m slip gauge * slip
    # plt.xlabel("Time (minutes)", fontsize=16)  # declare the x axis label
    # plt.ylabel("Wave Amplitude (m)", fontsize=16)
    plt.axhline(y=0.00, xmin=0, xmax=14400, c='black', linewidth=.5, zorder=0)  # draw a zero line
    # declare the x-axis tick marks
    if plot_number < (ar_len -1):
        plt.xticks([])
    else:
        plt.xticks([seconds_per_increment * i for i in range(num_ticks)],
                   ['%d' % (i * units_per_tick) for i in range(num_ticks)])
    if plot_number % 2 == 0:
        plt.yticks([])
    plt.xlim(0, 5400.)
    plt.figlegend(loc='upper right', prop={'size':6})
    plt.title('{}m water depth'.format(gauge_depth))  # title shows what water depth each gauge is located
    plt.tick_params(labelsize=12)

    plt.savefig('waterdepth.ps')


def get_data(file1, file2):
    data = np.loadtxt(file1)
    data1 = np.loadtxt(file2)
    h1 = data[:,5]
    h2 = data1[:,5]
    t1 = data[:,1]
    t2 = data1[:,1]
    return h1, h2, t1, t2



depth = [5, 10, 15, 20, 30, 40]
slip = 20
ar_len = len(depth)
print(ar_len)
cols, rows = no_cols(ar_len)
for i, d in enumerate(depth):
    print(i, d)
    gauge_depth = d # water depth of the gauge
    slip_amount = slip # amount of slip to compare
    gauge_file = 'gauge{:05d}.txt'.format(gauge_depth) # name of the gauge file, uses water depth
    # path of the 1m slip file
    path_original = '/Users/jeffriesc/clawpack-5.4.1/geoclaw/examples/tsunami/TestingLinearity/SF_8_1m/_output'
    # path of the comparison file
    path_compare = '/Users/jeffriesc/clawpack-5.4.1/geoclaw/examples/tsunami/TestingLinearity/SF_8_20m/_output'  # .format(d)
    # file names
    file_original = os.path.join(path_original, gauge_file)
    file_compare = os.path.join(path_compare, gauge_file)
    # call the function, pass the parameters
    h1, h2, t1, t2 = get_data(file_original, file_compare)

    create_group_plot(ar_len, i, h1, h2, t1, t2, slip_amount, gauge_depth, cols, rows)
plt.show()