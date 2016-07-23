#!/usr/bin/env python3

"""
Конвертер гео-данных v1.00.01
2014-11-11

Конвертер предназначен для преобразования координат в файл DXF

формат файла настройки:
А,ББББББББББ.БББ
А,ББББББББББ.БББ

, где:
А - тип файла для преобразования
БББББББББ.БББ - имя файла с данными

Типы преобразования:
T - данные с тахеометра выводятся в файл DXF
G - данные с GPS выводятся в файл DXF
P - данные в формате тахеометра выводятся в полилинию в DXF файл
C - данные в формате тахеометра преобразуются в местную систему координат и выводятся в DXF файл.

"""


import sdxf
import math
import os

layerName = 'METKI01'
layerColor = 1
# 1-красный
# 2-желтый
# 3-зеленый
# 4-голубой
# 5-синий
# 6-розовый
# 7-черный
# 8-серый
# 9-светло-серый
# 10-красный
# 11-светло-красный

#---------------------------------------------------------------------------------------------
def metka(obj, x, y, txt, lay):
    #add drawing elements
    global num_block
    #размер текста
    HT=0.5
    #размер блока
    razmer=0.5
    num_block+=1
    name_block="block_"+str(txt)+"_"+str(num_block)
    bl = sdxf.Block(name_block)
    bl.append(sdxf.Text(txt,point=(razmer,0),layer=lay,height=HT))
    bl.append(sdxf.Line(points=[(-razmer,-razmer),(razmer,razmer)], layer=lay))
    bl.append(sdxf.Line(points=[(razmer,-razmer),(-razmer,razmer)], layer=lay))
    bl.append(sdxf.Circle(center=(0,0,0),layer=lay,radius=razmer/2))
    obj.blocks.append(bl)
    obj.append(sdxf.Insert(name_block,point=(x,y,0)))
    
#---------------------------------------------------------------------------------------------
def Taheometr(FilePath):
    file_open=open(FilePath, 'r')
    for txt_string in file_open:
        txt_string = txt_string.rstrip('\n')
        dataT = txt_string.split(',')
        if (len(dataT) > 3):
            #Добавляем в чертеж блок с данными координатами
            a = float(dataT[1])
            b = float(dataT[2])
            if (a < b):
                c = b
                b = a
                a = c
            metka(DXFObj,a,b,dataT[0],layerName)
        else:
            #или выводим сообщение об ошибке в строке
            if ((txt_string != '') and (txt_string != '\n')):
                print('WARNING !! Ошибочная строка - ' + txt_string)

#---------------------------------------------------------------------------------------------
def GPS(FilePath):
    file_open=open(FilePath, 'r')
    for txt_string in file_open:
        txt_string = txt_string.rstrip('\n')
        dataT = txt_string.split(',')
        if ((dataT[0] != 'COMPD') and (dataT[0] != 'id')):
            if (len(dataT) > 4):
            #Добавляем в чертеж блок с данными координатами
                a = float(dataT[2])
                b = float(dataT[3])
                if (a < b):
                    c = b
                    b = a
                    a = c
                metka(DXFObj,a,b,dataT[0],layerName)
            else:
                #или выводим сообщение об ошибке в строке
                if ((txt_string != '') and (txt_string != '\n')):
                    print('WARNING !! Ошибочная строка - ' + txt_string)
            
#---------------------------------------------------------------------------------------------
def CreateLine(FilePath):
    number_words=0
    file_open=open(FilePath, 'r')
    points=[]
    for txt_string in file_open:
        txt_string = txt_string.rstrip('\n')
        if ((txt_string == '') or (txt_string[0] == '-') or (txt_string[0] == '\n')):  
            DXFObj.append(sdxf.LwPolyLine(points, flag=1))
            print(' -line create')
            points=[]
        else:
            dataT = txt_string.split(',')
            if (len(dataT) > 3):
                #Добавляем в чертеж блок с данными координатами
                a = float(dataT[1])
                b = float(dataT[2])
                if (a < b):
                    c = b
                    b = a
                    a = c
                metka(DXFObj,a,b,dataT[0],layerName)
                point=(a,b)
                points.append(point);
            else:
                #или выводим сообщение об ошибке в строке
                if ((txt_string != '') and (txt_string != '\n')):
                    print('WARNING !! Ошибочная строка - ' + txt_string)            

