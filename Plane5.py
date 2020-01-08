import tkinter as tk
from random import randint,choice
from time import sleep
import math
import serial
import threading
from multiprocessing import Process, Value, Array


BACKGROUND_COLOR = "#000000"
FOREGROUND_COLOR = "#B0B0B0"
MASTER = tk.Tk()
TRUEWIDTH = MASTER.winfo_screenwidth()
print(TRUEWIDTH)
TRUEHEIGHT = MASTER.winfo_screenheight()
print(TRUEHEIGHT)

#TRUEHEIGHT=900
#TRUEWIDTH=1600
if TRUEWIDTH*9/16<TRUEHEIGHT:
    HEIGHT=TRUEWIDTH*9/16
    WIDTH = TRUEWIDTH
else:
    WIDTH=16/9*TRUEHEIGHT
    HEIGHT = TRUEHEIGHT
class Program():
    def __init__(self):
        self.stats = StatsDisplay(WIDTH/5,WIDTH/5*4)
        self.buttons = ButtonDisplay(0,434,WIDTH/5,HEIGHT-434)
        self.top = tk.Toplevel()
        self.top.destroy()
        
        #self.ser = serial.Serial('com3',9600)
    
    def mainloop(self, ardData):
        while True:
            w.delete("all")
            self.stats.draw(ardData)
            w.create_line(WIDTH/5,449,WIDTH/5,HEIGHT-15,fill=FOREGROUND_COLOR)
            w.create_line(WIDTH/5,15,WIDTH/5,419,fill=FOREGROUND_COLOR)
            w.create_line(15,434,WIDTH/5-15,434,fill=FOREGROUND_COLOR)
            w.after(5)
            w.update()

class ButtonDisplay(object):

    def __init__(self,x,y,width,height):
        self.light = False
        self.lightLevel = tk.IntVar(value=100)
        self.bombAmount = tk.IntVar(value=2)

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        w.bind_all("<Escape>",close)
        self.objects = []
        self.createPlaceObjects()
        
    def createPlaceObjects(self):
        light = tk.Button(MASTER,activebackground="#202020",activeforeground="#404040",bg="#404040",fg=FOREGROUND_COLOR,text="Turn Light On",font="Tahoma 15",relief=tk.FLAT,command=self.toggleLight)
        level = tk.Scale(bd=0,from_=0,to=100,troughcolor="#404040",activebackground="#202020",bg=BACKGROUND_COLOR,fg=FOREGROUND_COLOR,font="Tahoma 12 bold",orient=tk.HORIZONTAL,label="Light Level",length=90,highlightthickness=0,sliderrelief=tk.FLAT,variable=self.lightLevel,command=self.changeLightLevel)
        level.set(self.lightLevel.get())
        bomb = tk.Button(MASTER,activebackground="#470505",activeforeground="#404040",bg="#900909",fg=FOREGROUND_COLOR,text="Drop Bombs",font="Tahoma 16 bold",relief=tk.FLAT,command=self.dropBomb)
        amount = tk.Scale(bd=0,from_=0,to=12,troughcolor="#404040",activebackground="#202020",bg=BACKGROUND_COLOR,fg=FOREGROUND_COLOR,font="Tahoma 12 bold",orient=tk.VERTICAL,length=90,highlightthickness=0,sliderrelief=tk.FLAT,variable=self.bombAmount,command=self.nextBombAmount)
        amount.set(self.bombAmount.get())
        self.objects = [light,level,bomb,amount]
        self.placeObjects()

    def toggleLight(self):
        if self.light == False:
            self.light = True
            self.objects[0].config(text = "Turn Light Off")
        else:
            self.light = False
            self.objects[0].config(text = "Turn Light On")
        self.placeObjects()

    def changeLightLevel(self,event=None):
        program.stats.plane.lightColor = colorMultiply("#FFFF00",self.lightLevel.get()/100)

    def nextBombAmount(self,value):
        newvalue = min(list(range(0,13,2)), key=lambda x:abs(x-float(value)))
        self.objects[3].set(newvalue)

    def dropBomb(self):
        program.stats.plane.dropBombs(self.bombAmount.get())

    def placeObjects(self):
        for i in self.objects:
            i.place_forget()
        self.objects[0].place(x=self.x+self.width*0.1,y=self.y+self.height*0.2-20,width=self.width*0.8,height=HEIGHT*0.05)
        if self.light == True:
            self.objects[1].place(x=self.x+self.width*0.1,y=self.y+self.height*0.25,width=self.width*0.8,height=100)
        self.objects[2].place(x=self.x+self.width*0.1,y=self.y+self.height*0.75-self.width*0.3,width=self.width*0.6,height=self.width*0.6)
        self.objects[3].place(x=self.x+self.width*0.8,y=self.y+self.height*0.75-self.width*0.3,width=60,height=self.width*0.6)

