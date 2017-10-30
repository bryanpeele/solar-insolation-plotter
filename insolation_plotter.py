### Solar Insolation Plotter
### Written By: Bryan Peele
### Last Updated: 2017/10/30
###
### Adapted from code written by Eric Strong
### Source: https://github.com/drericstrong/Blog/blob/master/20170520_linear_example.py
from sklearn.datasets import make_regression
from sklearn.linear_model import LinearRegression as LR
from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.models.ranges import Range1d
from bokeh.models import ColumnDataSource, LabelSet
from bokeh.layouts import column, row, widgetbox
from bokeh.models.widgets import Slider, Button, Div
import pandas as pd
from pandas import DataFrame
import numpy as np
import time


###-----------------------------------------------------------------------###
###------------------------PARAMETER DEFAULTS-----------------------------###
### This section contains defaults and ranges for the Bokeh controls and  ###
### may be modified without concern, if required. ("View" Part 1)         ###
###-----------------------------------------------------------------------###
# The format for this section is: default, range[Lower, Upper, Step Size]
d_lat, r_lat = 35, [ -90,  90, 2] # Latitude
d_lon, r_lon = 80,  [-180, 180, 2] # Longitude
d_year, r_year = 2005, [1983, 2005, 1]    # Year

#for testing
d_lat, r_lat = 0, [ -90,  90, 2] # Latitude
d_lon, r_lon = 0,  [-180, 180, 2]  # Longitude
d_year, r_year = 2005, [1983, 2005, 1]    # Year


###-----------------------------------------------------------------------###
###----------------------GRAPHICAL USER INTERFACE-------------------------###
### This code defines the Bokeh controls that are used for the user       ###
### interface. All the defaults for the controls are above. This code     ###
### should not need to be modified. ("View" Part 2)                       ### 
###-----------------------------------------------------------------------###
# Plot- Regression Data
plot_data = figure(plot_height=600, plot_width=600,
                   title="Solar Insolation", 
                   toolbar_location="above", 
                   x_axis_label='Month', 
                   y_axis_label='Insolation (kWh/m^2-day)',
                   tools="pan,save,box_zoom,wheel_zoom")
plot_data.title.text_font_size = "20pt"
plot_data.xaxis.axis_label_text_font_size = "14pt"
plot_data.yaxis.axis_label_text_font_size = "14pt"

# Plot Control Buttons
#plot_update = Button(label="Update")
#plot_ctls = column(plot_update)

# Main Control Buttons
ctl_title = Div(text="<h3>Parameters</h3>")
ctl_lat = Slider(title="Latitude", value=d_lat, 
                start=r_lat[0], end=r_lat[1], step=r_lat[2])
ctl_lon = Slider(title="Longitude", value=d_lon, 
                start=r_lon[0], end=r_lon[1], step=r_lon[2])
ctl_year = Slider(title="Year", value=d_year, 
                start=r_year[0], end=r_year[1], step=r_year[2])
ctl_inputs = widgetbox(ctl_title, ctl_lat, ctl_lon, ctl_year)



    
###-----------------------------------------------------------------------###
###------------------DATA SOURCES AND INITIALIZATION----------------------###
### This section defines the data sources which will be used in the Bokeh ###
### plots. To update a Bokeh plot in the server, each of the sources will ###
### be modified in the CALLBACKS section. ("Model")                       ###
###-----------------------------------------------------------------------###
# Generating some initial data for the plots, based on the parameter defaults

d_data_2 = pd.read_csv('./data/insolation_data_1983-2005_trimmed.csv')

time.sleep(0.5)

#Subet useful data
d_data_subset = d_data_2[(d_data_2.Year==d_year) & (d_data_2.Latitude==d_lat) & (d_data_2.Longitude==d_lon)]

# Find the minimum and maximum values of the data, for ranges, etc.
# d_data[0] is the "X" data, and d_data[1] is the "Y" data
# Remember that the "X" data is of size [n,1] while the "Y" data is [n]
# That's the reason for the extra [0] in the "X" data below
d_x = np.array(list(range(1,13)))
d_months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
d_y = np.array(list(d_data_subset.Insolation[0:12]))

d_x_min = 0
d_x_max = 13
d_y_min = -0.5
d_y_max = 15


# Defining the Bokeh data sources
source_data = ColumnDataSource(data=dict(x=d_x, y=d_y))

#source_data = DataFrame(dict(insolation=d_y,time=d_x,label=d_months))

# Associating the sources with plots
plot_data.scatter('x', 'y', source=source_data,size=18)
#plot_data.scatter(x='time', y='insolation', source=source_data,size=18)
#labels = LabelSet(x='time', y='insolation', text='label', level='glyph',
#                x_offset=5, y_offset=5, source=ColumnDataSource(source_data), render_mode='canvas')

#plot_data.add_layout(labels)


# Defining the plot ranges
xrange_data = Range1d(bounds=[None, None], start=d_x_min, end=d_x_max)
yrange_data = Range1d(bounds=[None, None], start=d_y_min, end=d_y_max)
# Associating the ranges with plots
plot_data.x_range = xrange_data
plot_data.y_range = yrange_data

####---
#def update_plot():
#    # Get the current slider values
#    year = ctl_year.value
#    lat = ctl_lat.value
#    lon = ctl_lon.value  
#    data_2 = pd.read_csv('./data/insolation_data_1983-2005_TEST.csv')
#    data_subset = data_2[(data_2.Year==year) & (data_2.Latitude==lat) & (data_2.Longitude==lon)]
#    x = np.array(list(range(1,13)))
#    y = np.array(list(data_subset.Insolation[0:12]))
#    #y = np.array(list(data_subset.Insolation[0:12]))
#    x_min = 0
#    x_max = 13
#    y_min = 0
#    y_max = 10
#    source_data.data = dict(x=x, y=y)
#    xrange_data.start = x_min
#    xrange_data.end = x_max
#    yrange_data.start = y_min
#    yrange_data.end = y_max

def update_sliders(attrname,new,old):
    # Get the current slider values
    year = ctl_year.value
    lat = ctl_lat.value
    lon = ctl_lon.value  
    #data_2 = pd.read_csv('./data/insolation_data_1983-2005_TEST_2.csv')
    #data_subset = data_2[(data_2.Year==year) & (data_2.Latitude==lat) & (data_2.Longitude==lon)]
    data_subset = d_data_2[(d_data_2.Year==year) & (d_data_2.Latitude==lat) & (d_data_2.Longitude==lon)]
    x = np.array(list(range(1,13)))
    #x=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    y = np.array(list(data_subset.Insolation[0:12]))
    #y = np.array(list(data_subset.Insolation[0:12]))
    x_min = 0
    x_max = 13
    y_min = -0.5
    y_max = 15
    source_data.data = dict(x=x, y=y)
    xrange_data.start = x_min
    xrange_data.end = x_max
    yrange_data.start = y_min
    yrange_data.end = y_max

# Button callbacks, using the above functions
#plot_update.on_click(update_plot)

ctl_lat.on_change('value',update_sliders)
ctl_lon.on_change('value',update_sliders)
ctl_year.on_change('value',update_sliders)

###-----------------------------------------------------------------------###
###----------------------------PAGE LAYOUT--------------------------------###
### This section defines the basic layout of the GUI. ("View" Part 3)     ###
###-----------------------------------------------------------------------###
#col_inputs = column(plot_ctls,ctl_inputs)
col_inputs = column(ctl_inputs)
col_plots = column(plot_data)
row_page = row(col_inputs, col_plots, width=1200)
curdoc().add_root(row_page)
curdoc().title = "Solar Insolation Data"