#---------------------------------------------------------------------------------------------
def MSK18Mestn(FilePath):
    a=401295.84
    b=2226339.13
    c=32581.14
    d=17064.3
    file_csv=open('konv.csv','w');
    file_csv.write('№;X mest;Y mest;X msk;Y msk\n') 
    number_words=0
    file_open=open(FilePath, 'r')
    for txt_string in file_open:
        txt_string = txt_string.rstrip('\n')
        dataT = txt_string.split(',')
        if (len(dataT) > 3):
            x = float(dataT[1])
            y = float(dataT[2])
            if (y < x):
                z = x
                x = y
                y = z
            #временные значения
            Xmsk=x;
            Ymsk=y;
            tempX=x-a;
            tempY=y-b;
            #расчет координат
            x2=c+math.sqrt(math.pow(tempX,2)+math.pow(tempY,2))*(-1*math.cos(math.atan(tempY/tempX)-math.radians(0.3019612)))-tempX*0.0000011;
            y2=d+math.sqrt(math.pow(tempX,2)+math.pow(tempY,2))*(-1*math.sin(math.atan(tempY/tempX)-math.radians(0.3019612)))-tempY*0.0000011;
            #Добавляем в чертеж блок с данными координатами
            y=round(x2,2)
            x=round(y2,2)
            metka(DXFObj,x,y,dataT[0],layerName)
            file_csv.write(dataT[0] + ';' + str(x) + ';' + str(y) + ';' + str(Xmsk)  + ';' + str(Ymsk)+ '\n')
    file_csv.close()

#---------------------------------------------------------------------------------------------
FilePath="setup.txt"
file_name="setup.txt"
num_block=0 #переменная последовательной нумерации всех блоков
#открываем файл настроек
try:
    setup_open=open(FilePath, 'r')
    #Создаем объект чертежа
    DXFObj=sdxf.Drawing()
    #Добавляем слой для рисования и выбираем цвет элементов на нем
    DXFObj.layers.append(sdxf.Layer(name=layerName,color=layerColor))
    #открываем файл настроек и читаем его строки
    for txt in setup_open:
            print('--------------------')
            dataF = txt.split(',')
            if (len(dataF) > 1):
                tip = dataF[0]
                file_name = dataF[1].rstrip('\n')
                if (tip=="T"):
                    print("Запущена обработка файла тахеометра "+file_name)
                    Taheometr(file_name)
                    print("Файл ("+file_name+")с тахеометра обработан!")
                elif (tip=="G"):
                    print("Запущена обработка файла GPS "+file_name)
                    GPS(file_name)
                    print("Файл ("+file_name+")с GPS данными обработан!")
                elif (tip=="P"):
                    print("Запущена обработка файла полилинии "+file_name)
                    CreateLine(file_name)
                    print("Файл ("+file_name+")с данными полилинии обработан!")
                elif (tip=="C"):
                    print("Запущена конвертация координат "+file_name)
                    MSK18Mestn(file_name)
                    print("Файл ("+file_name+")с данными обработан!")
                                
    DXFObj.saveas('Output.dxf')
    print('--------------------')
    print("Файл чертежа (Output.dxf) создан и сохранен....")
except FileNotFoundError as testErr:
    print(testErr)
    print ('Не найден файл:', file_name)
except UnboundLocalError:
    print('Неверное значение в файле:', file_name)
except PermissionError:
    print('Нет доступа к файлу: Output.dxf')
    print('Чертеж не записан...')
i=input("Конвертация окончена...")