class StatsDisplay(object):
    def __init__(self,x,width):
        
        self.x = x
        self.width = width
        self.plane = Plane(self.x+15,15,self.width-449,404)
        #self.anglePlane = AnglePlane(15,15,WIDTH/5-115,404)
        self.sidePlane=sidePlane(WIDTH-419, 450, 404, HEIGHT-450)
        self.map = Map(WIDTH-419,15,404)
        self.speedDisplay = SpeedDisplay(WIDTH/5+15,449,WIDTH/10,HEIGHT-464)
        self.compass = Compass(WIDTH*0.3+30,HEIGHT*0.9,WIDTH*0.55-494,HEIGHT*0.1-15,0)
        self.heightDisplay = HeightDisplay(WIDTH*0.85-449,449,WIDTH*0.15,HEIGHT-464)
        self.horizon = ArtificialHorizon(WIDTH*0.3+30,449,WIDTH*0.55-494,HEIGHT*0.9-464)

    def draw(self, ardData):
        self.horizon.draw()
        self.map.draw()
        self.plane.draw()
        #self.anglePlane.draw()
        self.sidePlane.draw(ardData[0])
        self.speedDisplay.draw()
        self.compass.draw()
        #print(ardData[0])
        self.heightDisplay.draw(ardData[0])

class Map(object):
    def __init__(self,x,y,size):
        self.x = x
        self.y = y
        self.size = size
        self.world = []
        for i in range(50):
            self.world.append([])
            for j in range(50):
                if randint(0,75) == 42:
                    self.world[-1].append(2)
                else:
                    self.world[-1].append(0)
        self.world[24][24] = 1

    def update(self,newworld):
        self.world = newworld   #Also Amerika Hahahaha
        self.world[24][24] = 1

    def draw(self):
        w.create_rectangle(self.x,self.y,self.x+self.size,self.y+self.size,outline=FOREGROUND_COLOR,width=2,fill="green")
        x = self.x+2
        y = self.y+2
        for i in self.world:
            for j in i:
                if j == 1:
                    w.create_polygon((x-6,y+9),(x,y+2),(x+6,y+9),(x,y-9),fill="black")
                elif j == 2:
                    w.create_oval(x-3,y-3,x+3,y+3,fill="blue")
                #else:
                #    w.create_oval(x,y,x,y,fill="blue")
                y += 8
            x += 8
            y = self.y+2

