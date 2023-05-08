
import asyncio
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtCore, QtGui, QtWidgets

import pylab
import json
from matplotlib.widgets import Button
import rasterio
from rasterio.plot import show
import numpy as np
import matplotlib.pyplot as plt
from mpl_point_clicker import clicker
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import pickle
import line_algebra_support as las
from geopy import distance
import matplotlib as mpl
import qdarkstyle
import scientific_backend 

def add_Z(x,y):
    dataset = rasterio.open('3.tif')    
    band1 = dataset.read(1)
    row, col = dataset.index(x, y)
    return band1[row, col]

def addDots(ax, point_1, point_2, point_3, point_4,color):
    list_with_dots=[]

    distance_betwen_point_1_and_point_2 = las.distance_betwen_dots(point_1,point_2)

    local_point_1 = point_1
    local_point_2 = point_2
    local_point_3 = point_3
    local_point_4 = point_4

    count_dots_in_row = 5
    count_dots_in_colums =5
    
    for j in np.arange(point_1.y,point_4.y,-(point_1.y - point_4.y) / count_dots_in_row):
        local_point_1.y =j
        local_point_2.y =j
        ax.plot([local_point_1.x],[local_point_1.y], marker = 'o', color =color)
        list_with_dots.append(las.Point(local_point_1.x,local_point_1.y,add_Z(local_point_1.x,local_point_1.y)))
        for i in np.arange(0, distance_betwen_point_1_and_point_2, distance_betwen_point_1_and_point_2/count_dots_in_colums):

            m1 = distance_betwen_point_1_and_point_2 - i
            m2 = i
            x = (m2*local_point_1.x + m1*local_point_2.x) / (m1+m2)
            y = (m2*local_point_1.y + m1*local_point_2.y) / (m1+m2)
            ax.plot([x],[y], marker = 'o', color =color)
            list_with_dots.append(las.Point(x,y,add_Z(x,y)))
            plt.draw()


    distance_betwen_point_3_and_point_4 = las.distance_betwen_dots(point_3,point_4)
    for i in np.arange(0, distance_betwen_point_3_and_point_4, distance_betwen_point_3_and_point_4/count_dots_in_colums):
            m1 = distance_betwen_point_3_and_point_4 - i
            m2 = i
            x = (m2*local_point_3.x + m1*local_point_4.x) / (m1+m2)
            y = (m2*local_point_3.y + m1*local_point_4.y) / (m1+m2)
            ax.plot([x],[y], marker = 'o', color =color)
            list_with_dots.append(las.Point(x,y,add_Z(x,y)))
            plt.draw()

    ax.plot([local_point_3.x],[local_point_3.y], marker = 'o', color =color)
    list_with_dots.append(las.Point(local_point_3.x,local_point_3.y,add_Z(local_point_3.x,local_point_3.y)))

    if color == 'red':
        with open('NBS_point.pkl', 'wb') as fp:
            pickle.dump(list_with_dots, fp)

    if color == 'blue':
        with open('LNS_point.pkl', 'wb') as fp:
            pickle.dump(list_with_dots, fp)


def draw_GF(NBS_groop, itog_list):
        
    for i in itog_list:
        ans = scientific_backend.geomFactor_d(NBS_groop, i)
        print('i work')
        markersize = 10
        if ans <= 1.5:
            ax.plot([i.x],[i.y], marker = 'o', color ='lime',markersize=markersize, alpha =0.5)
        if ans > 1.5 and ans <= 3:
            ax.plot([i.x],[i.y], marker = 'o', color ='limegreen',markersize=markersize, alpha =0.5)
        if ans > 3 and ans <= 5:
            ax.plot([i.x],[i.y], marker = 'o', color ='yellowgreen',markersize=markersize, alpha =0.5)
        if ans > 5 and ans <= 8:
            ax.plot([i.x],[i.y], marker = 'o', color ='yellow',markersize=markersize, alpha =0.5)
        if ans > 8 and ans <=15 :
            ax.plot([i.x],[i.y], marker = 'o', color ='orange', markersize=markersize, alpha =0.5)
        if ans > 15 and ans <=30 :
            ax.plot([i.x],[i.y], marker = 'o', color ='orangered',markersize=markersize, alpha =0.5)
        if ans > 30 and ans <=35 :
            ax.plot([i.x],[i.y], marker = 'o', color ='red', markersize=markersize, alpha =0.5)
        if ans > 35 and ans <=40 :
            ax.plot([i.x],[i.y], marker = 'o', color ='darkred', markersize=markersize, alpha =0.5)
        if ans > 40 :
            ax.plot([i.x],[i.y], marker = 'o', color ='black', markersize=markersize, alpha =0.5)
    plt.draw()




