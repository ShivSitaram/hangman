from random import choice as c
import turtle as tur
import string as s
import re as r

with open('all words.txt', 'r') as f:
    ws = [word.rstrip('\n').lower() for word in f.readlines() if not bool(r.search('[' + s.punctuation + ']', word)) and len(word) >= 2]

wrd = c(ws)
#wrd = 'ENTER WORD HERE'
rvld = [None] * len(wrd)
#{0: L, 1: head, 2: neck, 3: arm, 4: arm 2, 5: body, 6: leg, 7: second leg}
prog = 0
l_rmvd = []
w_rmvd = []
l_gssd = []
w_gssd = []


def frmt_rvld(rvld):
    return ''.join(['_ ' if ch == None else ch + ' ' for ch in rvld])

def frmt_rmvd(rmvd):
    return str(rmvd)[1:-1]

def i_act():
    act = None
    act_dict = {'l': 1, 'w': 0}
    while act != 'l' and act != 'w':
        act = input("Would you like to guess a letter or the word? {'l': guess letter, 'w': guess word} ").lower()
    return act_dict[act]

def i_gss(act):
    gss = '!!!'
    global l_gssd
    global w_gssd
    if act == 1:
        prmpt = 'Enter your letter guess: '
        while gss not in s.ascii_lowercase or gss in l_gssd or gss == '':
            gss = input(prmpt).lower()
        l_gssd.append(gss)
    elif act == 0:
        prmpt = 'Enter your word guess: '
        while gss not in ws or gss in w_gssd or gss == '':
            gss = input(prmpt).lower()
        w_gssd.append(gss)
    return gss

def up_rvld(gss, act, wrd, rvld):
    n_rvld = []
    hang = False
    if act == 1:
        n_rvld = [(gss if wrd[pl] == gss else None) if l == None else l for pl, l in enumerate(rvld)]
        if n_rvld == rvld:
            hang = True
            l_rmvd.append(gss)
    else:
        if gss == wrd:
            n_rvld = [l for l in wrd]
        else:
            hang = True
            w_rmvd.append(gss)
    return [n_rvld, hang]

def hang(prog, t):
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
    return prog + 1

def main():
    trwn = tur.Screen()
    t = tur.Turtle()
    t.speed(0)
    t.hideturtle()
    global prog
    global rvld
    #print(word)
    print('Let\'s play hangman! I\'ve thought about my word already.')
    print('Make sure \'Python Turtle Graphics\' is open.\n')
    while prog < 8 and rvld.count(None) != 0:
        print(f'\nLetters removed: {frmt_rmvd(l_rmvd)}')
        print(f'Words removed: {frmt_rmvd(w_rmvd)}')
        print(f'Places revealed: {frmt_rvld(rvld)}\n')
        act = i_act()
        data = up_rvld(i_gss(act), act, wrd, rvld)
        rvld = data[0]
        if data[1]:
            prog = hang(prog, t)
    if prog == 8:
        print('You lost! The word was ' + wrd + '.')
    elif rvld.count(None) == 0:
        print('You won! The word was ' + wrd + '.')


main()