class Plane(object):
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.showPositionLights = 10
        self.positionLightCooldown = 50
        self.lightColor = "#FFFF00"
        self.bombs = []
        self.bombAmount = 0
        self.batteryLife1 = 5
        self.batteryLife2 = 100
        for i in range(6):
            self.bombs.append(Bomb(self.x+self.width*0.42,self.y+self.height*0.36-6+i*(1+self.height*0.04),self.width*0.07,self.height*0.03,self))
        for i in range(6):
            self.bombs.append(Bomb(self.x+self.width*0.51,self.y+self.height*0.36-6+i*(1+self.height*0.04),self.width*0.07,self.height*0.03,self))
        self.bombBarrier = 1

    def draw(self):
        w.create_polygon((self.x+10,self.y+self.height-10),(self.x+20,self.y+self.height*0.85),(self.x+self.width/2,self.y+10),(self.x+self.width-20,self.y+self.height*0.85),(self.x+self.width-10,self.y+self.height-10),(self.x+self.width*0.63,self.y+self.height*0.75),(self.x+self.width*0.37,self.y+self.height*0.75),width=2,fill=BACKGROUND_COLOR,outline=FOREGROUND_COLOR)
        w.create_rectangle(self.x+self.width*0.37,self.y+self.height*0.75,self.x+self.width*0.41,self.y+self.height*0.17,width=2,outline=FOREGROUND_COLOR,fill=BACKGROUND_COLOR)
        w.create_rectangle(self.x+self.width*0.63,self.y+self.height*0.75,self.x+self.width*0.59,self.y+self.height*0.17,width=2,outline=FOREGROUND_COLOR,fill=BACKGROUND_COLOR)
        #Battery
        self.batteryLife1 -= 0.1
        if self.batteryLife1 <= 0:
            self.batteryLife1 = 100
        self.batteryLife2 -= 0.3
        if self.batteryLife2 <= 0:
            self.batteryLife2 = 100
        w.create_rectangle(self.x+self.width*0.415,self.y+self.height*0.2,self.x+self.width*0.49,self.y+self.height*0.27,fill=BACKGROUND_COLOR,outline=FOREGROUND_COLOR)
        w.create_rectangle(self.x+self.width*0.49,self.y+self.height*0.22,self.x+self.width*0.495,self.y+self.height*0.25,fill=FOREGROUND_COLOR,width=0)
        w.create_rectangle(self.x+self.width*0.505,self.y+self.height*0.2,self.x+self.width*0.58,self.y+self.height*0.27,fill=BACKGROUND_COLOR,outline=FOREGROUND_COLOR)
        w.create_rectangle(self.x+self.width*0.58,self.y+self.height*0.22,self.x+self.width*0.585,self.y+self.height*0.25,fill=FOREGROUND_COLOR,width=0)
        colors = ["darkred","red","orange","yellow","yellow","darkgreen","darkgreen","green","green","green"]
        w.create_rectangle(self.x+self.width*0.415,self.y+self.height*0.2,self.x+self.width*0.415+(self.width*0.075)*(self.batteryLife1/100),self.y+self.height*0.27,fill=colors[int(math.ceil(self.batteryLife1/10))-1],outline=FOREGROUND_COLOR)
        w.create_text(self.x+self.width*0.45,self.y+self.height*0.23,text=str(round(self.batteryLife1))+"%",fill=FOREGROUND_COLOR,font="Tahoma 12")
        w.create_rectangle(self.x+self.width*0.505,self.y+self.height*0.2,self.x+self.width*0.505+(self.width*0.075)*(self.batteryLife2/100),self.y+self.height*0.27,fill=colors[int(math.ceil(self.batteryLife2/10))-1],outline=FOREGROUND_COLOR)
        w.create_text(self.x+self.width*0.54,self.y+self.height*0.23,text=str(round(self.batteryLife2))+"%",fill=FOREGROUND_COLOR,font="Tahoma 12")
        #Lights
        if program.buttons.light == True:
            if self.positionLightCooldown > 0:
                self.positionLightCooldown -= 1
                if self.positionLightCooldown == 0:
                    self.showPositionLights = 10
            w.create_polygon((self.x+self.width*0.3,self.y+self.height*0.35),(self.x+self.width*0.22,0),(self.x+self.width*0.38,0),fill=self.lightColor)
            w.create_polygon((self.x+self.width*0.7,self.y+self.height*0.35),(self.x+self.width*0.62,0),(self.x+self.width*0.78,0),fill=self.lightColor)
            if self.showPositionLights > 0:
                w.create_oval(self.x+15,self.y+self.height-15,self.x+5,self.y+self.height-5,fill="red",width=0)
                w.create_oval(self.x+self.width-15,self.y+self.height-15,self.x+self.width-5,self.y+self.height-5,fill="green",width=0)
                self.showPositionLights -= 1
                if self.showPositionLights == 0:
                    self.positionLightCooldown = 50
        #Bombs
        w.create_rectangle(self.x+self.width*0.42-1,self.y+self.height*0.6-1,self.x+self.width*0.58+1,self.y+self.height*0.63+1,fill=BACKGROUND_COLOR,outline=FOREGROUND_COLOR)
        if self.bombAmount > 0 and self.bombs != [] and self.bombBarrier > 0:
            self.bombBarrier -= 0.05
        elif (self.bombAmount == 0 or self.bombs == []) and self.bombBarrier < 1:
            self.bombBarrier += 0.05
        w.create_line(self.x+self.width*0.41,self.y+self.height*0.6-1,self.x+self.width/2-(1-self.bombBarrier)*self.width*0.09,self.y+self.height*0.6-1,width=2,fill=FOREGROUND_COLOR)
        w.create_line(self.x+self.width/2+(1-self.bombBarrier)*self.width*0.09,self.y+self.height*0.6-1,self.x+self.width*0.59,self.y+self.height*0.6-1,width=2,fill=FOREGROUND_COLOR)
        for i in range(len(self.bombs)-1,-1,-1):
            self.bombs[i].draw()

    def dropBombs(self,amount):
        if amount == 0:
            return False
        self.bombAmount = amount
        for i in self.bombs:
            i.move = 0.5

class Bomb(object):
    def __init__(self,x,y,width,height,plane):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.plane = plane
        self.color = "#"
        for i in range(6):
            self.color += choice("0123456789ABCDEF")
        self.size = 1
        self.floor = True
        self.move = 0

    def draw(self):
        if self.floor == True and self.plane.bombBarrier <= 0:
            self.y += self.move
        elif self.floor == False:
            self.size -= 0.03
            if self.size <= 0:
                self.plane.bombs.remove(self)
        w.create_rectangle((0.5-self.size/2)*self.width+self.x,(0.5-self.size/2)*self.height+self.y,self.x+(0.5+self.size/2)*self.width,self.y+(0.5+self.size/2)*self.height,fill=self.color)
        if self.y > self.plane.y+self.plane.height*0.6 and self.floor == True:
            self.floor = False
            self.plane.bombAmount -= 1
            if self.plane.bombAmount == 0:
                for i in self.plane.bombs:
                    i.move = 0