class Index:
    def write_NBS(self, event):
        
        list_with_dots = []
        for i in (klicker.get_positions()["НБС"]): 
            print(las.Point(i[0], i[1]))
            list_with_dots.append(las.Point(i[0], i[1]))
     
        with open('NBS_point_hand.pkl', 'wb') as fp:
            pickle.dump(list_with_dots, fp)
        print('Значение НБС задано')
        
        
    def write_LNS_zone(self, event):
        global ax
        list_of_dots = []
        for i in (klicker.get_positions()["Зона ЛНС"]): 
            list_of_dots.append(list(i))
        point_1 = las.Point(list_of_dots[0][0],list_of_dots[0][1])
        point_4 = las.Point(list_of_dots[1][0],list_of_dots[1][1])
        point_2 = las.Point(point_4.x, point_1.y)
        point_3 = las.Point(point_1.x, point_4.y)
        point_list = [point_1, point_2, point_3,point_4]
        with open('Begin_LNS_point.pkl', 'wb') as fp:
            pickle.dump(point_list, fp)
        print('Значение зоны ЛНС задано')

        

    def distance_betwen_dots(self, event):
        global ax
        list_of_dots = []
        for i in (klicker.get_positions()["Растояние между точками"]): 
            list_of_dots.append(list(i))
        point_1 = las.Point(list_of_dots[-2][0],list_of_dots[-2][1])
        point_2 = las.Point(list_of_dots[-1][0],list_of_dots[-1][1])
        
        print(distance.great_circle((point_1.x,point_1.y), (point_2.x,point_2.y)).km)
        ax.set(title=f'Растояние между точками {distance.great_circle((point_1.x,point_1.y), (point_2.x,point_2.y)).km} км')
        plt.draw()        
        #ax1.set_title('Above example with clear() function') 
        #plt.show()

    def bild_landscape_profile(self, event):
        list_of_dots = []
        for i in klicker.get_positions()["Профиль местности"]: 
            list_of_dots.append(list(i))
        global ax
        point_1 = las.Point(list_of_dots[-2][0],list_of_dots[-2][1])
        point_2 = las.Point(list_of_dots[-1][0],list_of_dots[-1][1])
        count_dots_in_colums = int(distance.great_circle((point_1.x,point_1.y), (point_2.x,point_2.y)).km / 0.01)
        distance_betwen_point_1_and_point_2 = las.distance_betwen_dots(point_1,point_2)
        print(count_dots_in_colums)
        print(distance.great_circle((point_1.x,point_1.y), (point_2.x,point_2.y)).km)        
        list_with_dots = []
        for i in np.arange(0, distance_betwen_point_1_and_point_2, distance_betwen_point_1_and_point_2/count_dots_in_colums):
            m1 = distance_betwen_point_1_and_point_2 - i
            m2 = i
            x = (m2*point_1.x + m1*point_2.x) / (m1+m2)
            y = (m2*point_1.y + m1*point_2.y) / (m1+m2)
            ax.plot([x],[y], marker = 'o', color ='red')
            list_with_dots.append(las.Point(x,y))
            plt.draw()

        dataset = rasterio.open('3.tif')
        list_with_dots.reverse()
        X = []
        Y = []
        band1 = dataset.read(1)
        for i in list_with_dots:
            x,y =i.x,i.y
            row, col = dataset.index(x, y)
            X.append(band1[row, col])
        for i in range(len(list_with_dots)):
            Y.append((i*100)/10000)

        fig2 = plt.figure()
        plt.plot(Y,X)
        plt.show()
    
    def calc_GF(self, event):
        
        with open('NBS_point_hand.pkl', 'rb') as fp:
            NBS_groop= pickle.load(fp)

        itog_list_LNS = []

        with open('Begin_LNS_point.pkl', 'rb') as fp:
            Begin_LNS_point = pickle.load(fp)
        print('_____________________________________')
        point_1 = Begin_LNS_point[0]
        point_2 = Begin_LNS_point[1]
        point_3 = Begin_LNS_point[2]
        point_4 = Begin_LNS_point[3]
        print(point_1)
        print(point_2)
        print(point_3)
        print(point_4)
        local_point_1 = Begin_LNS_point[0]
        local_point_2 = Begin_LNS_point[1]
        local_point_3 = Begin_LNS_point[2]
        local_point_4 = Begin_LNS_point[3]
        

        count_dots_in_row = 5
        count_dots_in_colums =5
        distance_betwen_point_1_and_point_2 = las.distance_betwen_dots(point_1, point_2)
        for j in np.arange(point_1.y,point_4.y,-(point_1.y - point_4.y) / count_dots_in_row):
            local_point_1.y =j
            local_point_2.y =j
            print('_____________________________________')
            itog_list_LNS.append(las.Point(local_point_1.x,local_point_1.y,add_Z(local_point_1.x,local_point_1.y)))
            for i in np.arange(0, distance_betwen_point_1_and_point_2, distance_betwen_point_1_and_point_2/count_dots_in_colums):
                m1 = distance_betwen_point_1_and_point_2 - i
                m2 = i
                x = (m2*local_point_1.x + m1*local_point_2.x) / (m1+m2)
                y = (m2*local_point_1.y + m1*local_point_2.y) / (m1+m2)
                itog_list_LNS.append(las.Point(x,y,add_Z(x,y)))

        distance_betwen_point_3_and_point_4 = las.distance_betwen_dots(point_3,point_4)
        for i in np.arange(0, distance_betwen_point_3_and_point_4, distance_betwen_point_3_and_point_4/count_dots_in_colums):
                m1 = distance_betwen_point_3_and_point_4 - i
                m2 = i
                x = (m2*local_point_3.x + m1*local_point_4.x) / (m1+m2)
                y = (m2*local_point_3.y + m1*local_point_4.y) / (m1+m2)
                itog_list_LNS.append(las.Point(x,y,add_Z(x,y)))
        
        itog_list_LNS.append(las.Point(local_point_3.x,local_point_3.y,add_Z(local_point_3.x,local_point_3.y)))
        print('_____________________________________')
        draw_GF(NBS_groop,itog_list_LNS )

    def draw_energ(self, event):
        with open('NBS_point_hand.pkl', 'rb') as fp:
            NBS_groop= pickle.load(fp)
        print(NBS_groop)
        for i in NBS_groop:
            ax.plot([i.x],[i.y], marker = 'o', color ='red', markersize=200, alpha =0.2)
        plt.draw()
            
        


