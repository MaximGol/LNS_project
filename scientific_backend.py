import pickle
import numpy as np
from geopy import distance
from itertools import combinations
import matplotlib.pyplot as plt
import line_algebra_support as las
import rasterio
from itertools import filterfalse
import time


def dalnostPV (point1, point2, isPrint = False):# формула дальности прямой видимости
	ans = 4.12*(np.sqrt(point1.z)+np.sqrt(point2.z))
	if isPrint: print('Дальность прямой видимости между объектом c высотой',point1.z,'(м) и объектом с высотой ',point2.z, '(м):', ans, ' [км] ')
	return ans 

def getDalnost(point1, point2):
	return np.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2 )



def Pvhod(PG,d):#добвить (deltafc)  (deltaFp)
    Ga = 1
    lamda = (3*10**8)/float(1575.42*10**6)
    P = 10*np.log10((PG)*((Ga*(lamda**2))/((4*np.pi*d)**2)))
    #print(P)
    return P

def proverka_prim_vidimost(i):
    for j in LNS_point_list:#
        if dalnostPV(i,j,isPrint = False)<=  distance.great_circle((j.x,j.y), (i.x,i.y)).km:

            return True
    return False

def proverka_energ_dostupnost(i):   
    for j in LNS_point_list:
        #print(Pvhod(0.000000001, distance.great_circle((j.x,j.y), (i.x,i.y)).km ))
        
        if Pvhod(0.000000001, distance.great_circle((j.x,j.y), (i.x,i.y)).km ) <-143 and Pvhod(0.000000001, distance.great_circle((j.x,j.y), (i.x,i.y)).km )>-162.5  :
            return False
    return True
def geomFactor_m(sats, refPoint):
    naprCosine = np.zeros((3, len(sats)))
    for i in range(len(sats)):
        naprCosine[0][i] = (refPoint.x-sats[i].x)/getDalnost(refPoint, sats[i])
        naprCosine[1][i] = (refPoint.y-sats[i].y)/getDalnost(refPoint, sats[i])
        naprCosine[2][i] = (refPoint.z-sats[i].z)/getDalnost(refPoint, sats[i])
    print(naprCosine)
    try:
        res=np.matrix(np.dot(naprCosine, naprCosine.T)).I
    except: 
        return 7
    return np.sqrt(res[0,0]+res[1,1])

def geomFactor_d(sats, refPoint):# для градусов
    naprCosine = np.zeros((3, len(sats)))
    for i in range(len(sats)):
        #print((distance.great_circle((refPoint.x, 0), (sats[i].x,0)).m), 'metr')
        #print(distance.great_circle((refPoint.x, refPoint.y), (sats[i].x,sats[i].y)).m)
        #print((distance.great_circle((refPoint.x, 0), (sats[i].x,0)).m)/distance.great_circle((refPoint.x, refPoint.y), (sats[i].x,sats[i].y)).m)
        naprCosine[0][i] = (distance.great_circle((refPoint.x, 0), (sats[i].x,0)).m)/distance.great_circle((refPoint.x, refPoint.y), (sats[i].x,sats[i].y)).m
        naprCosine[1][i] = (distance.great_circle((refPoint.y, 0), (sats[i].y,0)).m)/distance.great_circle((refPoint.x, refPoint.y), (sats[i].x,sats[i].y)).m
        naprCosine[2][i] = (refPoint.z-sats[i].z)/distance.great_circle((refPoint.x, refPoint.y), (sats[i].x,sats[i].y)).m
    try:
        res=np.matrix(np.dot(naprCosine, naprCosine.T)).I
        #print(res)
        #print(np.sqrt(res[0,0]+res[1,1]))
    except: 
        return 7
    return np.sqrt(res[0,0]+res[1,1])

def add_Z(x,y):
    dataset = rasterio.open('3.tif')    
    band1 = dataset.read(1)
    row, col = dataset.index(x, y)
    return band1[row, col]

