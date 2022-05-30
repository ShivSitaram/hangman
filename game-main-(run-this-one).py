import tkinter as tk
import turtle as tur
import string as s
from random import choice as c
from re import search as r

def start():
    place_nes()
    place_gss()
    place_lt_btns()

def place_nes():
    global p_p_lbl
    global p_l_lbl
    global p_w_lbl
    reload_buttons()
    p_p_lbl.place(x=400, y=0)
    p_l_lbl.place(x=0, y=900)
    p_w_lbl.place(x=0, y=950)

def del_nes():
    global p_p_lbl
    global p_l_lbl
    global p_w_lbl
    p_p_lbl.destroy()
    p_l_lbl.destroy()
    p_w_lbl.destroy()

def place_gss():
    global gss_lbl
    global gss_ent
    global gss_bttn
    gss_bttn.place(x=975, y=850)
    gss_lbl.place(x=400, y=850)
    gss_ent.place(x=600, y=850)

def reload_buttons():
    global p_p_lbl
    global p_l_lbl
    global p_w_lbl
    p_p_lbl = tk.Label(root, text=f'{"".join(["_ " if ch == None else ch + " " for ch in rvld])}', font=('Times New Roman', '48'), anchor='n')
    p_l_lbl = tk.Label(root, text=f'Letters Removed: {str(l_rmvd)[1:-1]}', font=('Times New Roman', '25'))
    p_w_lbl = tk.Label(root, text=f'Words Removed: {str(w_rmvd)[1:-1]}', font=('Times New Roman', '25'))

def place_lt_btns():
    global letter_buttons
    #letter_buttons[0].grid(row=0, column=0)
    columnnum = 0
    rownum = 0
    for num, i in enumerate(letter_buttons):
        if num < 24:
            i.grid(row=rownum, column=columnnum)
            columnnum += 1
            if columnnum == 6:
                rownum += 1
                columnnum = 0
        else:
            if num == 24:
                i.grid(row=4, column=2)
            elif num == 25:
                i.grid(row=4, column=3)

def up_rvld(gss, act):
    global up_rvld_response
    global letter_buttons
    global letter_dict
    global wrd
    global rvld
    global gss_ent
    n_rvld = []
    hang_bool = False
    if act == 1:
        n_rvld = [(gss if wrd[pl] == gss else None) if l == None else l for pl, l in enumerate(rvld)]
        if n_rvld == rvld:
            hang_bool = True
            l_rmvd.append(gss)
        letter_buttons[letter_dict[gss]]['state'] = 'disabled'
    else:
        if bool(r('[' + s.punctuation + ']', gss)) or gss == '':
            gss_ent.delete(0, 'end')
        else:
            if gss == wrd:
                n_rvld = [l for l in wrd]
            else:
                hang_bool = True
                w_rmvd.append(gss)
                n_rvld = rvld
        gss_ent.delete(0, 'end')
    rvld = n_rvld
    del_nes()
    place_nes()
    if hang_bool:
        hang()
    if prog >=8 or rvld.count(None) == 0:
        end()

def hang():
    global prog
    global t
    if prog == 0:
        t.penup()
        t.goto(125, -20)
        t.pendown()
        t.goto(125, 300)
        t.goto(0, 300)
        t.goto(0, 275)
    elif prog == 1:
        t.left(180)
        t.circle(35)
    elif prog == 2:
        t.penup()
        t.goto(0, 205)
        t.pendown()
        t.goto(0, 185)
    elif prog == 3:
        t.goto(-100, 110)
    elif prog == 4:
        t.penup()
        t.goto(0, 185)
        t.pendown()
        t.goto(100, 110)
    elif prog == 5:
        t.penup()
        t.goto(0, 185)
        t.pendown()
        t.goto(0, 70)
    elif prog == 6:
        t.goto(-100, -5)
    elif prog == 7:
        t.penup()
        t.goto(0, 70)
        t.pendown()
        t.goto(100, -5)
    prog = prog + 1

with open('all words.txt', 'r') as f:
    ws = [word.rstrip('\n').lower() for word in f.readlines() if not bool(r('[' + s.punctuation + ']', word))]

wrd = c(ws)
#wrd = 'ENTER WORD HERE'
rvld = [None] * len(wrd)
#{0: L, 1: head, 2: neck, 3: arm, 4: arm 2, 5: body, 6: leg, 7: second leg}
prog = 0
l_rmvd = []
w_rmvd = []
l_gssd = []
w_gssd = []

root = tk.Tk()
root.title('Hangman')
root.geometry("1100x1000+10+10")

wrd_gss = tk.StringVar()

p_p_lbl = None
p_l_lbl = None
p_w_lbl = None

gss_lbl = tk.Label(root, text='Enter your word guess: ', font=('Times New Roman', '20'))
gss_ent = tk.Entry(root, textvariable=wrd_gss, font=('Times New Roman', '20'), width=35)
gss_ent.bind('<Return>', lambda: up_rvld(gss_ent.get(), 0))
gss_bttn = tk.Button(root, text='Guess!', font=('Times New Roman', '20'), command=lambda: up_rvld(gss_ent.get(), 0))

letters = tk.Frame(root)
letters.place(x=500, y=300)
letter_dict = {l:n for n, l in enumerate(s.ascii_lowercase)}
letter_buttons = [(tk.Button(letters, text=(l.upper()), padx=20, pady=20, font=('Times New Roman', '25'), state='normal', command=lambda l=l: up_rvld(l, 1))) for l in s.ascii_lowercase]

turtleCa = tur.Canvas(root, width=375, height=900)
turtleCa.place(x=0, y=0)
screen = tur.TurtleScreen(turtleCa)
t = tur.RawTurtle(turtleCa)
t.speed(0)
t.hideturtle()

start()

def end():
    global letter_buttons
    global gss_bttn
    global gss_ent
    if prog >= 8:
        tk.Label(root, text='You lost! The word was ' + wrd + '.', fg='red', font=('Times New Roman', '40')).place(x=400, y=750)
    elif rvld.count(None) == 0:
        tk.Label(root, text='You won!', fg='green', font=('Times New Roman', '40')).place(x=400, y=750)
    for btn in letter_buttons:
        btn['state'] = 'disabled'
    gss_bttn['state'] = 'disabled'
    gss_ent['state'] = 'disabled'
for module in [tur, tk, root, letters, turtleCa]:
    module.mainloop()
