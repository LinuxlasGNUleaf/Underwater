import tkinter
# from tkinter import *
import random
import time
from math import sqrt
import operator
import pickle


#save parameters
HIGHSCORE = "high.score2"

#window parameters
HEIGHT = 500
WIDTH = 800
TITLE = 'Bubble Blaster!'
BACKGROUND = 'darkblue'

#ship parameters
SCHIFF_R = 15
SCHIFF_COLOR = 'red'
SCHIFF_GESCHW = 10

#bubble parameters
MIN_BUB_R = 10
MAX_BUB_R = 30
MAX_BUB_GESCHW = 10
GAP = 100
BUB_COLOR = 'white'
BUB_CHANCE = 10

#time params
TIME_LIMIT = 30
BONUS_SCORE = 1000 

#relative parameters
MID_X = WIDTH/2
MID_Y = HEIGHT/2

#initializing
score = 0
bonus = 0
ende = time.time() + TIME_LIMIT

bub_id = list()
bub_r = list()
bub_geschw = list()

file = open(HIGHSCORE,'a+')
file.close()

#--->Set up of the window and canvas
window = tkinter.Tk()
window.title(TITLE)
canvas = tkinter.Canvas(window,width=WIDTH,height=HEIGHT, bg=BACKGROUND)
canvas.pack()
canvas.create_text(50,30,text='ZEIT',fill='white')
canvas.create_text(150,30,text='PUNKTE',fill='white')
time_text = canvas.create_text(50, 50, fill='white')
score_text = canvas.create_text(150,50,fill = 'white')

#---> Set up of the ship
schiff_id = canvas.create_polygon(5,5,5,25,30,15, fill = SCHIFF_COLOR)
schiff_id2 = canvas.create_oval(0,0,30,30,outline = SCHIFF_COLOR)
canvas.move(schiff_id,MID_X,MID_Y)
canvas.move(schiff_id2, MID_X,MID_Y)


def readHighscores():
    highscores = {}

    # read from file
    file = open(HIGHSCORE,"rb")

    try:
        highscores = pickle.load(file)
    except EOFError:
        print('Highscore file empty or corrupted!')

    file.close()
    print(highscores)
    return highscores   


