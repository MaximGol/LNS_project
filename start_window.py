import numpy as np
import matplotlib.pyplot as plt
from matplotlib import backend_bases 
from matplotlib.widgets import Button,RadioButtons, CheckButtons
from PIL import Image
import rasterio
from rasterio.plot import show
from mpl_point_clicker import clicker
import sys
import matplotlib.backend_bases


select_way_list=[]
def link(val):
        global fig

        fig.clear('all')
        plt.clf()
        
        fig.draw()
        print('hgkgkghhj')
        '''ax1 = fig.subplots()
        ax1.imshow(Image.open(list_img[0]))
        plt.subplots_adjust(left = 0.35, bottom=0.1)

        # --- RADIO BUTTONS---
        ax_color1 = plt.axes([0.011, 0.54, 0.31, 0.31])
        image_button1 = RadioButtons(ax_color1,['1"', '2'], active=0, activecolor='blue')
        image_button1.on_clicked(change_image)

        plt.ioff()'''
        
        '''fig1 = plt.figure(2)
        axes1 = fig1.subplots()
        img = rasterio.open('3.tif')
        
        
        
        klicker = clicker(axes1, ["Зона НБС", "Зона ЛНС", "Растояние между точками", "Профиль местности"], markers=["x", "o", "*", "+"],colors=['red','blue','yellow','yellow'])
        show(img)'''
'''print(select_way_list)
        fig1 = plt.figure(figsize=(8, 5))
        fig1.suptitle('Different types of oscillations', fontsize=16)
        ax = fig.subplots()
        plt.show()'''

def change_image(label):        
        index = labels.index(label)
        ax.imshow(Image.open(list_img[index]))
        fig.canvas.draw()

def select_way(label):
    global select_way_list
    index = check_labels.index(label)
    select_way_list.append(index)
    return index


if __name__ == "__main__":
    list_img = ['LNS.jpg','Leica_Geosystems_LocataLite.webp']
    labels = ['ЛНС "СТЦ"', 'ЛНС "LocateNET']

    fig = plt.figure(figsize=(8, 5))
    ax = fig.subplots()
    ax.imshow(Image.open(list_img[0]))
    plt.subplots_adjust(left = 0.35, bottom=0.1)

    # --- RADIO BUTTONS---
    ax_color = plt.axes([0.01, 0.55, 0.3, 0.3])
    image_button = RadioButtons(ax_color,['ЛНС "СТЦ"', 'ЛНС "LocateNET'], active=0, activecolor='blue')
    image_button.on_clicked(change_image)

    #-----CHECK BUTTON---
    check_labels = ['','-' ]
    ax_check = plt.axes([0.01, 0.1, 0.3, 0.4])
    txt = ax_check.text(-0.03, 0.01, 'Ручной способ расстановки ЛНС', ha='left', rotation=0, wrap=True)
    txt._get_wrap_line_width = lambda : 200
    txt = ax_check.text(-0.03, -0.035, 'Автоматический способ расстановки ЛНС', ha='left', rotation=0, wrap=True)
    txt._get_wrap_line_width = lambda : 200
    way_button = RadioButtons(ax_check,['', '-'], active=0, activecolor='blue')
    way_button.on_clicked(select_way)#select_way

    #---BUTTON---


    ax_start_button = plt.axes([0.5,0.01,0.3, 0.05])
    #xposition, yposition, width, height

    start_button = Button(ax_start_button, 'Начать работу', color ='white', hovercolor = 'grey')
    start_button.on_clicked(link)

    plt.show(block=True)


''' ax_button = plt.axes([0.01,0.01,0.3, 0.05])
    #xposition, yposition, width, height

    link_button = Button(ax_button, 'Выбрать карту', color ='white', hovercolor = 'grey')
    link_button.on_clicked(link)'''