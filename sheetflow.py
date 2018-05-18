import matplotlib.pyplot as plt
from netCDF4 import Dataset
import ipywidgets as widget


def g(variable, varmin, varmax, zmin, zmax):
    fig_xsize = 10
    fig_ysize = 10
    font_size = 25
    markersize = 10
    fig = plt.figure(num=0, figsize=(fig_xsize, fig_ysize), dpi=60,
                     facecolor='w', edgecolor='w')
    #xaxis_name = rootgrp.variables[variable1].name + " (" + rootgrp.variables[variable1].units + ")"
    yaxis_name = r'$z/d_p$'
    plt.rcParams.update({'font.size': font_size})
    plt.rcParams['lines.markersize'] = 10
    dp = rootgrp.variables['dp']
    z = rootgrp.variables['Z']
    plt.plot(rootgrp.variables[variable],
             z[:]/dp,
             'or',
             label= rootgrp.variables[variable].name + " (" + rootgrp.variables[variable].units + ")")
    
    plt.xlim(varmin, varmax)
    plt.ylim(zmin, zmax)
    plt.ylabel(yaxis_name)
    plt.legend()
    plt.show()

    
def plotexpe():
    global rootgrp
    file_name = "data_expe_mb1.nc"
    url_base = 'http://servdap.legi.grenoble-inp.fr:80/opendap/meige/15SHEET_FLOW/data_expe/'
    url = url_base + file_name
    rootgrp = Dataset(url)
    var = []
    for i in rootgrp.variables.keys():
        if len(rootgrp.variables[i]) == 90 and i != 'Z':
            var.append(i)
    
    print('Please select a variable to plot and plot axis dimensions:')
    widget.interact(g,
                    variable=var,
                    varmin=widget.BoundedFloatText(value=0,
                                                   min=-1,
                                                   max=1,
                                                   step=0.01,
                                                   description='varmin:',
                                                   disabled=False), 
                    varmax=widget.BoundedFloatText(value=1,
                                                   min=-1,
                                                   max=1,
                                                   step=0.01,
                                                   description='varmax:',
                                                   disabled=False),
                    zmin=widget.BoundedFloatText(value=-2,
                                                 min=-2,
                                                 max=30,
                                                 step=0.1,
                                                 description='zmin:',
                                                 disabled=False),
                    zmax=widget.BoundedFloatText(value=30,
                                                 min=-2,
                                                 max=30,
                                                 step=0.1,
                                                 description='zmax:',
                                                 disabled=False)
                   );