def draw_GF(NBS_grop, LNS_groop = []):
    itog_list = LNS_groop
    with open('Begin_LNS_point.pkl', 'rb') as fp:
        Begin_LNS_point = pickle.load(fp)

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
    

    count_dots_in_row = 20
    count_dots_in_colums =25
    distance_betwen_point_1_and_point_2 = las.distance_betwen_dots(point_1, point_2)
    for j in np.arange(point_1.y,point_4.y,-(point_1.y - point_4.y) / count_dots_in_row):
        local_point_1.y =j
        local_point_2.y =j
        itog_list.append(las.Point(local_point_1.x,local_point_1.y,add_Z(local_point_1.x,local_point_1.y)))
        for i in np.arange(0, distance_betwen_point_1_and_point_2, distance_betwen_point_1_and_point_2/count_dots_in_colums):
            m1 = distance_betwen_point_1_and_point_2 - i
            m2 = i
            x = (m2*local_point_1.x + m1*local_point_2.x) / (m1+m2)
            y = (m2*local_point_1.y + m1*local_point_2.y) / (m1+m2)
            itog_list.append(las.Point(x,y,add_Z(x,y)))

    distance_betwen_point_3_and_point_4 = las.distance_betwen_dots(point_3,point_4)
    for i in np.arange(0, distance_betwen_point_3_and_point_4, distance_betwen_point_3_and_point_4/count_dots_in_colums):
            m1 = distance_betwen_point_3_and_point_4 - i
            m2 = i
            x = (m2*local_point_3.x + m1*local_point_4.x) / (m1+m2)
            y = (m2*local_point_3.y + m1*local_point_4.y) / (m1+m2)
            itog_list.append(las.Point(x,y,add_Z(x,y)))
    
    itog_list.append(las.Point(local_point_3.x,local_point_3.y,add_Z(local_point_3.x,local_point_3.y)))
    #print(len(NBS_grop),'---------------------------------')
    #geomFactor(sats, refPoint):
    fig = plt.figure(figsize=(16, 6))
    ax = fig.add_subplot()
    for i in NBS_grop:
        ax.plot([i.x],[i.y], marker = 'o', color ='red')
    for i in itog_list:
        ans = geomFactor_d(NBS_grop, i)
        print(ans)
        if ans <= 1.5:
            ax.plot([i.x],[i.y], marker = 'o', color ='green')
        if ans > 1.5 and ans <= 3:
            ax.plot([i.x],[i.y], marker = 'o', color ='yellow')
        if ans > 3 and ans <= 5:
            ax.plot([i.x],[i.y], marker = 'o', color ='orange')
        if ans > 5 and ans <= 8:
            ax.plot([i.x],[i.y], marker = 'o', color ='orange')
        if ans > 8 :
            ax.plot([i.x],[i.y], marker = 'o', color ='red', alpha =0.9)
    plt.show()


def main():
    print('Алгоритм начал работу')
    #NBS_point_list=[]
    with open('NBS_point.pkl', 'rb') as fp:
        NBS_point_list = pickle.load(fp)
    #print(len(NBS_point_list))
    #LNS_point_list =[]
    with open('LNS_point.pkl', 'rb') as fp:
        LNS_point_list = pickle.load(fp)
    #print(LNS_point_list)
    #print(len(NBS_point_list))
    NBS_point_list[:] = filterfalse(proverka_prim_vidimost, NBS_point_list)
    #print(len(NBS_point_list))
    NBS_point_list[:] = filterfalse(proverka_energ_dostupnost, NBS_point_list)

    fig = plt.figure(figsize=(16, 6))
    ax = fig.add_subplot()
    count = 0
    NBS_GF_dict={}
    '''    #print(a)
    NBS_GF_dict={}
    count = 0
    for i in combinations(NBS_point_list, 3):
        count+=1
    print(count,'-------------------------------------------------------<')'''
    
    for i in combinations(NBS_point_list, 4):
        list_zn_gf = []
        count +=1
        a = [i[0], i[1], i[2]]
        #ax.plot([i[0].x, i[1].x, i[2].x],[i[0].y, i[1].y, i[2].y], marker = 'x', color ='red')
        cr_zn = 0
        for j in LNS_point_list:
            ax.plot([j.x],[j.y], marker = 'o', color ='blue')
            ans = geomFactor_d(a, j) 
            cr_zn += ans
            list_zn_gf.append(ans)
        cr_zn = cr_zn/len(LNS_point_list)
        
        NBS_GF_dict[(cr_zn)] = (i,list_zn_gf)
        
        print(count)
            
        if count == 500:
            break
    with open('NBS_GF_dict.pkl', 'wb') as fp:
            pickle.dump(NBS_GF_dict, fp)
    print('Вычисление завершились')
    
