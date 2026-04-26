import pygame
import sys
import datetime
from tools import *

pygame.init()

SCREEN_WIDTH=900
SCREEN_HEIGHT=600
TOOLBAR_HEIGHT=80

BLACK=(0,0,0)
WHITE=(255,255,255)
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)
YELLOW=(255,255,0)
CYAN=(0,255,255)
MAGENTA=(255,0,255)
ORANGE=(255,165,0)
PURPLE=(128,0,128)
GRAY=(128,128,128)
LIGHT_GRAY=(200,200,200)

MODE_BRUSH="brush"
MODE_LINE="line"
MODE_RECT="rectangle"
MODE_SQUARE="square"
MODE_CIRCLE="circle"
MODE_RIGHT_TRI="right_triangle"
MODE_EQ_TRI="equilateral"
MODE_ISO_TRI="isosceles"
MODE_RHOMBUS="rhombus"
MODE_ERASER="eraser"
MODE_BUCKET="bucket"
MODE_TEXT="text"

BRUSH_SIZES=[2,5,10]
brush_index=1
brush_size=BRUSH_SIZES[brush_index]

screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Paint")
clock=pygame.time.Clock()

class Button:

    def __init__(self,x,y,w,h,color,text=""):
        self.rect=pygame.Rect(x,y,w,h)
        self.color=color
        self.text=text
        self.font=pygame.font.Font(None,18)

    def draw(self,surface):
        pygame.draw.rect(surface,self.color,self.rect)
        pygame.draw.rect(surface,BLACK,self.rect,2)

        if self.text:
            txt=self.font.render(self.text,True,BLACK)
            surface.blit(txt,txt.get_rect(center=self.rect.center))

    def clicked(self,pos):
        return self.rect.collidepoint(pos)

class ColorPalette:

    def __init__(self,x,y):

        self.colors=[BLACK,WHITE,RED,GREEN,BLUE,YELLOW,
                     CYAN,MAGENTA,ORANGE,PURPLE,GRAY]

        self.rects=[]
        self.selected=BLACK

        for i,c in enumerate(self.colors):
            r=pygame.Rect(x+i*35,y,30,30)
            self.rects.append((r,c))

    def draw(self,surf):

        for r,c in self.rects:
            pygame.draw.rect(surf,c,r)
            pygame.draw.rect(surf,BLACK,r,1)

            if c==self.selected:
                pygame.draw.rect(surf,WHITE,r,3)

    def check(self,pos):

        for r,c in self.rects:
            if r.collidepoint(pos):
                self.selected=c
                return True

        return False

