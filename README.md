Converter_GPS_Nikon
===================

Конвертер гео-данных v1.00.01
2014-11-11

Конвертер предназначен для преобразования координат в файл DXF

формат файла настройки (setup.txt):
А,ББББББББББ.БББ
А,ББББББББББ.БББ

, где:
А - тип файла для преобразования
БББББББББ.БББ - имя файла с данными

Типы файлов для преобразования:
T - данные с тахеометра выводятся в файл DXF (Nikon Novo 5M)
Выходной файл: output.dxf

G - данные с GPS выводятся в файл DXF (AshTech ProMark 100/200)
Выходной файл: output.dxf

P - данные в формате тахеометра выводятся в полилинию в DXF файл
Выходной файл: output.dxf

C - данные в формате тахеометра преобразуются в местную систему координат и выводятся в DXF файл.
Выходной файлы: output.dxf, konv.csv

Преобразования T и G возможны совместно и в неграниченном колличестве. На выходе получится объединенный файл output.dxf
