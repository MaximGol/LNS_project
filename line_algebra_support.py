import numpy as np
import math
class Point:
    def __init__(self, x, y, z = 0):
        self.x = x
        self.y = y
        self.z = z
    def __str__(self):
        return "Point[x={},y={},z={}]".format(self.x, self.y,self.z)

class Segment:
    def __init__(self,start_point, end_point, angle = 'None',energy_potential = 0,Ko = 0 ):

        self.start_point = start_point   
        self.end_point = end_point
        self.angle = angle
        self.energy_potential = energy_potential
        self.Ko = Ko

    def __str__(self):
        return "Segment[start={},end={},angle_on_Earth = {},energy_potential={}, Ko ={} ]".format(self.start_point, self.end_point,self.angle,self.energy_potential,self.Ko )
class Algebra_vector:
			def __init__(self, point1, point2):
				self.vector  = (point2.x - point1.x, point2.y - point1.y)
				self.x = point2.x - point1.x
				self.y = point2.y - point1.y
class Vector:
    def __init__(self, start_point, end_point):
        self.start_point = start_point
        self.end_point = end_point
        self.x_component = end_point.x - start_point.x
        self.y_component = end_point.y - start_point.y
    def __str__(self):
        return "Vector[start={},end={}]".format(self.start_point, self.end_point)

def range_intersection(range_1_s, range_1_e, range_2_s, range_2_e):
    'проверка правильности подстановки начала и конца отрезка'
    if range_1_s > range_1_e:
        range_1_s,range_1_e = range_1_e,range_1_s
    if range_2_s > range_2_e:
        range_2_s,range_2_e = range_2_e,range_2_s
    return max(range_1_s,range_2_s) <=min(range_1_e,range_2_e)

def bounding_box(segment_1, segment_2):#попарное пересечение (натянутый параллелипипед)
    x1 = segment_1.start_point.x
    x2 = segment_1.end_point.x
    x3 = segment_2.start_point.x
    x4 = segment_2.end_point.x

    y1 = segment_1.start_point.x
    y2 = segment_1.end_point.x
    y3 = segment_2.start_point.x
    y4 = segment_2.end_point.x

    return range_intersection(x1,x2,x3,x4) and range_intersection(y1,y2,y3,y4)

def vector_cross_product(vector_1, vector_2):
    return vector_1.x_component * vector_2.y_component - vector_2.x_component * vector_1.y_component

def check_segmen_intersection(segment_1, segment_2):
    if not bounding_box(segment_1,segment_2):
        return False
    vector_ab = Vector(segment_1.start_point, segment_1.end_point) 
    vector_ac = Vector(segment_1.start_point, segment_2.start_point) 
    vector_ad = Vector(segment_1.start_point, segment_2.end_point)

    vector_cd = Vector(segment_2.start_point, segment_2.end_point) 
    vector_ca = Vector(segment_2.start_point, segment_1.start_point) 
    vector_cb = Vector(segment_2.start_point, segment_1.end_point)  

    d1 = vector_cross_product(vector_ab,vector_ac)
    d2 = vector_cross_product(vector_ab,vector_ad)
    d3 = vector_cross_product(vector_cd,vector_ca)
    d4 = vector_cross_product(vector_cd,vector_cb)

    if ((d1 <=0 and d2>=0) or (d1 >= 0 and d2<=0)) and ((d3 <=0 and d4>=0) or (d3 >= 0 and d4<=0)):
        return True
    return False
    

class Triangle:
    def __init__(self, vertex_1,vertex_2, vertex_3):
        self.vertex_1 = vertex_1
  
        self.vertex_2 = vertex_2
        self.vertex_3 = vertex_3
def __str__(self):
        return "Triangle[vertex_1={},vertex_2={},vertex_3 = {}]".format(self.vertex_1, self.vertex_2, self.vertex_3)

def hitting_the_triangle(point, triangle):
    product_1 = vector_cross_product(Vector(triangle.vertex_1, point),Vector(triangle.vertex_1, triangle.vertex_2))
    product_2 = vector_cross_product(Vector(triangle.vertex_2, point),Vector(triangle.vertex_2, triangle.vertex_3))
    product_3 = vector_cross_product(Vector(triangle.vertex_3, point),Vector(triangle.vertex_3, triangle.vertex_1))
    return ((product_1>=0 and product_2>=0 and product_3>=0) or (product_1 <=0 and product_2 <=0 and product_3 <=0))

def normalization_vector(point):# нормализация вектора |a|
    down = np.sqrt((point.x**2)+ (point.y**2))
    return Point(point.x /down, point.y /down )



def get_angle_betwen_vectors(segment1,segment2):#A•B = |A||B|cosΘ
    A = Point(segment1.start_point.x - segment1.end_point.x,segment1.start_point.y - segment1.end_point.y)
    B = Point(segment2.start_point.x - segment2.end_point.x,segment2.start_point.y - segment2.end_point.y)
    vector1 = normalization_vector(A)
    vector2 = normalization_vector(B)
    #return (math.acos(0.31)* (180/np.pi))
 
    return 180-round(math.acos((vector1.x * vector2.x)+ (vector1.y * vector2.y))* (180/np.pi))
    

def distance_betwen_dots(Point1, Point2):
    return np.sqrt((Point1.x - Point2.x)**2 + (Point1.y - Point2.y)**2)


def intersection_point(segment1,segment2):
    x1_1, y1_1 = segment1.start_point.x, segment1.start_point.y
    x1_2, y1_2 = segment1.end_point.x, segment1.end_point.y
    x2_1, y2_1 = segment2.start_point.x, segment2.start_point.y
    x2_2, y2_2 = segment2.end_point.x, segment2.end_point.y
    
    def point(x, y):
        if min(x1_1, x1_2) <= x <= max(x1_1, x1_2):
            #print('Точка пересечения отрезков есть, координаты: ({0:f}, {1:f}).'.format(x, y))
            return Point(x,y)
        else:
            #print(segment1.start_point, segment1.end_point)
            #print(segment2.start_point, segment2.end_point)
            #print('Точки пересечения отрезков нет.')
            return None
    
    A1 = y1_1 - y1_2
    B1 = x1_2 - x1_1
    C1 = x1_1*y1_2 - x1_2*y1_1
    A2 = y2_1 - y2_2
    B2 = x2_2 - x2_1
    C2 = x2_1*y2_2 - x2_2*y2_1
    
    if B1*A2 - B2*A1 and A1:
        y = (C2*A1 - C1*A2) / (B1*A2 - B2*A1)
        x = (-C1 - B1*y) / A1
        return point(x, y)
    elif B1*A2 - B2*A1 and A2:
        y = (C2*A1 - C1*A2) / (B1*A2 - B2*A1)
        x = (-C2 - B2*y) / A2
        point(x, y)
    else:
        pass#print('Точки пересечения отрезков нет, отрезки ||.')    

'''point_h = Point(-30,16)
point_g = Point(-30,15)
point_e = Point(0,0)

V = Segment(point_h,point_g)
D = Segment(point_e,point_g)

a = intersection_point(V,D)
print(a)'''

'''
a = Point(3,1)
b = Point(5,5)
c = Point(8,2)
triangle = Triangle(a,b,c)
o = Point(7,2)

print(hitting_the_triangle(o,triangle))
point_a = Point(1,2)
point_b = Point(3,3)
point_c = Point(1,1)
point_d = Point(4,3)
segment_1 = Segment(point_a,point_b)
segment_2 = Segment(point_c,point_d)
#print(check_segmen_intersection(segment_1,segment_2))


'''