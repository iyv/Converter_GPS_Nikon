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
    number_words=0
    file_open=open(FilePath, 'r')
    for txt_string in file_open:
        #print('---------tah-----------')
        num_simbol=0
        dlina_stroki=len(txt_string)-1
        while(num_simbol < dlina_stroki):
            stroka_data=""
            while((txt_string[num_simbol]!=',')and(num_simbol<dlina_stroki)):
                stroka_data+=txt_string[num_simbol]
                num_simbol+=1
            #перескакиваем через запятую
            num_simbol+=1
            #увеличиваем колличество слов на 1
            number_words+=1
            if (number_words==1):
                name_point=stroka_data
                #print(stroka_data)
            elif (number_words==2):
                x=float(stroka_data)
                #print(stroka_data)
            elif (number_words==3):
                y=float(stroka_data)
                #print(stroka_data)
        #print('======================')
        #Обнуляем количество слов в строке
        number_words=0
        #Добавляем в чертеж блок с данными координатами
        metka(DXFObj,x,y,name_point,layerName)

#---------------------------------------------------------------------------------------------
def GPS(FilePath):
    number_words=0
    file_open=open(FilePath, 'r')
    for txt_string in file_open:
        #print('---------tah-----------')
        true_data=True
        num_simbol=0
        dlina_stroki=len(txt_string)-1
        while(num_simbol < dlina_stroki):
            stroka_data=""
            while((txt_string[num_simbol]!=',')and(num_simbol<dlina_stroki)):
                stroka_data+=txt_string[num_simbol]
                num_simbol+=1
            #перескакиваем через запятую
            num_simbol+=1
            #увеличиваем количество слов на 1
            number_words+=1
            if (number_words==1):
                name_point=stroka_data
                #print(name_point[0:5])
                if ((name_point[0:5]=='COMPD')or(name_point[0:2]=='Id')):
                    true_data=False
                #print(stroka_data)
            elif ((number_words==3) and true_data):
                x=float(stroka_data)
                #print(stroka_data)
            elif ((number_words==4) and true_data):
                y=float(stroka_data)
                #print(stroka_data)
        #print('======================')
        #Обнуляем количество слов в строке
        number_words=0
        #Добавляем в чертеж блок с данными координатами
        if (true_data):
            metka(DXFObj,x,y,name_point,layerName)
            
#---------------------------------------------------------------------------------------------
def CreateLine(FilePath):
    number_words=0
    file_open=open(FilePath, 'r')
    points=[]
    for txt_string in file_open:
        #print('---------polyline----------')
        num_simbol=0
        dlina_stroki=len(txt_string)-1
        if (dlina_stroki >3):
            while(num_simbol < dlina_stroki):
                stroka_data=""
                while((txt_string[num_simbol]!=',')and(num_simbol<dlina_stroki)):
                    stroka_data+=txt_string[num_simbol]
                    num_simbol+=1
                #перескакиваем через запятую
                num_simbol+=1
                #увеличиваем колличество слов на 1
                number_words+=1
                if (number_words==1):
                    name_point=stroka_data
                    #print(stroka_data)
                elif (number_words==2):
                    x=float(stroka_data)
                    #print(stroka_data)
                elif (number_words==3):
                    y=float(stroka_data)
                    #print(stroka_data)
            #print('======================')
            point=(y,x)
            points.append(point);
            
        else:
            DXFObj.append(sdxf.LwPolyLine(points, flag=1))
            points=[]
        #Обнуляем количество слов в строке
        number_words=0

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
        #print('-----Convert MSK18------')
        num_simbol=0
        dlina_stroki=len(txt_string)-1
        while(num_simbol < dlina_stroki):
            stroka_data=""
            while((txt_string[num_simbol]!=',')and(num_simbol<dlina_stroki)):
                stroka_data+=txt_string[num_simbol]
                num_simbol+=1
            #перескакиваем через запятую
            num_simbol+=1
            #увеличиваем колличество слов на 1
            number_words+=1
            if (number_words==1):
                name_point=stroka_data
                #print(stroka_data)
            elif (number_words==2):
                y=float(stroka_data)
                #print(stroka_data)
            elif (number_words==3):
                x=float(stroka_data)
                #print(stroka_data)
        #print('======================')
        #Обнуляем количество слов в строке
        number_words=0
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
        metka(DXFObj,x,y,name_point,layerName)
        file_csv.write(name_point + ';' + str(x) + ';' + str(y) + ';' + str(Xmsk)  + ';' + str(Ymsk)+ '\n')
    file_csv.close()

#---------------------------------------------------------------------------------------------
FilePath="setup.txt"
setup_open=open(FilePath, 'r')
num_block=0
try:
    #set the color of the layer
    DXFObj=sdxf.Drawing()
    DXFObj.layers.append(sdxf.Layer(name=layerName,color=layerColor))

    for txt in setup_open:
            print('--------------------')
            num_simbol=0
            dlina_stroki=len(txt)-1
            while(num_simbol < dlina_stroki):
                stroka_data=""
                while((txt[num_simbol]!=',')and(num_simbol<dlina_stroki)):
                    stroka_data+=txt[num_simbol]
                    num_simbol+=1
                num_simbol+=1
                tip=stroka_data
                stroka_data=""
                while((txt[num_simbol]!=',')and(num_simbol<dlina_stroki)):
                    stroka_data+=txt[num_simbol]
                    num_simbol+=1
                num_simbol+=1
                file_name=stroka_data
                
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
except FileNotFoundError:
    print ('Не найден файл:', file_name)
except UnboundLocalError:
    print('Неверное значение в файле:', file_name)
except PermissionError:
    print('Нет доступа к файлу: Output.dxf')
    print('Чертеж не записан...')
i=input("Конвертация окончена...")