class SpeedDisplay(object):
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.speed = 0
        self.direction = 1
        self.updateNumbers()

    def setSpeed(self,speed):
        self.speed = speed
        self.updateNumbers()

    def updateNumbers(self):
        self.numbers = []
        number1 = int(self.speed/10)*10
        number = number1
        while self.y+self.height/2+(self.speed-number)*5 < self.y+self.height:
            self.numbers.append(number)
            number -= 10
        number = number1 + 10
        while self.y+self.height/2-(number-self.speed)*5 > self.y:
            self.numbers.append(number)
            number += 10

    def draw(self):
        self.setSpeed(self.speed+0.5*self.direction)
        if not 300 > self.speed > 0:
            self.direction *= -1
        w.create_rectangle(self.x,self.y,self.x+self.width,self.y+self.height,fill="#404040",outline=FOREGROUND_COLOR)
        for i in self.numbers:
            y = self.y+self.height/2+(self.speed-i)*5
            if i%100 == 0:
                w.create_line(self.x+self.width*0.8,y,self.x+self.width,y,fill=FOREGROUND_COLOR)
            else:
                w.create_line(self.x+self.width*0.85,y,self.x+self.width,y,fill=FOREGROUND_COLOR)
            if i%20 == 0:
                w.create_text(self.x+self.width*0.65,y,text=str(i),fill=FOREGROUND_COLOR,font="Tahoma 14")
        w.create_polygon((self.x+self.width,self.y+self.height/2-10),(self.x+self.width,self.y+self.height/2+10),(self.x+self.width*0.9,self.y+self.height/2),fill=FOREGROUND_COLOR)

