import kivy
from datetime import datetime
import threading
import time
import socket
import base64

from kivy.config import Config
Config.set('graphics', 'resizable', False)

from kivy.core.window import Window
from kivy.app import App
from kivy.graphics import Color,RoundedRectangle
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager,Screen

Window.size=(450,550)
Window.clearcolor = (0/255,0/255,0/255,1)

dply=0
bts=[]
blanks=[]
found=0
speed=100
max_speed=False

def check():
    global bts
    dict={}
    for row in bts:
        for i in range(9):
            if row[i].text==' ':
                continue
            if row[i].text in dict:
                return False
            dict[row[i].text]=1
        dict.clear()
    for i in range(9):
        for j in range(9):
            #print(f"{j}-{i}-{bts[j][i].text}")
            #print(dict)
            if bts[j][i].text==' ':
                continue
            if bts[j][i].text in dict:
                return False
            dict[bts[j][i].text]=1
        dict.clear()
    vv=[(0,0),(0,3),(0,6),(3,0),(3,3),(3,6),(6,0),(6,3),(6,6)]
    for tup in vv:
        for i in range(tup[0],tup[0]+3):
            for j in range(tup[1],tup[1]+3):
                if bts[i][j].text==' ':
                    continue
                if bts[i][j].text in dict:
                    return False
                dict[bts[i][j].text]=1
        dict.clear()
    return True

def recur(depth):
    global found
    global blanks
    global bts
    global speed
    global max_speed

    if max_speed==False:
        time.sleep(speed*0.0001)
    if found==1:
        return
    if depth==len(blanks):
        #print(f"At {depth}")
        found=1
        return
    else:
        for i in range(1,10):
            blanks[depth].text=str(i)
            blanks[depth].color=(0,1,0,1)
            if check():
                recur(depth+1)
            if found==1:
                return
        blanks[depth].text=str(' ')

def solve_sud(buton):
    global bts
    global blanks
    global found

    blanks.clear()
    found=0
    for row in bts:
        for but in row:
            if but.text==' ':
                blanks.append(but)
    buton.disabled=True
    recur(0)
    buton.disabled=False
    print("Here!")

class Sudoku_SolverApp(App):
    def initialize(self, d, text,buton):
        global dply
        global bts
        dply=d
        if text=="Start":
            tmp=[]
            for i in range(1,82):
                bt=Button(size_hint=(None,None),size=(50,50),font_size=16,text=str(' '),on_press=self.press)
                tmp.append(bt)
                if len(tmp)==9:
                    bts.append(tmp)
                    tmp=[]
                dply.add_widget(bt)
            v=[[5,3,' ',' ',7,' ',' ',' ',' '],[6,' ',' ','1',9,'5',' ',' ',' '],[' ',9,'8',' ',' ',' ',' ','6',' '],[8,' ',' ',' ','6',' ',' ',' ','3'],[4,' ',' ','8',' ','3',' ',' ','1'],[7,' ',' ',' ',2,' ',' ',' ','6'],[' ',6,' ',' ',' ',' ','2','8',' '],[' ',' ',' ','4','1','9',' ',' ','5'],[' ',' ',' ',' ','8',' ',' ','7','9']]
            r=0
            c=0
            for row in bts:
                for but in row:
                    but.text=str(v[r][c])
                    c=c+1
                r=r+1
                c=0
        else:
            t1=threading.Thread(target=solve_sud,args=(buton,),daemon=True)
            t1.start()

    def press(self1,self):
        print(f"Pressed!")
        if self.text==' ':
            self.text="1"
        else:
            self.text=str(int(self.text)+1)

    def slid(self, slid):
        global speed
        speed=1001-slid.value

    def toggle_max(self):
        global max_speed
        if max_speed:
            max_speed=False
        else:
            max_speed=True
    def clear(self):
        global bts
        v=[[5,3,' ',' ',7,' ',' ',' ',' '],[6,' ',' ','1',9,'5',' ',' ',' '],[' ',9,'8',' ',' ',' ',' ','6',' '],[8,' ',' ',' ','6',' ',' ',' ','3'],[4,' ',' ','8',' ','3',' ',' ','1'],[7,' ',' ',' ',2,' ',' ',' ','6'],[' ',6,' ',' ',' ',' ','2','8',' '],[' ',' ',' ','4','1','9',' ',' ','5'],[' ',' ',' ',' ','8',' ',' ','7','9']]
        r=0
        c=0
        for row in bts:
            for but in row:
                but.text=str(v[r][c])
                c=c+1
            r=r+1
            c=0

    def build(self):
        return Builder.load_file("design.kv")

Sudoku_SolverApp().run()
print("Exitted!")
