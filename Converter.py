import tkinter
from tkinter.ttk import *
from tkinter.filedialog import *

class FilePath:
    def __init__(self, frameFN, numF = 0):
        self.numF = numF
        textLF = "Файл " + str(numF)
        self.labelFrFile = LabelFrame(frameFN, text = textLF)
        self.labelFrFile.columnconfigure(0, weight=1)
        self.labelFrFile.grid(column = 0, row = numF, padx = 5, pady = 1, sticky = 'wen')
        self.entryPath = tkinter.Entry(self.labelFrFile, width=50)
        self.entryPath.grid(column = 0, row = 0, padx = 5, pady = 1, sticky = 'we')
        self.butPath = tkinter.Button(self.labelFrFile, text='...')
        self.butPath.bind('<Button-1>', self.queryFileName)
        self.butPath.grid(column = 1, row = 0, pady = 1, sticky = 'w')
        self.combobox = Combobox(self.labelFrFile,values = ["Тахеометр","GPS"],width=10)
        self.combobox.set("GPS")
        self.combobox.grid(column = 2, row = 0, padx = 5, pady = 1, sticky = 'w')
        
    def queryFileName(self,event):
        pathF = askopenfilename()
        self.entryPath.delete(0,END)
        self.entryPath.insert(0, pathF)

    def getParam(self):
        return(self.numF, self.entryPath.get(), self.combobox.get())

    def printParam(self):
        print('id-', self.numF, '\tpath-', self.entryPath.get(), '\ttip-', self.combobox.get())

class FullForm:
    def __init__(self, frameForm):
        self.FrameTip = LabelFrame(frameForm, text = " Вид операции: ")
        self.FrameTip.grid(column = 0, row = 0, padx = 5, pady = 5, sticky = 'we')

        self.varType = tkinter.IntVar()
        self.rBut1 = Radiobutton(self.FrameTip, text = "Конвертация координат в DXF", variable = self.varType, value = 1)
        self.rBut2 = Radiobutton(self.FrameTip, text = "Создание полилинии по координатам", variable = self.varType, value = 2)
        self.rBut3 = Radiobutton(self.FrameTip, text = "Конвертация из МСК в местную систему (Ижевск)", variable = self.varType, value = 3)
        self.rBut1.grid(column = 0, row = 0, padx = 5, pady = 5, sticky = 'w')
        self.rBut2.grid(column = 0, row = 1, padx = 5, pady = 5, sticky = 'w')
        self.rBut3.grid(column = 0, row = 2, padx = 5, pady = 5, sticky = 'w')
        self.varType.set(1)

        self.FramePath = LabelFrame(frameForm, text = " Файлы: ", labelanchor = 'n', height = 230)
        self.FramePath.columnconfigure(0, weight=1)
        self.FramePath.rowconfigure(1, weight=1)
        self.FramePath.grid(column = 0, row = 1, padx = 5, pady = 2, sticky = 'wens')

        self.fileName = []
        self.fileName.append(FilePath(self.FramePath, 1))

        self.FrameBut = LabelFrame(frameForm, text = "")
        self.FrameBut.columnconfigure(0, weight=1)
        self.FrameBut.grid(column = 0, row = 2, padx = 5, pady = 5, sticky = 'wes')

        self.buttonAdd = Button(self.FrameBut, text = 'Добавить файл')
        self.buttonAdd.bind('<Button-1>', self.addFile)
        self.buttonAdd.grid(column = 0, row = 0, padx = 3, pady = 5, sticky = 'w')

        self.buttonReset = Button(self.FrameBut, text = 'Сбросить')
        self.buttonReset.bind('<Button-1>', self.reset)
        self.buttonReset.grid(column = 1, row = 0, padx = 8, pady = 5, sticky = 'we')

        self.buttonConv = Button(self.FrameBut, text = 'Конвертировать')
        self.buttonConv.bind('<Button-1>', self.convert)
        self.buttonConv.grid(column = 2, row = 0, padx = 3, pady = 5, sticky = 'e')
        self.frameForm = frameForm

    def addFile(self, event):
        num = len(self.fileName) + 1
        self.fileName.append(FilePath(self.FramePath, num))

    def convert(self, event):
        print('Вид - ', self.varType.get())
        for elem in self.fileName:
            elem.printParam()
            
    def reset(self, event):
        self.__init__(self.frameForm)
    
tk = tkinter.Tk()
tk.title("Конвертер координат в DXF")
tk.resizable(width = False, height = True)
tk.geometry("640x480")

#tk.rowconfigure(0, weight=1)
tk.columnconfigure(0, weight=1)

#frame = tkinter.Frame(tk, bg = 'green')
#frame.grid(column = 0, row = 0,sticky = 'nwes')

FullForm(tk)

tk.mainloop()
