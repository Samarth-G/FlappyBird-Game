from tkinter import *
import random

GAMECOUNTER = 0
GAMESPEED = 30
GAME = True
path_to_score = "highscore.txt"

height = 700
width = 700

BIRDvelocity = 8
PIPEvelocity = 8
UpForce = 8

BIRD_Y = height/2
PIPE_X = width
PIPESIZE = 120
PIPEDISTANCE = 8 * 60

pipelist = []
endcards = []

jumps = 0
SCORE = 0
HighScore = 0

window = Tk()
window.title("Flappy Bird")
canvas = Canvas(height=height, width=width, bg="skyblue", bd=0)
canvas.pack()

scoreboard = canvas.create_text(80, 40, text="Score: 0", font=("", 30))
highboard = canvas.create_text(80, 70, text=(
    "High Score: " + str(HighScore)), font=("", 15))
canvas.tag_raise(scoreboard)
canvas.tag_raise(highboard)

imageBIRD = PhotoImage(file="assets/bird.gif")
imageBIRDUP = PhotoImage(file="assets/birdup.gif")
imageBIRDDOWN = PhotoImage(file="assets/birddown.gif")

bird = canvas.create_image(120, BIRD_Y, image=imageBIRD)
canvas.tag_lower(bird)


def pipecreate():
    global PIPE_X

    minrand = imageBIRD.height() + (UpForce * 10)
    maxrand = minrand * 1.5

    gap = random.randint(minrand, maxrand)
    up_height = random.randint(50, (height - (gap + 50)))
    down_height = up_height + gap

    pipe_up = canvas.create_rectangle(PIPE_X, 0, (PIPE_X + PIPESIZE), up_height, fill="darkgreen")
    pipe_down = canvas.create_rectangle(PIPE_X, 700, (PIPE_X + PIPESIZE), down_height, fill="darkgreen")

    canvas.tag_lower(pipe_up)
    canvas.tag_lower(pipe_down)

    pipelist.append([pipe_up, pipe_down, up_height, down_height, PIPE_X])


def gravity():
    global BIRD_Y

    BIRD_Y += BIRDvelocity
    if BIRD_Y >= 700-(imageBIRD.height()/3):
        BIRD_Y = 700-(imageBIRD.height()/3)
        gameover()

    if jumps == 0:
        canvas.itemconfigure(bird, image=imageBIRDDOWN)

    canvas.coords(bird, 120, BIRD_Y)
    if GAME:
        window.after(GAMESPEED, gravity)


def jump(event=None):
    global BIRD_Y
    global jumps

    if jumps == 1:
        canvas.itemconfigure(bird, image=imageBIRDUP)

    if GAME:
        BIRD_Y -= UpForce
        if BIRD_Y <= 0 + (imageBIRD.height() / 2):
            BIRD_Y = 0 + (imageBIRD.height() / 2)

        canvas.coords(bird, 120, BIRD_Y)

    if jumps < 10:
        window.after(10, jump)
        jumps += 1
    else:
        jumps = 0


def pipemotion():
    global SCORE
    global PIPEvelocity
    global GAMESPEED

    for pipe in pipelist:

        pipe[4] = pipe[4] - PIPEvelocity
        canvas.coords(pipe[0], pipe[4], 0, (pipe[4] + PIPESIZE), pipe[2])
        canvas.coords(pipe[1], pipe[4], 700, (pipe[4] + PIPESIZE), pipe[3])

        if pipe[4] == width - PIPEDISTANCE:
            pipecreate()

        if (pipe[4] + PIPESIZE) < 0:
            canvas.delete(pipe[0])
            canvas.delete(pipe[1])
            pipelist.pop(0)

            SCORE += 1
            canvas.itemconfigure(scoreboard, text=("Score: " + str(SCORE)))

        else:
            collision(pipe[2], pipe[3], pipe[4])

    if GAME:
        window.after(GAMESPEED, pipemotion)


def collision(up_height, down_height, cord_x):
    global SCORE

    if cord_x <= 120 + imageBIRD.width()/3 and \
            (cord_x + PIPESIZE) >= 120 - imageBIRD.width()/3:

        if BIRD_Y - imageBIRD.height()/3 <= up_height or \
                BIRD_Y + imageBIRD.height()/2 >= down_height:
            gameover()


def gameover():
    global GAME
    global HighScore

    GAME = False
    print("GAME OVER")

    if SCORE > HighScore:
        endcard = [canvas.create_text(350, 300, text="GAME OVER", font=("", 50)),
             canvas.create_text(350, 350, text=("-- NEW HIGH SCORE = " + str(SCORE) + " --"), font=("", 30)),
             canvas.create_text(350, 380, text="Press ENTER to restart")]

        HighScore = SCORE
        scorefile = open(path_to_score, "w+")
        scorefile.write(str(HighScore))

    else:
        endcard = [canvas.create_text(350, 300, text="GAME OVER", font=("", 50)),
             canvas.create_text(350, 340, text="Press ENTER to restart")]

    for item in endcard:
        endcards.append(item)

    window.bind("<Return>", restartgame)


def restartgame(event=None):
    global SCORE
    global BIRD_Y
    global GAME
    global pipelist
    global endcards

    BIRD_Y = height/2
    canvas.itemconfigure(bird, image=imageBIRD)
    SCORE = 0
    canvas.itemconfigure(scoreboard, text=("Score: " + str(SCORE)))

    for item in pipelist:
        canvas.delete(item[0])
        canvas.delete(item[1])

    for item in endcards:
        canvas.delete(item)

    pipelist = []
    endcards = []
    GAME = True
    main()


def main():
    global GAMECOUNTER
    global HighScore

    GAMECOUNTER += 1

    scorefile = open(path_to_score)
    HighScore = int(scorefile.read())
    scorefile.close()

    canvas.itemconfigure(highboard, text=("High Score: " + str(HighScore)))

    print()
    print("START", GAMECOUNTER)

    window.after(GAMESPEED, pipecreate)
    window.after(GAMESPEED, pipemotion)
    window.after(GAMESPEED, gravity)


if __name__ == "__main__":
    window.bind("<space>", jump)
    main()

window.mainloop()
