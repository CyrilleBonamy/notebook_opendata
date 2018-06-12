from netCDF4 import Dataset
import requests
from lxml import etree
import numpy as np
import ipywidgets as widgets
from IPython.display import display, clear_output
import matplotlib.pyplot as plt

global base_url
global path
global select

base_url = 'http://servdap.legi.grenoble-inp.fr:80/opendap/'
path = base_url
select = widgets.Select(
                        options=['.', '..'],
                        value='.',
                        description='Select a file or folder',
                        disabled=False
                        )

global loadedfiles
loadedfiles = [[],[]]

def g(button, variable, vector):
    global path
    global base_url
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
        
    options = ['.', '..']
    
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
        
        plot_func(variable, rootgrp, vector)
        plt.show()
        
def plot_func(variable, rootgrp, vector):
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
    xlin = np.linspace(0, len(rootgrp.variables['lon'])-1, len(rootgrp.variables['lon']))
    x, y = np.meshgrid(xlin, xlin)
    if variable == 'norm':
        norm = np.sqrt(rootgrp.variables['u'][0, 0, :, :]**2 +
                       rootgrp.variables['v'][0, 0, :, :]**2)
        mycontour = plt.contourf(norm, 50, cmap=contourcolor)
        cbar = plt.colorbar(mycontour)
        cbar.ax.set_ylabel('norm (m/s)')
    else:
        varplot = rootgrp.variables[variable][0, 0, :, :]
        mycontour = plt.contourf(varplot, 50, cmap=contourcolor)
        cbar = plt.colorbar(mycontour)
        cbar.ax.set_ylabel(rootgrp.variables[variable].name +
                           " (" + rootgrp.variables[variable].units + ")")
    if vector:
        plt.quiver(x, y, rootgrp.variables['u'][0, 0, :, :],
                   rootgrp.variables['v'][0, 0, :, :])

def plot_field():
    
    display(select)

    widgets.interact(g,
                     button=widgets.ToggleButton(
                                                 value=False,
                                                 description='Select',
                                                 disabled=False,
                                                 button_style='', # 'success', 'info', 'warning', 'danger' or ''
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