def sortHighscoresbyValue(highscores):
    sorted_d = sorted(highscores.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_d



def addHighscore(name, score):

    #getting actual highscore list
    actual_hs = readHighscores()
    if actual_hs == 0:
        actual_hs[name] = score
    else:
        #appending new score
        if name in actual_hs:
            if (actual_hs[name] < score):
                actual_hs[name] = score
        else:
            actual_hs[name] = score
    
    #writing new list to file
    file = open(HIGHSCORE,"wb")
    pickle.dump(actual_hs,file)
    file.close()
    return actual_hs



#---> Moving the ship (event)
def schiff_beweg(event):
    if event.keysym == 'Up':
        canvas.move(schiff_id, 0, -SCHIFF_GESCHW)
        canvas.move(schiff_id2, 0, -SCHIFF_GESCHW)
    elif event.keysym == 'Down':
        canvas.move(schiff_id, 0, SCHIFF_GESCHW)
        canvas.move(schiff_id2, 0, SCHIFF_GESCHW)
    elif event.keysym == 'Left':
        canvas.move(schiff_id, -SCHIFF_GESCHW, 0)
        canvas.move(schiff_id2, -SCHIFF_GESCHW, 0)
    elif event.keysym == 'Right':
        canvas.move(schiff_id, SCHIFF_GESCHW, 0)
        canvas.move(schiff_id2, SCHIFF_GESCHW, 0)



#Registration of keybindings 
canvas.bind_all('<Key>',schiff_beweg)

# def moveS(x, y):
#     canvas.move(schiff_id,x*-1,y)
#     canvas.move(schiff_id2,x*-1,y)

def erstelleBubble():
    x = WIDTH + GAP
    y = random.randint(0, HEIGHT)
    r = random.randint(MIN_BUB_R, MAX_BUB_R)
    id1 = canvas.create_oval(x-r,y-r,x+r,y+r, outline=BUB_COLOR)
    bub_id.append(id1)
    bub_r.append(r)
    bub_geschw.append(random.randint(0,MAX_BUB_GESCHW))



def bewege_bubbles():
    for i in range(len(bub_id)):
        canvas.move(bub_id[i], -bub_geschw[i], 0)



def getCoordinates(id):
    pos = canvas.coords(id)
    x = ((pos[0]+pos[2])/2)
    y = ((pos[1]+pos[3])/2)
    return x,y



def deleteBubble(i):
    del bub_r[i]
    del bub_geschw[i]
    canvas.delete(bub_id[i])
    del bub_id[i]



def remove_OffScreen():
    for i in range(len(bub_id)-1,-1,-1):
        x,y = getCoordinates(bub_id[i])
        y + 1
        if (x < -GAP):
            deleteBubble(i)
            # print("{} deleted!".format(i))



def distance(id1,id2):
    x1, y1 = getCoordinates(id1)
    x2, y2 = getCoordinates(id2)
    return sqrt((x2-x1)**2 + (y2-y1)**2)



def collision():
    points = 0
    for bub in range(len(bub_id)-1, -1, -1):
        if (distance(schiff_id2, bub_id[bub]) < (SCHIFF_R + bub_r[bub])):
            points += (bub_r[bub] + bub_geschw[bub])
            deleteBubble(bub)
    return points



def show_points(score):
    canvas.itemconfig(score_text, text=str(score))



def show_time(time_left):
    canvas.itemconfig(time_text, text = str(time_left))
    


def endGame():
    for i in range(len(bub_id)-1,-1,-1):
        deleteBubble(i)
    canvas.delete(schiff_id)
    canvas.delete(schiff_id2)
    canvas.create_text(MID_X, MID_Y, text = 'GAME OVER', fill = 'white', font=('Helvetica','50'))
    canvas.create_text(MID_X, MID_Y+40, text = 'Punkte: {}'.format(score), fill = 'white',font=('Arial','20'))
    canvas.create_text(MID_X, MID_Y+60, text = 'Bonuszeit: {}'.format(bonus*TIME_LIMIT), fill = 'white',font=('Arial','20'))
    window.update()
    time.sleep(2)
    canvas.destroy()
    window.destroy()



def submitName():
    #retrieving input
    name = "Anonym"
    name2 = name_input.get("1.0",'end-1c')
    if (name2 != ""):
        name = name2 
    splitted = name.split("\n")
    print (splitted)
    name = splitted[len(splitted)-1]
    #deleting input field
    confirm_button.destroy()
    name_input.destroy()
    # s_canvas.destroy()

    #adding input (see also addHighscore())
    hs_list = sortHighscoresbyValue(addHighscore(name,score))

    text = ""
    if (len(hs_list) < 10):
        for i in range(len(hs_list)):
            a,b = hs_list[i]
            text += "{a}: {b}\n".format(a=a,b=b) 
    else:
        i = 0
        for key in hs_list:
            i += 1
            if (i > 10):
                continue
            text += "{a}: {b}\n".format(a=key, b=hs_list[key]) 
    print(text)
    s_canvas.config(height = 0)
    sb_text = tkinter.Text(scoreboard,width = 15, height = 10,font=("Helvetica", 32))
    sb_text.delete(0.0)
    sb_text.insert(0.0,text)
    sb_text.config(state="disabled")
    sb_text.pack()
    scoreboard.update()
    


#---> Main Loop
while time.time() < ende:
    #Randomly creating new bubbles
    if random.randint(1,BUB_CHANCE) == 1:
        erstelleBubble()

    #movement of bubbles
    bewege_bubbles()
    remove_OffScreen()

    #collisions
    score += collision()

    #bonus time
    if (int(score/BONUS_SCORE)) > bonus:
        bonus += 1
        ende += TIME_LIMIT
    
    #actualizing shown time and score
    show_points(score)
    show_time(int(ende-time.time()))

    #update screen and sleeping
    window.update()
    time.sleep(0.01)

endGame()

#---> Scoreboard
scoreboard = tkinter.Tk()
scoreboard.title('Scoreboard')
s_canvas = tkinter.Canvas(scoreboard,width=300,height=500, bg='white')
s_canvas.pack()
name_input = tkinter.Text(scoreboard, width=10, height = 1)
name_input.pack()



confirm_button = tkinter.Button(scoreboard, text="Enter", command=submitName)
confirm_button.pack()

# Getting the highscores from file
# h_list = readHighscores()
window.mainloop()