if __name__ == "__main__":
    fig = plt.figure(figsize=(16, 6))
    img = rasterio.open('3.tif')
    callback = Index()
    
    ax2 = fig.add_axes([0.84, 0.6, 0.15, 0.1])#	[left, bottom, width, height]
    axNBS_zone = fig.add_axes(ax2)
    bNBS_zone = Button(axNBS_zone, 'Задать НБС')
    bNBS_zone.on_clicked(callback.write_NBS)

    ax3 = fig.add_axes([0.84, 0.5, 0.15, 0.1])
    axLNS_zone = fig.add_axes(ax3)
    bLNS_zone = Button(axLNS_zone, 'Задать зону ЛНС')
    bLNS_zone.on_clicked(callback.write_LNS_zone)

    ax4 = fig.add_axes([0.84, 0.4, 0.15, 0.1])
    axgf = fig.add_axes(ax4)
    bgf = Button(axgf, 'Расчитать ГФ')
    bgf.on_clicked(callback.calc_GF)

    ax5 = fig.add_axes([0.84, 0.3, 0.15, 0.1])
    axDistance_betwen_dots = fig.add_axes(ax5)
    bDistance_betwen_dots = Button(axDistance_betwen_dots, 'Растояние м/у точками')
    bDistance_betwen_dots.on_clicked(callback.distance_betwen_dots)

    ax6 = fig.add_axes([0.84, 0.2, 0.15, 0.1])
    axpm = fig.add_axes(ax6)
    bpm = Button(axpm, 'Построить профиль местности')
    bpm.on_clicked(callback.bild_landscape_profile)

    ax7 = fig.add_axes([0.84, 0.1, 0.15, 0.1])
    axenerg = fig.add_axes(ax7)
    benerg = Button(axenerg, 'Показать энерогопотенциал')
    benerg.on_clicked(callback.draw_energ)
    

    ax_color_bar = fig.add_axes([0.1, 0.3, 0.05, 0.5])
    cmap = mpl.colors.ListedColormap(['lime', 'limegreen', 'yellowgreen', 'yellow','orange','darkorange','orangered', 'red', 'darkred','black' ])

    cmap.set_over('red')
    cmap.set_under('blue')

    bounds = [1.5, 3, 5,8,15,30, 35,40,45,50]
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    cb3 = mpl.colorbar.ColorbarBase(ax_color_bar, cmap=cmap,
                                    norm=norm,
                                    boundaries=[-10] + bounds + [10],
                                    extend='both',
                                    extendfrac='auto',
                                    ticks=bounds,
                                    spacing='uniform',
                                    orientation='vertical')
    cb3.set_label('Значение геометрического фактора')
    ax = fig.add_subplot()
    img = rasterio.open('3.tif')

    klicker = clicker(ax, ["НБС", "Зона ЛНС", "Растояние между точками", "Профиль местности"], markers=["x", "o", "*", "+"],colors=['red','blue','yellow','orange'])
    show(img)