class Compass(object):
    def __init__(self,x,y,width,height,angle):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.angle = angle
        self.updateNumbers()

    def setAngle(self,angle):
        self.angle = angle%360
        self.updateNumbers()

    def updateNumbers(self):
        self.numbers = []
        number1 = int(self.angle/5)*5
        number = number1
        while self.x+self.width/2-(self.angle-number)*5 > self.x:
            self.numbers.append(number)
            number -= 5
        number = number1 + 5
        while self.x+self.width/2-(self.angle-number)*5 < self.x+self.width:
            self.numbers.append(number)
            number += 5

    def draw(self):
        self.setAngle(self.angle+0.5)
        w.create_rectangle(self.x,self.y,self.x+self.width,self.y+self.height,fill="#404040",outline=FOREGROUND_COLOR)
        for i in self.numbers:
            x = self.x+self.width/2+(i-self.angle)*5
            if i%10 == 0:
                w.create_line(x,self.y,x,self.y+self.height*0.3,fill=FOREGROUND_COLOR)
            else:
                w.create_line(x,self.y,x,self.y+self.height*0.2,fill=FOREGROUND_COLOR)
            if i%30 == 0:
                if i%90 == 0:
                    w.create_text(x,self.y+self.height*0.4,text=["N","E","S","W"][(i%360)//90],fill=FOREGROUND_COLOR,font="Tahoma 14 bold")
                else:
                    w.create_text(x,self.y+self.height*0.4,text=str(i%360),fill=FOREGROUND_COLOR,font="Tahoma 14")
        w.create_polygon((self.x+self.width/2-10,self.y),(self.x+self.width/2+10,self.y),(self.x+self.width/2,self.y+self.height*0.15),fill=FOREGROUND_COLOR)

class HeightDisplay(object):
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.displayHeight = height
        self.border = self.width*2/3

        self.height = 0
        self.setHeight(0)
        #self.direction = 1

    def setHeight(self,height):
        self.height = (height-self.height)*0.05+self.height
        self.updateNumbers()

    def updateNumbers(self):
        self.numbers1 = []
        number1 = int(self.height)
        number = number1
        while self.y+self.displayHeight/2+(self.height-number)*25 < self.y+self.displayHeight:
            self.numbers1.append(number)
            number -= 1
        number = number1 + 1
        while self.y+self.displayHeight/2-(number-self.height)*25 > self.y:
            self.numbers1.append(number)
            number += 1
        self.numbers2 = []
        number1 = int(round(self.height%1*100)/5)*5
        number = number1
        while self.y+self.displayHeight/2+(round(self.height%1*100)-number)*4 < self.y+self.displayHeight*0.7:
            self.numbers2.append(number)
            number -= 5
        number = number1 + 5
        while self.y+self.displayHeight/2-(number-round(self.height%1*100))*4 > self.y+self.displayHeight*0.3:
            self.numbers2.append(number)
            number += 5

    def draw(self, height):
        #self.height+=0.01
        self.height = (height-self.height)*0.05+self.height
        self.updateNumbers()
        w.create_polygon((self.x,self.y),(self.x,self.y+self.displayHeight),(self.x+self.border,self.y+self.displayHeight),
                         (self.x+self.width,self.y+self.displayHeight*0.7),(self.x+self.width,self.y+self.displayHeight*0.3),(self.x+self.border,self.y),fill="#404040",outline=FOREGROUND_COLOR)
        w.create_line(self.x+self.border,self.y,self.x+self.border,self.y+self.displayHeight,fill=FOREGROUND_COLOR)
        w.create_rectangle(self.x+self.border,self.y+self.displayHeight*0.3,self.x+self.width-10,self.y+self.displayHeight*0.7,fill=BACKGROUND_COLOR,outline=FOREGROUND_COLOR)
        for i in self.numbers1:
            y = self.y+self.displayHeight/2+(self.height-i)*25
            if i%20 == 0:
                w.create_line(self.x+self.border*0.83,y,self.x+self.border,y,fill=FOREGROUND_COLOR,width=2)
            elif i%10 == 0:
                w.create_line(self.x+self.border*0.85,y,self.x+self.border,y,fill=FOREGROUND_COLOR)
            elif i%2 == 0:
                w.create_line(self.x+self.border*0.88,y,self.x+self.border,y,fill=FOREGROUND_COLOR)
            else:
                w.create_line(self.x+self.border*0.9,y,self.x+self.border,y,fill=FOREGROUND_COLOR)
            if i%10 == 0:
                w.create_text(self.x+self.border*0.83-15,y,text=str(int(i/10)),fill=FOREGROUND_COLOR,font="Tahoma 14")
        w.create_rectangle(self.x,self.y+self.displayHeight/2-20,self.x+self.border,self.y+self.displayHeight/2+20,fill=BACKGROUND_COLOR,outline=FOREGROUND_COLOR)
        zeroMinus = ["",""]
        if self.height%1 > 0.5:
            if 0 > self.height > -1:
                if self.height >= 0:
                    zeroMinus = ["-",""]
                else:
                    zeroMinus = ["","-"]
            w.create_text(self.x+self.border/2,self.y+self.displayHeight/2-20-(1-self.height%1)*40,
                          text=zeroMinus[0]+str(int(self.height+1)),fill=FOREGROUND_COLOR,font="Tahoma 18")
            w.create_text(self.x+self.border/2,self.y+self.displayHeight/2+20-(1-self.height%1)*40,
                          text=zeroMinus[1]+str(int(self.height)),fill=FOREGROUND_COLOR,font="Tahoma 18")
        elif self.height%1 < 0.5:
            if 0 > self.height > -1:
                if self.height >= 0:
                    zeroMinus = ["-",""]
                else:
                    zeroMinus = ["","-"]
            w.create_text(self.x+self.border/2,self.y+self.displayHeight/2+20+(self.height%1)*40,text=zeroMinus[0]+str(int(self.height-1)),fill=FOREGROUND_COLOR,font="Tahoma 18")
            w.create_text(self.x+self.border/2,self.y+self.displayHeight/2-20+(self.height%1)*40,text=zeroMinus[1]+str(int(self.height)),fill=FOREGROUND_COLOR,font="Tahoma 18")
        else:
            w.create_text(self.x+self.border/2,self.y+self.displayHeight/2,text=str(int(self.height)),fill=FOREGROUND_COLOR,font="Tahoma 18")
        w.create_rectangle(self.x+1,self.y+1,self.x+self.border*0.83-34,self.y+self.displayHeight/2-20,width=0,fill="#404040")
        w.create_rectangle(self.x+1,self.y+self.displayHeight/2+21,self.x+self.border*0.83-34,self.y+self.displayHeight,width=0,fill="#404040")
        for i in self.numbers2:
            y = self.y+self.displayHeight/2+(round(self.height%1*100)-i)*4
            if i%100 == 0:
                w.create_line(self.x+self.border,y,self.x+self.border*1.2,y,fill=FOREGROUND_COLOR,width=2)
            elif i%10 == 0:
                w.create_line(self.x+self.border,y,self.x+self.border*1.15,y,fill=FOREGROUND_COLOR)
            else:
                w.create_line(self.x+self.border,y,self.x+self.border*1.12,y,fill=FOREGROUND_COLOR)
            if i%10 == 0:
                w.create_text(self.x+self.border*1.2+15,y,text=str((i%100)/10),fill=FOREGROUND_COLOR,font="Tahoma 14")
        w.create_polygon((self.x+self.border,self.y+self.displayHeight/2-8),(self.x+self.border,self.y+self.displayHeight/2+8),(self.x+self.border*1.1,self.y+self.displayHeight/2),fill=FOREGROUND_COLOR)
       
class ArtificialHorizon(object):
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.midx = x+width/2
        self.midy = y+height/2
        self.lineLength=width/10
        self.shortLineLength=self.lineLength/10
        self.middleLineLength=self.lineLength/2
        self.yPerDegree = self.height/50
        self.heightAngle = 0
        self.setWidthAngle(10)

        self.direction = 1

    def setHeightAngle(self,angle):
        self.heightAngle = angle

    def setWidthAngle(self,angle):
        angle %= 360
        if angle == 90 or angle == -1:
            angle -= 0.01
        self.widthAngle = angle
        angle = angle/180*math.pi
        self.xTan = math.tan(angle)
        self.xSin=math.sin(angle)
        self.xCos=math.cos(angle)

    def draw(self):
        #if abs(self.widthAngle) > 80:
        #    self.direction *= -1
        self.setWidthAngle(self.widthAngle-self.direction)
        """if 270 > self.widthAngle > 90:
            colors = ["#0000FF","#8B4513"]
        else:
            colors = ["#8B4513","#0000FF"]
        """
        colors = ["#8B4513","#0000FF"]
        #blue background
        w.create_rectangle(self.x,self.y,self.x+self.width,self.y+self.height,fill=colors[1],outline=FOREGROUND_COLOR)
        #w.create_polygon((self.x,self.y+self.height),(self.x,self.midy-self.heightAngle*self.yPerDegree+self.xTan*self.width/2),
                         #(self.x+self.width,self.midy-self.heightAngle*self.yPerDegree-self.xTan*self.width/2),(self.x+self.width,self.y+self.height),fill=colors[0],outline=FOREGROUND_COLOR)
        lineMidx = self.midx+self.xSin*self.yPerDegree*(-self.heightAngle)
        line2Midx = self.midx+self.xSin*self.yPerDegree*(-self.heightAngle+100)
        lineMidy = self.midy+self.xCos*self.yPerDegree*(-self.heightAngle)
        line2Midy = self.midy+self.xCos*self.yPerDegree*(-self.heightAngle+100)
        """w.create_polygon((self.x,self.y+self.height),(self.x,lineMidy+self.xTan*(lineMidx-self.x)),
                         (self.x+self.width,lineMidy-self.xTan*(self.x+self.width-lineMidx)),(self.x+self.width,self.y+self.height),
        fill=colors[0],outline=FOREGROUND_COLOR)"""
        w.create_polygon((lineMidx-self.xCos*500,lineMidy+self.xSin*500),
                          (lineMidx+self.xCos*500,lineMidy-self.xSin*500),
                          (line2Midx+self.xCos*500,line2Midy-self.xSin*500),(line2Midx-self.xCos*500,line2Midy+self.xSin*500),fill=colors[0],outline=FOREGROUND_COLOR)
        for i in range(0,90,1):
            lineMidx = self.midx+self.xSin*self.yPerDegree*(-(self.heightAngle%10)+i)
            lineMidy = self.midy+self.xCos*self.yPerDegree*(-(self.heightAngle%10)+i)
            if i%10==0:
                w.create_line(lineMidx-self.xCos*self.lineLength,lineMidy+self.xSin*self.lineLength,
                          lineMidx+self.xCos*self.lineLength,lineMidy-self.xSin*self.lineLength,fill=FOREGROUND_COLOR)
                if(not(self.y<lineMidy<self.y+self.height) or not(self.x<lineMidx<self.x+self.width)):
                    break
            else:
                if i%10==5:
                    w.create_line(lineMidx-self.xCos*self.middleLineLength,lineMidy+self.xSin*self.middleLineLength,
                          lineMidx+self.xCos*self.middleLineLength,lineMidy-self.xSin*self.middleLineLength,fill=FOREGROUND_COLOR)
                else:
                    w.create_line(lineMidx-self.xCos*self.shortLineLength,lineMidy+self.xSin*self.shortLineLength,
                              lineMidx+self.xCos*self.shortLineLength,lineMidy-self.xSin*self.shortLineLength,fill=FOREGROUND_COLOR)
        for i in range(-1,-90,-1):
            lineMidx = self.midx+self.xSin*self.yPerDegree*(-(self.heightAngle%10)+i)
            lineMidy = self.midy+self.xCos*self.yPerDegree*(-(self.heightAngle%10)+i)
            if i%10==0:
                w.create_line(lineMidx-self.xCos*self.lineLength,lineMidy+self.xSin*self.lineLength,
                          lineMidx+self.xCos*self.lineLength,lineMidy-self.xSin*self.lineLength,fill=FOREGROUND_COLOR)
                if(not(self.y<lineMidy<self.y+self.height) or not(self.x<lineMidx<self.x+self.width)):
                    break
            else:
                if i%10==5:
                    w.create_line(lineMidx-self.xCos*self.middleLineLength,lineMidy+self.xSin*self.middleLineLength,
                          lineMidx+self.xCos*self.middleLineLength,lineMidy-self.xSin*self.middleLineLength,fill=FOREGROUND_COLOR)
                else:
                    w.create_line(lineMidx-self.xCos*self.shortLineLength,lineMidy+self.xSin*self.shortLineLength,
                          lineMidx+self.xCos*self.shortLineLength,lineMidy-self.xSin*self.shortLineLength,fill=FOREGROUND_COLOR)
        w.create_line((self.x+self.width*0.8,self.y+self.height*0.55),(self.x+self.width*0.8,self.midy),(self.x+self.width*0.9,self.midy),width=2,fill=BACKGROUND_COLOR)
        w.create_line((self.x+self.width*0.2,self.y+self.height*0.55),(self.x+self.width*0.2,self.midy),(self.x+self.width*0.1,self.midy),width=2,fill=BACKGROUND_COLOR)
        w.create_rectangle(self.midx-4,self.midy-4,self.midx+4,self.midy+4,width=2,outline=BACKGROUND_COLOR)
        w.create_rectangle(self.x,0,self.x+self.width,self.y-1,fill=BACKGROUND_COLOR)
        w.create_rectangle(self.x,self.y+self.height+1,self.x+self.width,TRUEHEIGHT,fill=BACKGROUND_COLOR)
        w.create_rectangle(0,0,self.x-1,TRUEHEIGHT,fill=BACKGROUND_COLOR)
        w.create_rectangle(self.x+self.width+1,0,TRUEWIDTH,TRUEHEIGHT,fill=BACKGROUND_COLOR)
        w.create_line(self.x,self.y,self.x+self.width,self.y,fill=FOREGROUND_COLOR)

class Data(object):
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    #def draw(self):
        
        

class AnglePlane(object):
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.direction = 1
        self.setAngle(0)

    def setAngle(self,angle):
        self.angle = angle
        angle = angle/180*math.pi
        self.angleAdd1 = (math.cos(angle)*self.width*0.35,math.sin(angle)*self.width*0.35)
        self.angleAdd2 = (math.cos(angle)*self.width*-0.1,math.sin(angle)*self.width*-0.1)
        self.angleAdd3 = (math.cos(angle)*self.width*0.23,math.sin(angle)*self.width*0.23)
        self.angleAdd4 = (math.cos(angle)*self.width*-0.35,math.sin(angle)*self.width*-0.35)
        try:
            program.stats.horizon.setHeightAngle(self.angle)
        except:
            pass

    def draw(self):
        middle = self.x+self.width/2
        self.setAngle(self.angle+0.1*self.direction)
        if not 30 > self.angle > -30:
            self.direction *= -1
        w.create_text(self.x,self.y,text="Angle: "+str(round(self.angle))+"°",anchor=tk.W,fill=FOREGROUND_COLOR,font="Tahoma 12")
        w.create_polygon((middle+self.angleAdd4[0],self.y+self.height*0.1-self.angleAdd4[1]),(middle+self.angleAdd1[0],self.y+self.height*0.35-self.angleAdd1[1]),(middle+self.angleAdd4[0],self.y+self.height*0.6-self.angleAdd4[1]),
                         (middle+self.angleAdd2[0],self.y+self.height*0.4-self.angleAdd2[1]),(middle+self.angleAdd2[0],self.y+self.height*0.3-self.angleAdd2[1]),width=2,fill=BACKGROUND_COLOR,outline=FOREGROUND_COLOR)
        w.create_polygon((middle+self.angleAdd2[0],self.y+self.height*0.4-self.angleAdd2[1]),(middle+self.angleAdd3[0],self.y+self.height*0.4-self.angleAdd3[1]),
                         (middle+self.angleAdd3[0],self.y+self.height*0.38-self.angleAdd3[1]),(middle+self.angleAdd2[0],self.y+self.height*0.38-self.angleAdd2[1]),width=2,fill=BACKGROUND_COLOR,outline=FOREGROUND_COLOR)
        w.create_polygon((middle+self.angleAdd2[0],self.y+self.height*0.3-self.angleAdd2[1]),(middle+self.angleAdd3[0],self.y+self.height*0.3-self.angleAdd3[1]),
                         (middle+self.angleAdd3[0],self.y+self.height*0.32-self.angleAdd3[1]),(middle+self.angleAdd2[0],self.y+self.height*0.32-self.angleAdd2[1]),width=2,fill=BACKGROUND_COLOR,outline=FOREGROUND_COLOR)

"""class updateData(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        print("started updating data")
        
    def  run(self):
        self.updateData()
    def updateData(self):
        while True:
            try:
                #print("HI")
                data=int.from_bytes(self.ser.read(), byteorder='little')
                #data = data.split("'")[1]
                if data:
                    #data=str(data)
                    print(data)
                    threadLock.acquire()
                    print("bla")
                    program.stats.heightDisplay.setHeight(int(data))
                    threadLock.release()
                    if self.ser.inWaiting()>100:
                        self.ser.flushInput()
            except:
                print("Stecker draußen")
                
                try:
                    self.ser = serial.Serial('com3',9600)
                except:
                    pass"""
class sidePlane(object):
    def __init__(self,x,y,width, height):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.z=self.height/38
        self.cgx=self.x+1/2*self.width
        self.cgy=self.y+6*self.z
        self.HoG=0
        self.pitch=0
        self.AoT=0
        self.dists=[2*self.z, 1.2*self.z, 1/2*self.z, 4*self.z, 5.2*self.z, 5.5*self.z, 5*self.z, 1/2*self.z, 1.2*self.z, 2*self.z, 3*self.z]
        self.angles=[0, 20, 90,178, 170, 171, 182, 270, 340, 0, 0]
        for i in range(len(self.angles)):
            self.angles[i]*=math.pi/180

    def draw(self, HoG):
        self.pitch+=0.03
        self.AoT+=0.01
        self.AoT%=1/2
        #self.HoG+=(HoG-self.HoG)/10
        self.HoG+=(HoG-self.HoG)/5
        #self.HoG+=1
        self.HoG%=300
        for i in range(len(self.dists)-2):
            w.create_line(self.cgx+math.cos(self.angles[i]+self.pitch)*self.dists[i],self.cgy-math.sin(self.angles[i]+self.pitch)*self.dists[i],
                          self.cgx+math.cos(self.angles[i+1]+self.pitch)*self.dists[i+1],self.cgy-math.sin(self.angles[i+1]+self.pitch)*self.dists[i+1],fill=FOREGROUND_COLOR)
        w.create_line(self.cgx+math.cos(self.angles[10]+self.pitch)*self.dists[10],self.cgy-math.sin(self.angles[10]+self.pitch)*self.dists[10],
                          self.cgx+math.cos(self.angles[10]+self.pitch)*self.dists[10]+math.cos(self.pitch-self.AoT)*self.z*2,
                          self.cgy-math.sin(self.angles[10]+self.pitch)*self.dists[10]-math.sin(self.pitch-self.AoT)*self.z*2,
                          fill=FOREGROUND_COLOR)
    
        w.create_line(self.x, self.z*1/2+self.cgy+self.HoG*self.z/10, self.x+self.width, self.z*1/2+self.cgy+self.HoG*self.z/10,fill=FOREGROUND_COLOR)
        



    
class ArduinoData(object):
    #height=0
    def __init__(self):
        self.height=0
        self.bank=0
        self.pitch=0
        self.voltage=0
        
    def getHeight():
        return self.height
    

    def arduino(self, ardData):
        while True:
            try:
                #ardData[0]+=0.1
                #print("HI")
                data=int.from_bytes(ser.read(), byteorder='little')
                print(data)
                if data:
                    #data=str(data)
                    #print(data)
                    """threadLock.acquire()
                    program.stats.heightDisplay.setHeight(int(data))
                    threadLock.release()"""
                    #threadLock.acquire()
                    self.height=data
                    ardData[0]=data
                    log.write(str(data)+ '\n')
                    #print(ardData[0])
                    #print(self.height)
                    #threadLock.release()
                    if ser.inWaiting()>100:
                        ser.flushInput()
            except:
                print("Stecker draußen")
                log.write("Stecker draußen" + '\n')
                sleep(0.3)
                try:
                    ser = serial.Serial('COM3',9600)
                except:
                    pass
            
def close(event=None):
    def confirm():
        MASTER.destroy()
        quit()
    log.close()
    program.top.destroy()
    program.top = tk.Toplevel(MASTER,bg=BACKGROUND_COLOR,takefocus=True)
    program.top.geometry("300x150+"+str(int(WIDTH/2-150))+"+"+str(int(HEIGHT/2-75)))
    program.top.title("Quit?")
    program.top.resizable(False,False)
    l = tk.Label(program.top,text=choice(["Are you really\nfed up?","Do you really want\nto leave?","Do you really find the program\nthat boring?"]),bg=BACKGROUND_COLOR,fg=FOREGROUND_COLOR,font="Tahoma 14")
    l.place(x=10,y=10,width=260,height=90)
    qb = tk.Button(program.top,text="Quit",activebackground="#202020",activeforeground="#404040",
                   bg="#404040",fg=FOREGROUND_COLOR,font="Tahoma 15",relief=tk.FLAT,command=confirm)
    qb.place(x=15,y=105,width=130,height=40)
    cb = tk.Button(program.top,text="Cancel",activebackground="#202020",activeforeground="#404040",
                   bg="#404040",fg=FOREGROUND_COLOR,font="Tahoma 15",relief=tk.FLAT,command=program.top.destroy)
    cb.place(x=155,y=105,width=130,height=40)

def colorMultiply(color,multiplier):
    split = []
    for i in range(3):
        split.append(int(color[i*2+1:i*2+3],16))
    for i in range(3):
        split[i] = round(split[i]*multiplier)
        if split[i] > 255:
            split[i] = 255
        elif split[i] < 0:
            split[i] = 0
    color = "#"
    for i in split:
        cAdd = hex(i).split('x')[-1]
        if len(cAdd) != 2:
            cAdd = "0"+cAdd
        color += cAdd
    return color

def signum(number):
    if number > 0:
        return 1
    if number <  0:
        return -1
    if number == 0:
        return 0
    return number

def factorial(number):
    number = int(number)
    res = 0
    while number != 0:
        res += number
        number -= signum(number)
    return res

def spam():
    x = 0
    y = 0
    while True:
        for i in range(randint(42,100)):
            x = choice([math.sin(y),math.cos(y),math.tan(y)])
            y = choice([math.sin(x),math.cos(x),math.tan(x)])
log= open("C:\\Users\\olepe\\OneDrive\\Dokumente\\plane\\DataLogs\\log.txt","w+")
log.write("HI")
MASTER.title("Plane Simulator")
MASTER.attributes("-fullscreen", True)
#MASTER.iconbitmap(default='favicon.ico')
w = tk.Canvas(master=MASTER,bg=BACKGROUND_COLOR)
w.place(x=0,y=0,width=TRUEWIDTH,height=TRUEHEIGHT)
spiel = 42
program = Program()
#arduino_trd = threading.Thread(target=pragram.ardu.arduino)
mainloop_trd = threading.Thread(target=spam)
threadLock = threading.Lock()

if __name__ == '__main__':
    program = Program()
    ardData=Array("d",[0,1,2])
    ardu=ArduinoData()
    arduino_prc = Process(target=ardu.arduino, args=(ardData,))
  
    arduino_prc.start()
    print(ardData[2])

    program.mainloop(ardData)
#print("JOOJPHIJPGOKJ:GLKJ:LKJF:LKJ:HLKJGOFJ:OKFJ:ORJ")
#dataThread.join()