def main():

    global brush_index,brush_size

    canvas=pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT-TOOLBAR_HEIGHT))
    canvas.fill(WHITE)

    undo_stack=[]
    redo_stack=[]

    drawing=False
    start=None
    current=None

    mode=MODE_BRUSH
    color=BLACK

    typing=False
    text=""
    text_pos=(0,0)
    font=pygame.font.SysFont(None,28)

    buttons=[
        Button(10,5,60,25,GRAY,"Brush"),
        Button(75,5,60,25,GRAY,"Line"),
        Button(140,5,60,25,GRAY,"Rect"),
        Button(205,5,60,25,GRAY,"Square"),
        Button(270,5,60,25,GRAY,"Circle"),
        Button(335,5,60,25,GRAY,"R-Tri"),
        Button(400,5,60,25,GRAY,"E-Tri"),
        Button(465,5,60,25,GRAY,"Rhomb"),
        Button(530,5,60,25,GRAY,"Erase"),
        Button(595,5,60,25,GRAY,"Bucket"),
        Button(660,5,60,25,GRAY,"Text"),
        Button(725,5,50,25,GRAY,"S"),
        Button(780,5,50,25,GRAY,"M"),
        Button(835,5,50,25,GRAY,"L")
    ]

    palette=ColorPalette(10,40)

    running=True

    while running:

        mx,my=pygame.mouse.get_pos()
        cy=my-TOOLBAR_HEIGHT

        for e in pygame.event.get():

            if e.type==pygame.QUIT:
                running=False

            elif e.type==pygame.KEYDOWN:

                if e.key==pygame.K_s and pygame.key.get_mods()&pygame.KMOD_CTRL:

                    timestamp=datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename=f"canvas_{timestamp}.png"
                    pygame.image.save(canvas,filename)

                if e.key==pygame.K_z and pygame.key.get_mods()&pygame.KMOD_CTRL:

                    if undo_stack:
                        redo_stack.append(canvas.copy())
                        canvas.blit(undo_stack.pop(),(0,0))

                if e.key==pygame.K_y and pygame.key.get_mods()&pygame.KMOD_CTRL:

                    if redo_stack:
                        undo_stack.append(canvas.copy())
                        canvas.blit(redo_stack.pop(),(0,0))

                if typing:

                    if e.key==pygame.K_RETURN:
                        img=font.render(text,True,color)
                        canvas.blit(img,text_pos)
                        typing=False
                        text=""

                    elif e.key==pygame.K_ESCAPE:
                        typing=False
                        text=""

                    elif e.key==pygame.K_BACKSPACE:
                        text=text[:-1]

                    else:
                        text+=e.unicode

            elif e.type==pygame.MOUSEBUTTONDOWN:

                x,y=e.pos

                if y<TOOLBAR_HEIGHT:

                    for i,b in enumerate(buttons):

                        if b.clicked(e.pos):

                            if i==0: mode=MODE_BRUSH
                            elif i==1: mode=MODE_LINE
                            elif i==2: mode=MODE_RECT
                            elif i==3: mode=MODE_SQUARE
                            elif i==4: mode=MODE_CIRCLE
                            elif i==5: mode=MODE_RIGHT_TRI
                            elif i==6: mode=MODE_EQ_TRI
                            elif i==7: mode=MODE_RHOMBUS
                            elif i==8: mode=MODE_ERASER
                            elif i==9: mode=MODE_BUCKET
                            elif i==10: mode=MODE_TEXT
                            elif i==11: brush_index=0
                            elif i==12: brush_index=1
                            elif i==13: brush_index=2

                            brush_size=BRUSH_SIZES[brush_index]

                    palette.check(e.pos)
                    color=palette.selected

                else:

                    undo_stack.append(canvas.copy())

                    if mode==MODE_BUCKET:
                        target=canvas.get_at((x,cy))[:3]
                        flood_fill(canvas,(x,cy),target,color)
                        continue

                    if mode==MODE_TEXT:
                        typing=True
                        text=""
                        text_pos=(x,cy)
                        continue

                    drawing=True
                    start=(x,cy)
                    current=start

            elif e.type==pygame.MOUSEMOTION:

                if drawing:
                    current=(mx,cy)

                    if mode==MODE_BRUSH:
                        pygame.draw.line(canvas,color,start,current,brush_size)
                        start=current

                    elif mode==MODE_ERASER:
                        pygame.draw.line(canvas,WHITE,start,current,brush_size)
                        start=current

            elif e.type==pygame.MOUSEBUTTONUP:

                if drawing and start and current:

                    if mode==MODE_LINE:
                        pygame.draw.line(canvas,color,start,current,brush_size)

                    elif mode==MODE_RECT:
                        pygame.draw.rect(canvas,color,norm_rect(*start,*current),brush_size)

                    elif mode==MODE_SQUARE:

                        x1,y1=start
                        x2,y2=current

                        s=max(abs(x2-x1),abs(y2-y1))
                        x=x1 if x2>=x1 else x1-s
                        y=y1 if y2>=y1 else y1-s

                        pygame.draw.rect(canvas,color,(x,y,s,s),brush_size)

                    elif mode==MODE_CIRCLE:

                        r=int(((current[0]-start[0])**2+(current[1]-start[1])**2)**0.5)

                        pygame.draw.circle(canvas,color,start,r,brush_size)

                    elif mode==MODE_RIGHT_TRI:
                        draw_right_triangle(canvas,color,start,current,brush_size)

                    elif mode==MODE_EQ_TRI:
                        draw_equilateral_triangle(canvas,color,start,current,brush_size)

                    elif mode==MODE_ISO_TRI:
                        draw_isosceles_triangle(canvas,color,start,current,brush_size)

                    elif mode==MODE_RHOMBUS:
                        draw_rhombus(canvas,color,start,current,brush_size)

                drawing=False
                start=None
                current=None

        screen.fill(GRAY)
        screen.blit(canvas,(0,TOOLBAR_HEIGHT))

        if drawing:
            temp=screen.copy()
            preview(temp,mode,start,current,brush_size)
            screen.blit(temp,(0,0))

        pygame.draw.rect(screen,LIGHT_GRAY,(0,0,SCREEN_WIDTH,TOOLBAR_HEIGHT))

        for b in buttons:
            b.draw(screen)

        palette.draw(screen)

        if typing:
            img=font.render(text,True,color)
            screen.blit(img,text_pos)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__=="__main__":
    main()