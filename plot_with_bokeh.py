import numpy as np

from bokeh.layouts import gridplot
from bokeh.plotting import figure, output_file, show

def datetime(x):
    return np.array(x, dtype=np.datetime64)

a = np.loadtxt('allTimeCryptoBalance.txt',delimiter='\t')

p1 = figure(x_axis_type="datetime", title="Stock Closing Prices")
p1.grid.grid_line_alpha=0.3
p1.xaxis.axis_label = 'Date'
p1.yaxis.axis_label = 'Price'

p1.line(list(a[:,0]), list(a[:,1]), color='#A6CEE3', legend='Balance')
p1.legend.location = "top_left"

output_file("test.html")

show(gridplot([[p1]], plot_width=800, plot_height=400))  # open a browser

