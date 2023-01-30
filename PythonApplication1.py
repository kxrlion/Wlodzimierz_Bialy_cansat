from cmath import pi, sqrt
from pickle import FALSE, TRUE
from random import gauss
from subprocess import list2cmdline
from telnetlib import GA
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math
import webbrowser
import urllib


from time import time
from time import sleep
from urllib.request import urlopen
from matplotlib import style
from PIL import Image , ImageEnhance
from PIL import ImageGrab

#url= "https://earth.google.com/web/@64.75516033,20.52919838,118.72567778a,3230.44707272d,35y,16.10564206h,0t,0r"

#webbrowser.open_new(url)
#website = urlopen(url)
#sleep(10)

#ss=ImageGrab.grab()
#save_path = "C:\\Users\\kxrli\\source\\repos\\PythonApplication1\\ss.jpg"
#ss.save(save_path)

img = Image.open('example.jpg')
img = img.convert("HSV")
width,height = img.size;
pixel_access_object = img.load();

kernel_blur = ((1,2,1),(2,8,2),(1,2,1))
kernel_edge_detection_y = ((1,0,-1),(2,0,-2),(1,0,-1))
kernel_edge_detection_x = ((-1,-2,-1),(0,0,0),(1,2,1)) 





#blur gausowski: do wygladzania obrazu(aby lepiej dzialaly inne czesci)
def gaussian_blur(pix_acc_obj,ile):
    pix_val=[0,0,0]
    #print(pix_acc_obj[0,0][0])
    #a=10
    #b=10
    #print(int((pix_acc_obj[a-1,b-1][0]*kernel_blur[0][0])) )
    for i in range(ile):
        for j in range(1,height-2):
            for i in range(1,width-2):
                pix_val[0]=int((pix_acc_obj[i-1,j-1][0]*kernel_blur[0][0]+pix_acc_obj[i,j-1][0]*kernel_blur[1][0]+ pix_acc_obj[i+1,j-1][0]*kernel_blur[2][0]+ pix_acc_obj[i-1,j][0]*kernel_blur[0][1]+ pix_acc_obj[i,j][0]*kernel_blur[1][1]+ pix_acc_obj[i+1,j][0]*kernel_blur[2][1]+ pix_acc_obj[i-1,j+1][0]*kernel_blur[0][2]+ pix_acc_obj[i,j+1][0]*kernel_blur[1][2]+ pix_acc_obj[i+1,j+1][0]*kernel_blur[2][2])/20)
                #print(pix_val)
                pix_val[1]=int((int(pix_acc_obj[i-1,j-1][1])*kernel_blur[0][0]+ int(pix_acc_obj[i,j-1][1])*kernel_blur[1][0]+ int(pix_acc_obj[i+1,j-1][1])*kernel_blur[2][0]+ int(pix_acc_obj[i-1,j][1])*kernel_blur[0][1]+ int(pix_acc_obj[i,j][1])*kernel_blur[1][1]+ int(pix_acc_obj[i+1,j][1])*kernel_blur[2][1]+ int(pix_acc_obj[i-1,j+1][1])*kernel_blur[0][2]+ int(pix_acc_obj[i,j+1][1])*kernel_blur[1][2]+ int(pix_acc_obj[i+1,j+1][1])*kernel_blur[2][2])/20)
                pix_val[2]=int((int(pix_acc_obj[i-1,j-1][2])*kernel_blur[0][0]+ int(pix_acc_obj[i,j-1][2])*kernel_blur[1][0]+ int(pix_acc_obj[i+1,j-1][2])*kernel_blur[2][0]+ int(pix_acc_obj[i-1,j][2])*kernel_blur[0][1]+ int(pix_acc_obj[i,j][2])*kernel_blur[1][1]+ int(pix_acc_obj[i+1,j][2])*kernel_blur[2][1]+ int(pix_acc_obj[i-1,j+1][2])*kernel_blur[0][2]+ int(pix_acc_obj[i,j+1][2])*kernel_blur[1][2]+ int(pix_acc_obj[i+1,j+1][2])*kernel_blur[2][2])/20)
                pix_acc_obj[i,j] = tuple(pix_val)


