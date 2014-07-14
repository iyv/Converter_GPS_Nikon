#!/usr/bin/env python3
import sdxf

def metka(obj, x, y, txt, lay):
    #add drawing elements
    global num_block
    HT=0.5
    razmer=1
    num_block+=1
    name_block="block_"+str(txt)+"_"+str(num_block)
    bl = sdxf.Block(name_block)
    bl.append(sdxf.Text(txt,point=(razmer,0),layer=lay,height=HT))
    bl.append(sdxf.Line(points=[(-razmer,-razmer),(razmer,razmer)], layer=lay))
    bl.append(sdxf.Line(points=[(razmer,-razmer),(-razmer,razmer)], layer=lay))
    bl.append(sdxf.Circle(center=(0,0,0),layer=lay,radius=razmer/2))
    obj.blocks.append(bl)
    obj.append(sdxf.Insert(name_block,point=(x,y,0)))

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
        metka(d,x,y,name_point,"METKI")


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
            #увеличиваем колличество слов на 1
            number_words+=1
            if (number_words==1):
                name_point=stroka_data
                print(name_point[0:5])
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
            metka(d,x,y,name_point,"METKI")

FilePath="setup.txt"
setup_open=open(FilePath, 'r')
num_block=0
#set the color of the layer
d=sdxf.Drawing()
d.layers.append(sdxf.Layer(name="METKI",color=5))

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
                print("Запущена обработка файла "+file_name)
                Taheometr(file_name)
                print("Файл ("+file_name+")с тахеометра обработан!")
            elif (tip=="G"):
                print("Запущена обработка файла "+file_name)
                GPS(file_name)
                print("Файл ("+file_name+")с GPS данными обработан!")
                
d.saveas('Output.dxf')
print('--------------------')
print ("Файл чертежа (Output.dxf) создан и сохранен....")
