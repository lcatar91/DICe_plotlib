# -*- coding: utf-8 -*-
#
#=============================================================================
#IMPORT
#=============================================================================

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from PIL import Image
import PIL
import gif

#=============================================================================
#DATA IMPORTATION
#=============================================================================

def importation(nom):
    if nom<10:
        nom = '0' + str(nom)
    else:
        nom = str(nom)
    fic = open('DICe_solution_' + nom +'.txt', 'r')
    data = []
    while 1 :
        ligne = fic.readline()
        if ligne =="":
            break
        else:
            lg = ligne.split(',')
            data.append(lg)
    fic.close()
    
    del data[0:1] #delete title line
    
    Subset_ID = []
    x_coord, y_coord = [], []
    x_displ, y_displ = [], []
    sigma, gamma, beta = [], [], []
    status_flag = []
    uncert = []
    strain_xx, strain_yy, strain_xy = [], [], []
    
    
    for i in range(len(data)):
        L = data[i]
        Subset_ID.append(int(L[0]))
        x_coord.append(float(L[1]))
        y_coord.append(float(L[2]))
        x_displ.append(float(L[3]))
        y_displ.append(float(L[4]))
        sigma.append(float(L[5]))
        gamma.append(float(L[6]))
        beta.append(float(L[7]))
        status_flag.append(float(L[8]))
        uncert.append(float(L[9]))
        strain_xx.append(float(L[10]))
        strain_yy.append(float(L[11]))
        strain_xy.append(float(L[12]))
    return(x_coord, y_coord, x_displ, y_displ, sigma, gamma, beta, status_flag, uncert, strain_xx, strain_yy, strain_xy)

#=============================================================================

def lecture(num):
    text_num = str(num)
    x_coord, y_coord, x_displ, y_displ, sigma, gamma, beta, status_flag, uncert, strain_xx, strain_yy, strain_xy = importation(num)
    
    #eliminate the points where the tracking is lost (sigma = -1)
    for i in range(len(sigma)):
        if sigma[i] == -1:
            x_coord[i], y_coord[i], x_displ[i], y_displ[i], strain_xx[i], strain_yy[i], strain_xy[i] = 0, 0, 0, 0, 0, 0, 0
    
    #apply the displacements to the points to follow the strain
    for i in range(len(x_coord)):
        x_coord[i]=x_coord[i] + x_displ[i]
    
    for i in range(len(y_coord)):
        y_coord[i]=y_coord[i] + y_displ[i]
    
    e1 = []
    e2 = []
    theta = []
    emax = []
    for i in range(len(strain_xx)):
        if strain_xx[i]-strain_yy[i] != 0:
            theta_p = np.arctan(2*strain_xy[i]/(strain_xx[i]-strain_yy[i]))/2.
            theta.append(theta_p)
        else:
            theta.append(np.pi/2.)
        e1.append((strain_xx[i] + strain_yy[i])/2. + np.sqrt((((strain_xx[i] - strain_yy[i])/2)**2)+strain_xy[i]**2))
        e2.append((strain_xx[i] + strain_yy[i])/2. - np.sqrt((((strain_xx[i] - strain_yy[i])/2)**2)+strain_xy[i]**2))
        emax.append((e1[i]-e2[i])/2.)

    cmap = 'inferno'

    xmin, xmax = 850, 1150
    ymin, ymax = 250, 550
    w = xmax - xmin
    h = ymax - ymin
    
    plt.figure(dpi=600)
    image = PIL.Image.open('0_000'+ text_num +'.bmp')
    greyscale_img = image.convert(mode="LA", dither=Image.NONE)
    plt.imshow(greyscale_img)
    plt.scatter(x_coord, y_coord, c = e1, marker='.', s=1, alpha=1, norm=colors.SymLogNorm(linthresh=0.01, linscale=1, vmin=-0.1, vmax=0.85), cmap = cmap)
    rectangle = plt.Rectangle((xmin, ymin), w, h, fc='#1C00ff00', ec='white', lw=3)
    # plt.gca().add_patch(rectangle)
    plt.colorbar(orientation='horizontal')
    plt.axis('off')
    plt.savefig('BCC.png', dpi=600, bbox_inches='tight')
    plt.show()
    
    l = 10
    d = 4 #density of the arrows : 1 image on d
    u, v = [], []
    X, Y, E1 = x_coord, y_coord, e1
    x_coord = x_coord[::d]
    y_coord = y_coord[::d]
    x_displ = x_displ[::d]
    y_displ = y_displ[::d]
    theta = theta[::d]
    e1 = e1[::d]

    for i in range(len(theta)):
        u.append(l * np.cos(theta[i])*x_displ[i]/abs(x_displ[i]))
        v.append(l * np.sin(theta[i])*y_displ[i]/abs(y_displ[i]))
    plt.figure(dpi=600)
    plt.scatter(X, Y, c = E1, marker='.', s=50, alpha=1, norm=colors.SymLogNorm(linthresh=0.01, linscale=1, vmin=-0.1, vmax=0.85), cmap = cmap)
    for i in range(len(theta)):
        plt.arrow(x_coord[i], y_coord[i], u[i], v[i], head_width=2)
    
    plt.xlim(850,1150)
    plt.ylim(250,550)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.axis('off')
    plt.show()
    
lecture(53)

# frames = []
# for i in range(1,78):
#     frames.append(lecture(i))

# # Creating a gif with gif package
# gif.options.matplotlib["dpi"] = 300  # a decent resolution
    
# gif.save(frames, 'DIC.gif', duration=4, unit="s", between="startend")