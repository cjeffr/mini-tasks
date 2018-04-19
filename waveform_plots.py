import numpy as np
import matplotlib.pyplot as plt
import os

def create_subplot(number,v, x):
    fig = plt.Figure()

    ax = plt.subplot(number, v, x)

    return ax
def subplot_count(subplot_number, i):
    if subplot_number % 2 ==0:
        v = 2
        mod = subplot_number / 2
        x = (i % mod) + 1

    else:
        v = 1
        x = i + 1
        mod = subplot_number
    return(mod, v, x)

def create_group_plot(subplot_number, i, h1, h2, t1, t2, slip, gauge_depth):
    mod, v, x = subplot_count(subplot_number)

    ax = create_subplot(mod, v, x)

    # stuff to make the plots look pretty
    additional_incrememnts = 1
    units_per_tick = 15
    seconds_per_increment = 15 * 60
    num_ticks = int(np.floor(max(t1) / seconds_per_increment) + additional_incrememnts)

    # Actual plot items
    #plt.figure(1, figsize=(10, 5))  # open the plot figure, declare size
    ax.plot(t2, h2, 'b', label='{}m slip'.format(slip))  # plot compare gauge
    ax.plot(t1, h1 * slip, 'r', label='1m slip * {}'.format(slip))  # plot 1m slip gauge * slip
    plt.xlabel("Time (minutes)", fontsize=16)  # declare the x axis label
    plt.ylabel("Wave Amplitude (m)", fontsize=16)
    plt.axhline(y=0.00, xmin=0, xmax=14400, c='black', linewidth=.5, zorder=0)  # draw a zero line
    # declare the x-axis tick marks
    plt.xticks([seconds_per_increment * i for i in range(num_ticks)],
               ['%d' % (i * units_per_tick) for i in range(num_ticks)])
    plt.xlim(0, 5400.)
    plt.legend(loc='upper right')
    plt.title('{}m water depth'.format(gauge_depth))  # title shows what water depth each gauge is located
    plt.tick_params(labelsize=16)

    #plt.savefig('{}m slip {}m depth'.format(slip, depth))
    plt.show()

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
number = len(depth)
for i, d in enumerate(depth):

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

    create_group_plot(number, i, h1, h2, t1, t2, slip_amount, gauge_depth)
