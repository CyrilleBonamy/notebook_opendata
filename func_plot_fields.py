from netCDF4 import Dataset
import requests
from lxml import etree
import numpy as np
import ipywidgets as widgets
from IPython.display import display, clear_output
import matplotlib.pyplot as plt


def f(select, x_data, y_data, u_data, v_data):

    widgets.interact(g,
                     button=widgets.ToggleButton(value=False,
                                                 description='Select',
                                                 disabled=False,
                                                 button_style='',
                                                 tooltip='Description'
                                                ),
                     variable=widgets.ToggleButtons(options=['u', 'v', 'norm'],
                                                    description='Variable:',
                                                    disabled=False,
                                                    button_style='',
                                                   ),
                     vector=widgets.Checkbox(value=False,
                                             description='Display vectors',
                                             disabled=False
                                            ),
                     )


def g(button, variable, vector):
    global path
    global select
    value = select.value
    
    if value == '.':
        path = base_url
    elif value.endswith('.nc'):
        file = value
    else:
        path += value + '/'
    try:
        catalog_file = requests.get(path + 'catalog.xml')
        tree = etree.fromstring(catalog_file.content)
    except:
        path = base_url
        catalog_file = requests.get(path + 'catalog.xml')
        tree = etree.fromstring(catalog_file.content)
        
    options = ['', '.', '..']
    
    if not value.endswith('.nc'):
        for children in tree[2]:
            if children.get('ID').endswith('/') or children.get('ID').endswith('.nc'):
                options.append(children.get('name'))
        select.options = options 
    else:
        if value in loadedfiles[0]:
            rootgrp = loadedfiles[1][loadedfiles[0].index(value)]
        else:
            rootgrp = Dataset(path + file)
            loadedfiles[0].append(file)
            loadedfiles[1].append(rootgrp)
        datasets = rootgrp.variables
        datasets_name = ['choose a dataset']
        for i in datasets.keys():
            datasets_name.append(i)
        x_data.options = datasets_name
        y_data.options = datasets_name
        u_data.options = datasets_name
        v_data.options = datasets_name
        try:
            plot_func(variable, rootgrp, vector, x_data, y_data, u_data, v_data)
            plt.show()
        except:
            print('Invalid netCDF file or invalid dataset selection')

            
def plot_func(variable, rootgrp, vector, x_data, y_data, u_data, v_data):
    # Figure size
    fig_xsize = 15
    fig_ysize = 10
    font_size = 25
    fig = plt.figure(num=0, figsize=(fig_xsize, fig_ysize), dpi=60,
                     facecolor='w', edgecolor='w')
    plt.rcParams.update({'font.size': font_size})
    plt.gca().set_aspect('equal')
    #axis names
    xaxis_name = 'i'
    yaxis_name = 'j'
    plt.xlabel(xaxis_name)
    plt.ylabel(yaxis_name)
    contourcolor = plt.cm.coolwarm
    xlin = np.linspace(0, len(rootgrp.variables[x_data.value])-1, len(rootgrp.variables[x_data.value]))
    ylin = np.linspace(0, len(rootgrp.variables[y_data.value])-1, len(rootgrp.variables[y_data.value]))
    x, y = np.meshgrid(xlin, ylin)
    try:
        if variable == 'norm':
            norm = np.sqrt(rootgrp.variables[u_data.value][0, 0, :, :]**2 +
                           rootgrp.variables[v_data.value][0, 0, :, :]**2)
            mycontour = plt.contourf(norm, 50, cmap=contourcolor)
            cbar = plt.colorbar(mycontour)
            cbar.ax.set_ylabel('norm (m/s)')
        elif variable == 'u':
            varplot = rootgrp.variables[u_data.value][0, 0, :, :]
            mycontour = plt.contourf(varplot, 50, cmap=contourcolor)
            cbar = plt.colorbar(mycontour)
            cbar.ax.set_ylabel(rootgrp.variables[variable].name +
                               " (" + rootgrp.variables[u_data.value].units + ")")
        else:
            varplot = rootgrp.variables[v_data.value][0, 0, :, :]
            mycontour = plt.contourf(varplot, 50, cmap=contourcolor)
            cbar = plt.colorbar(mycontour)
            cbar.ax.set_ylabel(rootgrp.variables[variable].name +
                               " (" + rootgrp.variables[v_data.value].units + ")")            
        if vector:
            plt.quiver(x, y, rootgrp.variables[u_data.value][0, 0, :, :],
                       rootgrp.variables[v_data.value][0, 0, :, :])

    except:
        if variable == 'norm':
            norm = np.sqrt(rootgrp.variables[u_data.value][:, :]**2 +
                           rootgrp.variables[v_data.value][:, :]**2)
            mycontour = plt.contourf(norm, 50, cmap=contourcolor)
            cbar = plt.colorbar(mycontour)
            cbar.ax.set_ylabel('norm (m/s)')
        elif variable == 'u':
            varplot = rootgrp.variables[u_data.value][:, :]
            mycontour = plt.contourf(varplot, 50, cmap=contourcolor)
            cbar = plt.colorbar(mycontour)
            #cbar.ax.set_ylabel(rootgrp.variables[variable].name)
            #                   " (" + rootgrp.variables[u_data.value].units + ")")
        else:
            varplot = rootgrp.variables[v_data.value][:, :]
            mycontour = plt.contourf(varplot, 50, cmap=contourcolor)
            cbar = plt.colorbar(mycontour)
            #cbar.ax.set_ylabel(rootgrp.variables[variable].name)
            #                   " (" + rootgrp.variables[v_data.value].units + ")")            
        if vector:
            plt.quiver(x, y, rootgrp.variables[u_data.value][:, :],
                       variables[v_data.value][0, 0, :, :])
           
def plot_field():
    global base_url
    global path
    global select
    global x_data
    global y_data
    global u_data
    global v_data
    base_url = 'http://servdap.legi.grenoble-inp.fr:80/opendap/'
    path = base_url
    
    global loadedfiles
    loadedfiles = [[],[]]
    select = widgets.Select(
                            options=['.', '..'],
                            value='.',
                            description='Select a file or folder',
                            disabled=False
                            )
    x_data = widgets.Dropdown(
                             options=['choose a dataset'],
                             value='choose a dataset',
                             description='x',
                             disabled=False
                             )
    y_data = widgets.Dropdown(
                             options=['choose a dataset'],
                             value='choose a dataset',
                             description='y',
                             disabled=False
                             )
        
    u_data = widgets.Dropdown(
                             options=['choose a dataset'],
                             value='choose a dataset',
                             description='u',
                             disabled=False
                             )
    
    v_data = widgets.Dropdown(
                             options=['choose a dataset'],
                             value='choose a dataset',
                             description='v',
                             disabled=False
                             )
    widgets.interact(f, select=select, x_data=x_data, y_data=y_data, u_data=u_data, v_data=v_data)
