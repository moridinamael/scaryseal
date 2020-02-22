# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 22:29:46 2019

@author: Matt
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 13:58:42 2019

@author: mfreeman
"""

import math
import time
from PIL import ImageGrab

def draw_circle(r,xcenter,ycenter):
    yarray,xarray = [],[]
    for xx in range(int(-1.0*r),r+1):
        xarray.append(xx+xcenter)
        yarray.append(math.sqrt(r*r-xx*xx)+ycenter)

    for xx in reversed(range(int(-1.0*r),r+1)):
        xarray.append(xx+xcenter)
        yarray.append(-1.0*math.sqrt(r*r-xx*xx)+ycenter)

    return zip(xarray,yarray)

class Ship:
    def centroid(self):
        return 1 / 3 * (self.x0 + self.x1 + self.x2), 1 / 3 * (self.y0 + self.y1 + self.y2)

    def __init__(self, canvas, x, y, width, height, turnspeed, acceleration=1):
        self._d = {'Up':1, 'Down':-1, 'Left':1, 'Right':-1}

        self.canvas = canvas
        self.width = width
        self.height = height
        self.speed = 0
        self.turnspeed = turnspeed
        self.acceleration = acceleration

        self.x0, self.y0 = x, y

        self.bearing = -math.pi / 2

        self.x1 = self.x0 + self.width / 2
        self.y1 = self.y0 - self.height

        self.x2 = self.x0 + self.width
        self.y2 = self.y0

        self.x, self.y = self.centroid()

        #self.ship = self.canvas.create_polygon((self.x0, self.y0, self.x1, self.y1, self.x2, self.y2), outline="white", width=3)


        #self.ship = self.canvas.create_polygon(draw_circle(10,xcenter=self.x0+100,ycenter=self.y0), outline="red", width=3)

    def changeCoords(self):
        self.canvas.coords(self.ship,self.x0, self.y0, self.x1, self.y1, self.x2, self.y2)

    def rotate(self, event=None):
        t = self._d[event.keysym] * self.turnspeed * math.pi / 180 # the trig functions generally take radians as their arguments rather than degrees; pi/180 radians is equal to 1 degree

        self.bearing -= t

        def _rot(x, y):
            #note: the rotation is done in the opposite fashion from for a right-handed coordinate system due to the left-handedness of computer coordinates
            x -= self.x
            y -= self.y
            _x = x * math.cos(t) + y * math.sin(t)
            _y = -x * math.sin(t) + y * math.cos(t)
            return _x + self.x, _y + self.y

        self.x0, self.y0 = _rot(self.x0, self.y0)
        self.x1, self.y1 = _rot(self.x1, self.y1)
        self.x2, self.y2 = _rot(self.x2, self.y2)
        self.x, self.y = self.centroid()

        self.changeCoords()

    def accel(self, event=None):
        mh = int(self.canvas['height'])
        mw = int(self.canvas['width'])
        self.speed += self.acceleration * self._d[event.keysym]

        self.x0 += self.speed * math.cos(self.bearing)
        self.x1 += self.speed * math.cos(self.bearing)
        self.x2 += self.speed * math.cos(self.bearing)

        self.y0 += self.speed * math.sin(self.bearing)
        self.y1 += self.speed * math.sin(self.bearing)
        self.y2 += self.speed * math.sin(self.bearing)

        self.x, self.y = self.centroid()

        if self.y < - self.height / 2:
            self.y0 += mh
            self.y1 += mh
            self.y2 += mh
        elif self.y > mh + self.height / 2:
            self.y0 += mh
            self.y1 += mh
            self.y2 += mh

        if self.x < -self.width / 2:
            self.x0 += mw
            self.x1 += mw
            self.x2 += mw
        elif self.x > mw + self.width / 2:
            self.x0 -= mw
            self.x1 -= mw
            self.x2 -= mw

        self.x, self.y = self.centroid()

        self.changeCoords()

from Tkinter import *

def rotate_pivot(pointx,pointy,pivotx,pivoty,angle):
    s = math.sin(angle)
    c = math.cos(angle)
    xshift = pointx-pivotx
    yshift = pointy-pivoty
    xnew   = xshift*c - yshift*s
    ynew   = xshift*s + yshift*c
    newpoint_x = xnew+pivotx
    newpoint_y = ynew+pivoty
    return newpoint_x,newpoint_y




class Game:
    def __init__(self, gameWidth, gameHeight):
        self.root = Tk()
        self.gameWidth = gameWidth
        self.gameHeight = gameHeight
        self.gameWindow()

        self.ship = Ship(self.canvas, x=self.gameWidth / 2,y=self.gameHeight / 2, width=50, height=50, turnspeed=10, acceleration=5)

        basic_dimension = 100*2.0/3.0*math.sqrt(3.0)

        self.x0 = self.gameWidth/2
        self.y0 = self.gameHeight/2


        c1 = draw_circle(int(basic_dimension),xcenter=self.x0,ycenter=self.y0)
        self.canvas.create_polygon(c1, outline="red", width=3)
        #self.canvas.create_polygon(draw_circle(int(basic_dimension),0,0), outline="red", width=3)
        self.canvas.create_polygon(draw_circle(int(basic_dimension/1.6179),xcenter=self.x0,ycenter=self.y0), outline="red", width=3)
        self.canvas.create_polygon(draw_circle(int(basic_dimension/1.6179/1.6179),xcenter=self.x0,ycenter=self.y0), outline="red", width=3)
        #self.canvas.create_polygon(draw_circle(int(16.179),xcenter=self.x0-basic_dimension/2,ycenter=self.y0-100), outline="red", width=3)
        #self.canvas.create_polygon(draw_circle(10,xcenter=self.x0-basic_dimension/2,ycenter=self.y0-100), outline="red", width=3)
        #self.canvas.create_polygon(draw_circle(int(16.179),xcenter=self.x0-basic_dimension/2,ycenter=self.y0+100), outline="red", width=3)


        first_axis = {}
        second_axis = {}
        moonmap = {}



        r = 16.179
        tag = "mover6"
        cmx,cmy = self.x0-basic_dimension/2,self.y0-100
        cm = draw_circle(int(r),cmx,cmy)
        self.canvas.create_polygon(cm, outline="red", width=3, tags=tag)
        first_axis[tag] = [cm,cmx,cmy]

        # Moon

        #r = 2.0
        #offset = 20.0
        #tag = "mover6moon"
        #moonmap["mover6moon"] = "mover6"
        #cmx,cmy = self.x0-basic_dimension/2,self.y0-100+offset
        #cm = draw_circle(int(r),cmx,cmy)
        #self.canvas.create_polygon(cm, outline="red", width=3, tags=tag)
        #first_axis[tag] = [cm,cmx,cmy]


        r = 10.0
        tag = "mover5"
        cmx,cmy = self.x0-basic_dimension/2,self.y0-100
        cm = draw_circle(int(r),cmx,cmy)
        self.canvas.create_polygon(cm, outline="red", width=3, tags=tag)
        first_axis[tag] = [cm,cmx,cmy]

        r = 16.179
        tag = "mover4"
        cmx,cmy = self.x0-basic_dimension/2,self.y0+100
        cm = draw_circle(int(r),cmx,cmy)
        self.canvas.create_polygon(cm, outline="red", width=3, tags=tag)
        first_axis[tag] = [cm,cmx,cmy]

        r = 10.0
        tag = "mover3"
        cmx,cmy = self.x0-basic_dimension/2,self.y0+100
        cm = draw_circle(int(r),cmx,cmy)
        self.canvas.create_polygon(cm, outline="red", width=3, tags=tag)
        first_axis[tag] = [cm,cmx,cmy]

        r = 16.179
        cmx2,cmy2 = self.x0+100*(2.0/3.0)*math.sqrt(3.0),self.y0+0
        cm2 = draw_circle(int(r),cmx2,cmy2)
        self.canvas.create_polygon(cm2, outline="red", width=3, tags="mover2")
        first_axis["mover2"] = [cm2,cmx2,cmy2]

        r = 10.0
        cmx1,cmy1 = self.x0+100*(2.0/3.0)*math.sqrt(3.0),self.y0+0
        cm1 = draw_circle(int(r),cmx1,cmy1)
        self.canvas.create_polygon(cm1, outline="red", width=3, tags="mover1")
        first_axis["mover1"] = [cm1,cmx1,cmy1]

        r = 10.0
        tag = "moveri1"
        cmxi1,cmyi1 = self.x0+100/1.6179/2,self.y0-100/1.6179 #self.x0+100/1.6179*(2.0/3.0)*math.sqrt(3.0),self.y0+0
        cmi1 = draw_circle(int(r),cmxi1,cmyi1)
        self.canvas.create_polygon(cmi1, outline="red", width=3, tags="moveri1")
        first_axis[tag] = [cmi1,cmxi1,cmyi1]
        
        r = 10.0
        tag = "moveri2"
        cmxi2,cmyi2 = self.x0-100/1.6179*(2.0/3.0)*math.sqrt(3.0),self.y0+0 #self.x0-100/1.6179/2,self.y0-100/1.6179
        cmi2 = draw_circle(int(r),cmxi2,cmyi2)
        self.canvas.create_polygon(cmi2, outline="red", width=3, tags=tag)
        first_axis[tag] = [cmi2,cmxi2,cmyi2]

        r = 10.0
        tag = "moveri3"
        cmxi3,cmyi3 = self.x0+100/1.6179/2,self.y0+100/1.6179
        cmi3 = draw_circle(int(r),cmxi3,cmyi3)
        self.canvas.create_polygon(cmi3, outline="red", width=3, tags=tag)
        first_axis[tag] = [cmi3,cmxi3,cmyi3]
        
        reverse_rotation = ["moveri1","moveri2","moveri3"]

        currentcx,currentcy,prevx,prevy = {},{},{},{}
        for planet in first_axis:
            cm,cmx,cmy = first_axis[planet]
            currentcx[planet],currentcy[planet] = cmx,cmy
            prevx[planet],prevy[planet]=cmx,cmy
        """
        for planet in second_axis:
            cm,cmx,cmy,cmxm,cmym = second_axis[planet]
            currentcx[planet],currentcy[planet] = cmx,cmy
            prevx[planet],prevy[planet]=cmx,cmy
        """

        for kk in range(0,5000):

            for planet in first_axis:
                cm,cmx,cmy = first_axis[planet]
                if(planet in moonmap):
                    ctr_x,ctr_y = currentcx[moonmap[planet]],currentcy[moonmap[planet]]
                    #prevx[planet],prevy[planet]=currentcx[moonmap[planet]],currentcy[moonmap[planet]]
                else:
                    ctr_x,ctr_y = self.x0,self.y0

                if planet in reverse_rotation:
                    rotation_speed = -0.001
                else:
                    rotation_speed = 0.001
                currentcx[planet],currentcy[planet] = rotate_pivot(currentcx[planet],currentcy[planet],ctr_x,ctr_y,rotation_speed*math.pi)
                self.canvas.move(planet,currentcx[planet]-prevx[planet],currentcy[planet]-prevy[planet])
                prevx[planet],prevy[planet]=currentcx[planet],currentcy[planet]

            """
            for moon in second_axis:
                cm,cmx,cmy,cmxm,cmym = second_axis[moon]
                currentcx[moon],currentcy[moon] = rotate_pivot(currentcx[moon],currentcy[moon],cmxm,cmym,0.01*math.pi)
                self.canvas.move(planet,currentcx[moon]-prevx[moon],currentcy[moon]-prevy[moon])
                prevx[moon],prevy[moon]=currentcx[moon],currentcy[moon]
            """

            time.sleep(0.01)
            self.canvas.update()
                #self.canvas.bitmap(file="img"+str(kk)+".bmp",colormode='color')
                #ImageGrab.grab((0,0,self.gameWidth*3,self.gameHeight*3)).save("img"+str(kk)+".jpg")

        #self.root.mainloop()
        self.root.destroy()

        #self.root.bind('<Left>', self.ship.rotate)
        #self.root.bind('<Right>', self.ship.rotate)
        #self.root.bind('<Up>', self.ship.accel)
        #self.root.bind('<Down>', self.ship.accel)

        #self.root.mainloop()

    def gameWindow(self):
        self.frame = Frame(self.root)
        self.frame.pack(fill=BOTH, expand=YES)

        self.canvas = Canvas(self.frame,width=self.gameWidth, height=self.gameHeight, bg="black", takefocus=1)
        self.canvas.pack(fill=BOTH, expand=YES)

asteroids = Game(1000,1000) #300,300)