if __name__ == '__main__':
    main()
    #print(NBS_GF_dict.keys())
    #best_gf = [las.Point(NBS_GF_dict[min(NBS_GF_dict.keys())][0].x,NBS_GF_dict[min(NBS_GF_dict.keys())][0].y,5), las.Point(NBS_GF_dict[min(NBS_GF_dict.keys())][1].x,NBS_GF_dict[min(NBS_GF_dict.keys())][1].y,5), las.Point(NBS_GF_dict[min(NBS_GF_dict.keys())][2].x,NBS_GF_dict[min(NBS_GF_dict.keys())][2].y,5),las.Point(NBS_GF_dict[min(NBS_GF_dict.keys())][3].x,NBS_GF_dict[min(NBS_GF_dict.keys())][3].y,5)]
    #bed_gf = [las.Point(NBS_GF_dict[max(NBS_GF_dict.keys())][0].x,NBS_GF_dict[max(NBS_GF_dict.keys())][0].y,5), las.Point(NBS_GF_dict[max(NBS_GF_dict.keys())][1].x,NBS_GF_dict[max(NBS_GF_dict.keys())][1].y,5), las.Point(NBS_GF_dict[max(NBS_GF_dict.keys())][2].x,NBS_GF_dict[max(NBS_GF_dict.keys())][2].y,5),las.Point(NBS_GF_dict[max(NBS_GF_dict.keys())][3].x,NBS_GF_dict[max(NBS_GF_dict.keys())][3].y,5)]
 
    #best_gf = [las.Point([NBS_GF_dict[max(NBS_GF_dict.keys())][0].x],[NBS_GF_dict[max(NBS_GF_dict.keys())][0].y],5),las.Point([NBS_GF_dict[max(NBS_GF_dict.keys())][1].x],[NBS_GF_dict[max(NBS_GF_dict.keys())][1].y],5),las.Point([NBS_GF_dict[max(NBS_GF_dict.keys())][2].x],[NBS_GF_dict[max(NBS_GF_dict.keys())][2].y],5),las.Point([NBS_GF_dict[max(NBS_GF_dict.keys())][3].x],[NBS_GF_dict[max(NBS_GF_dict.keys())][3].y],5)]
    '''for i in NBS_GF_dict.keys():

        ax.plot([NBS_GF_dict[min(NBS_GF_dict.keys())][0].x],[NBS_GF_dict[min(NBS_GF_dict.keys())][0].y], marker = 'o', color ='red', alpha =0.9)
        ax.plot([NBS_GF_dict[min(NBS_GF_dict.keys())][1].x],[NBS_GF_dict[min(NBS_GF_dict.keys())][1].y], marker = 'o', color ='red', alpha =0.9)
        ax.plot([NBS_GF_dict[min(NBS_GF_dict.keys())][2].x],[NBS_GF_dict[min(NBS_GF_dict.keys())][2].y], marker = 'o', color ='red', alpha =0.9)
        #ax.plot([NBS_GF_dict[min(NBS_GF_dict.keys())][3].x],[NBS_GF_dict[min(NBS_GF_dict.keys())][3].y], marker = 'o', color ='red', alpha =0.9)

        ax.plot([NBS_GF_dict[max(NBS_GF_dict.keys())][0].x],[NBS_GF_dict[max(NBS_GF_dict.keys())][0].y], marker = 'o', color ='green', alpha =0.9)
        ax.plot([NBS_GF_dict[max(NBS_GF_dict.keys())][1].x],[NBS_GF_dict[max(NBS_GF_dict.keys())][1].y], marker = 'o', color ='green', alpha =0.9)
        ax.plot([NBS_GF_dict[max(NBS_GF_dict.keys())][2].x],[NBS_GF_dict[max(NBS_GF_dict.keys())][2].y], marker = 'o', color ='green', alpha =0.9)
        #ax.plot([NBS_GF_dict[max(NBS_GF_dict.keys())][3].x],[NBS_GF_dict[max(NBS_GF_dict.keys())][3].y], marker = 'o', color ='green', alpha =0.9)

    plt.show()'''
    '''NBS_groop =[las.Point(4500,1000,5), las.Point(5500,1000,5), las.Point(4500,3000,5), las.Point(10000,3000,5)]
    LNS_groop = []
    for i in range(0,10000,500):
        for j in range(5000,20000,500):
            LNS_groop.append(las.Point(i,j,1000))
    print(LNS_groop)
    for i in NBS_groop:
        print(i)
    draw_GF(NBS_groop,LNS_groop)'''

    '''for i in NBS_GF_dict[min(NBS_GF_dict.keys())]:
        NBS_groop.append(i)'''
    #las.Point(39.0895,51.60,5), las.Point(39.1060,51.6212,5)
    '''NBS_groop =[las.Point(39.0895,51.60,5), las.Point(39.17,51.61,5), las.Point(39.1649,51.6197,5), las.Point(39.1809,51.5993,5)]
    
    
    #print(LNS_point_list)
    with open('LNS_point.pkl', 'rb') as fp:
        LNS_point_list = pickle.load(fp)
    for i in LNS_point_list:
        print(i)
    fig = plt.figure(figsize=(16, 6))
    ax = fig.add_subplot()
    for i in LNS_point_list:
        ax.plot([i.x],[i.y], marker = 'o', color ='red')

    with open('Begin_LNS_point.pkl', 'rb') as fp:
        LNS_point_list = pickle.load(fp)
    for i in LNS_point_list:
        print(i,'---')
    for i in LNS_point_list:
        ax.plot([i.x],[i.y], marker = 'o', color ='blue')
    #print(LNS_point_list)
    LNS_groop = []
    plt.show()
    print(type(NBS_groop))
    print(type(best_gf))
    for i in NBS_groop:
        print(i)

    draw_GF(bed_gf,LNS_point_list)
    draw_GF(best_gf,LNS_point_list)'''
    '''z = las.Point(x=39.07936375597855,y=51.6474822093914,z=103)
    a = (distance.great_circle((z.x, 0), (NBS_groop[0].x,0)).m)/distance.great_circle((z.x, z.y), (NBS_groop[0].x,NBS_groop[0].y)).m
    q = best_gf[0]
    q1 = NBS_groop[0]
    print(q,q1)
    a = (distance.great_circle((z.x, 0), (best_gf[0].x,0)).m)/distance.great_circle((z.x, z.y), (best_gf[0].x,best_gf[0].y)).m
    '''        
    #ax.plot(, NBS_GF_dict[min(NBS_GF_dict.keys())][1].x, NBS_GF_dict[min(NBS_GF_dict.keys())][2].x],[NBS_GF_dict[min(NBS_GF_dict.keys())][0].y, NBS_GF_dict[min(NBS_GF_dict.keys())][1].y, NBS_GF_dict[min(NBS_GF_dict.keys())][2].y], marker = 'x', color ='red')
    #plt.draw()
    #plt.show()