#wykrywanie krawedzi(self explanatory)
def edge_detection(pix_acc_obj,img):
    img = img.convert("L")
    pix_acc_obj = img.load()
    #img.show()
    temp_x=[]
    temp_y=[]
    is_edge=[]
    
    
    
    for j in range(width):
        temp_temp_x=[]
        temp_temp_y=[]
        is_edge_temp=[]
        for i in range(height):
            temp_temp_x.append(0)
            temp_temp_y.append(0)
            is_edge_temp.append(FALSE)
        temp_x.append(temp_temp_x)
        temp_y.append(temp_temp_y)
        is_edge.append(is_edge_temp)

    for j in range(1,height-2):
        for i in range(1,width-2):
            temp_x[i][j]=(pix_acc_obj[i-1,j-1]*kernel_edge_detection_x[0][0])+(pix_acc_obj[i+1,j-1]*kernel_edge_detection_x[2][0])+(pix_acc_obj[i-1,j]*kernel_edge_detection_x[0][1])+(pix_acc_obj[i+1,j]*kernel_edge_detection_x[2][1])+(pix_acc_obj[i-1,j+1]*kernel_edge_detection_x[0][2])+(pix_acc_obj[i+1,j+1]*kernel_edge_detection_x[2][2]) 
            
            temp_y[i][j]=(pix_acc_obj[i-1,j-1]*kernel_edge_detection_y[0][0])+(pix_acc_obj[i,j-1]*kernel_edge_detection_y[1][0])+(pix_acc_obj[i+1,j-1]*kernel_edge_detection_y[2][0])+(pix_acc_obj[i-1,j+1]*kernel_edge_detection_y[0][2])+(pix_acc_obj[i,j+1]*kernel_edge_detection_y[1][2])+(pix_acc_obj[i+1,j+1]*kernel_edge_detection_y[2][2])
    for j in range(1,height-2):
        for i in range(1,width-2):
            if int(sqrt(pow(temp_x[i][j],2)+pow(temp_y[i][j],2) ).real) > 60:
                is_edge[i][j]=1
            else:
                is_edge[i][j]=0
    img = img.convert("HSV")
    return is_edge
     
#tworzenie mapki
def to_map(pix_acc_obj):
    #PIL uzywa jednostek 0-255 a HSV 0-360 i to jest mniej wiecej mnoznik dla H
    PIL_H_converter = 0.7083333
    #to mnoznik dla S lub V
    PIL_S_V_converter = 2.55
    #print(150 * PIL_H_converter)
    #woda h-150-255 
    H_woda_D = int(150 * PIL_H_converter)
    H_woda_G = int(255 * PIL_H_converter)
    #budynki s<5% i v<5% lub h <36 i >255
    H_budynki_D = int(36 * PIL_H_converter)
    H_budynki_G = int(255 * PIL_H_converter)
    S_budynki = int(5 * PIL_S_V_converter)
    V_budynki = int(5 * PIL_S_V_converter)
    #laki h-62-86
    H_laki_D = int(62 * PIL_H_converter)
    H_laki_G = int(86 * PIL_H_converter)
    #lasy h-86-150
    H_lasy_D = int(86 * PIL_H_converter)
    H_lasy_G = int(150 * PIL_H_converter)
    #piasek h-36-62 
    #H_piasek_D = int(36 * PIL_H_converter)
    #H_piasek_G = int(62 * PIL_H_converter)
    H_piasek_D = int(0 * PIL_H_converter)
    H_piasek_G = int(62 * PIL_H_converter)

    for j in range(height):
        for i in range(width):
            #woda
            if(pix_acc_obj[i,j][0]>H_woda_D and pix_acc_obj[i,j][0]<H_woda_G):
                pix_acc_obj[i,j] = (int(198 * PIL_H_converter),255,255)
            ##budynki
            #if((pix_acc_obj[i,j][0]<H_budynki_D and pix_acc_obj[i,j][0]>H_budynki_G) or (pix_acc_obj[i,j][1]<S_budynki or pix_acc_obj[i,j][2]<S_budynki)):
            #    pix_acc_obj[i,j] = (0,int(3 * PIL_S_V_converter),int(74 * PIL_S_V_converter))
            #laki
            if(pix_acc_obj[i,j][0]>H_laki_D and pix_acc_obj[i,j][0]<H_laki_G):
                pix_acc_obj[i,j] = (int(70 * PIL_H_converter),255,255)
            #lasy
            if(pix_acc_obj[i,j][0]>H_lasy_D and pix_acc_obj[i,j][0]<H_lasy_G):
                pix_acc_obj[i,j] = (int(120 * PIL_H_converter),255,255)
            #piasek
            if(pix_acc_obj[i,j][0]>H_piasek_D and pix_acc_obj[i,j][0]<H_piasek_G):
                pix_acc_obj[i,j] = (int(63 * PIL_H_converter),255,255)

#porownanie
def porownanie(pix_acc_obj1,pix_acc_obj2){
    
    
}


#img = ImageEnhance.Contrast(img).enhance(1.5)
#gaussian_blur(pixel_access_object,1)
is_edge=edge_detection(pixel_access_object,img)
#gaussian_blur(pixel_access_object,1)
to_map(pixel_access_object)
for j in range(1,height-2):
        for i in range(1,width-2):
            if(is_edge[i][j]==1):
               pixel_access_object[i,j]=(0,0,0)
#gaussian_blur(pixel_access_object,1)

img.show()

