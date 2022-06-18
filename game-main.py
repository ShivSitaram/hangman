'''
USER CUSTOMIZATIONS
===================
'''
TARGET_WORD = '' #fill the quotes if you'd like a customized target word; otherwise, leave it blank, a random word would be chosen from the file below

WORD_FILE_NAME = 'wordlist.txt' #if you left TARGET_WORD with blank quotes, please fill this out with a file name that has a list of words seperated with newlines; a random word will be chosen from those words.
'''
===================
USER CUSTOMIZATIONS
'''

import tkinter as tk
import turtle as tur
import string as s
import random as ra
import re as r
import os as o

class App:

    def __init__(self, word, wordfilename):
        if not o.path.exists(wordfilename):
            print(f'You don\'t have the file \'{wordfilename}\' installed or in the same folder this python program is in. Please install it before running. This program will automatically quit.')
            exit()

        with open(wordfilename, 'r') as f:
            self.ws = [word.rstrip('\n').lower() for word in f.readlines() if not bool(r.search('[' + s.punctuation + ']', word)) and 2 <= len(word) <= 17]

        self.res_nes()

        self.mode = 1
        if word != '':
            self.mode = 0
            self.wrd = word

        self.score = 0

        self.root = tk.Tk()

        self.p_p_f = tk.Frame(self.root, width=625, height=100)
        self.p_p_lbl = tk.Label(self.p_p_f, text=f'{"".join(["_ " if ch == None else ch + " " for ch in self.rvld])}', font=('Times New Roman', '48'))
        self.p_l_lbl = tk.Label(self.root, text=f'Letters Removed: {str(self.l_rmvd)[1:-1]}', font=('Times New Roman', '25'))
        self.p_w_lbl = tk.Label(self.root, text=f'Words Removed: {str(self.w_rmvd)[1:-1]}', font=('Times New Roman', '25'))

        self.gss_lbl = tk.Label(self.root, text='Enter your word guess: ', font=('Times New Roman', '20'))
        self.gss_ent = tk.Entry(self.root, font=('Times New Roman', '20'), width=35)
        self.gss_bttn = tk.Button(self.root, text='Guess!', font=('Times New Roman', '20'))
        
        self.session_lbl = tk.Label(self.root, text=f'Session Score: {self.score}', font=('Times New Roman', '20'))
        self.play_ag_bttn = tk.Button(self.root, text='Play Again', font=('Times New Roman', '20'), command=self.reset)

        self.inst_bttn = tk.Button(self.root, text='Instructions', font=('Times New Roman', '20'), command=self.trigger_inst)

        self.letters = tk.Frame(self.root)
        self.letter_dict = {l:n for n, l in enumerate(s.ascii_lowercase)}
        self.letter_buttons = [(tk.Button(self.letters, text=(l.upper()), padx=20, pady=20, font=('Times New Roman', '25'), state='normal', command=lambda l=l: self.up_rvld(l, 1))) for l in s.ascii_lowercase]

        self.turtleCa = tur.Canvas(self.root, width=375, height=650)
        self.screen = tur.TurtleScreen(self.turtleCa)
        self.t = tur.RawTurtle(self.turtleCa)

        self.message = tk.Label(self.root, font=('Times New Roman', '40'))

    def res_nes(self):
        self.wrd = ra.choice(self.ws)
        self.rvld = [None] * len(self.wrd)
        self.prog = 0
        self.l_rmvd = []
        self.w_rmvd = []
        self.w_gssd = []

        #print(self.wrd)


    def start(self):
        self.gss_bttn.place(x=875, y=650)
        self.gss_lbl.place(x=400, y=600)
        self.gss_ent.place(x=600, y=600)

        columnnum = 0
        rownum = 0
        for num, i in enumerate(self.letter_buttons):
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
        
        self.message.config(text='Starting...', fg='black')

    def reload_buttons(self):
        self.p_p_lbl.config(text=f'{"".join(["_ " if ch == None else ch + " " for ch in self.rvld])}')
        self.p_l_lbl.config(text=f'Letters Removed: {str(self.l_rmvd)[1:-1]}')
        self.p_w_lbl.config(text=f'Words Removed: {str(self.w_rmvd)[1:-1]}')

    def reset(self):
        self.res_nes()

        for btn in self.letter_buttons:
            btn['state'] = 'normal'
        self.gss_bttn['state'] = 'normal'
        self.gss_ent['state'] = 'normal'

        self.message.config(text='Starting...', fg='black')

        self.reload_buttons()

        self.turtleCa.destroy()
        self.turtleCa = tur.Canvas(self.root, width=375, height=650)
        self.turtleCa.place(x=0, y=0)
        self.screen = tur.TurtleScreen(self.turtleCa)
        self.t = tur.RawTurtle(self.turtleCa)
        self.t.speed(0)
        self.t.hideturtle()

        self.play_ag_bttn.destroy()
        self.play_ag_bttn = tk.Button(self.root, text='Play Again', font=('Times New Roman', '20'), command=self.reset)

    def trigger_inst(self):
        popup = tk.Toplevel(self.root)
        popup.title('Instructions for Hangman')
        tk.Label(popup, text='''
You can guess either a letter or a word.
If you guess a letter and that letter is in the word, then the computer will reveal the places as to where it is in the word.
If you guess a letter and that letter is not in the word, then the computer will draw a man being hanged.
If you guess a word that is correct, you win!\nIf you guess a word that is not correct, the hangman gets hanged.
If you are able to reveal all the places of the word or guess it before the hangman is hanged, you win!
                                ''', font=('Times New Roman', '20')).pack()
        self.message.config(text='Instructions have been popped out.', fg='black')

    def up_rvld(self, gss, act):
        n_rvld = []
        hang_bool = False
        gss = gss.lower()
        if act == 1:
            n_rvld = [(gss if self.wrd[pl] == gss else None) if l == None else l for pl, l in enumerate(self.rvld)]
            if n_rvld == self.rvld:
                hang_bool = True
                self.l_rmvd.append(gss)
                self.message.config(text=f'"{gss}" is not in the word.', fg='red')
            else:
                self.message.config(text=f'"{gss}" is in the word.', fg='green')
            self.letter_buttons[self.letter_dict[gss]]['state'] = 'disabled'
            self.rvld = n_rvld
        elif act == 0:
            if not (bool(r.search('[' + s.punctuation + ']', gss)) or gss == '' or gss in self.w_gssd):
                if gss == self.wrd:
                    n_rvld = [l for l in self.wrd]
                else:
                    hang_bool = True
                    self.w_rmvd.append(gss)
                    n_rvld = self.rvld
                self.message.config(text=f'"{gss}" is not the word.', fg='red')
                self.rvld = n_rvld
                self.w_gssd.append(gss)
            self.gss_ent.delete(0, 'end')
        self.reload_buttons()
        if hang_bool:
            self.hang()
        if self.prog >=8 or self.rvld.count(None) == 0:
            self.end()

    def hang(self):
        if self.prog == 0:
            self.t.penup()
            self.t.goto(125, -20)
            self.t.pendown()
            self.t.goto(125, 300)
            self.t.goto(0, 300)
            self.t.goto(0, 275)
        elif self.prog == 1:
            self.t.left(180)
            self.t.circle(35)
        elif self.prog == 2:
            self.t.penup()
            self.t.goto(0, 205)
            self.t.pendown()
            self.t.goto(0, 185)
        elif self.prog == 3:
            self.t.goto(-100, 110)
        elif self.prog == 4:
            self.t.penup()
            self.t.goto(0, 185)
            self.t.pendown()
            self.t.goto(100, 110)
        elif self.prog == 5:
            self.t.penup()
            self.t.goto(0, 185)
            self.t.pendown()
            self.t.goto(0, 70)
        elif self.prog == 6:
            self.t.goto(-100, -5)
        elif self.prog == 7:
            self.t.penup()
            self.t.goto(0, 70)
            self.t.pendown()
            self.t.goto(100, -5)
        self.prog += 1

    def end(self):
        if self.prog >= 8:
            self.score -= 1
            self.message.config(text=f'You lost! The word was {self.wrd}.', fg='red')
        elif self.rvld.count(None) == 0:
            self.score += 1
            self.message.config(text='You won!', fg='green')

        self.session_lbl.config(text=f'Session Score: {self.score}')
        
        for btn in self.letter_buttons:
            btn['state'] = 'disabled'
        self.gss_bttn['state'] = 'disabled'
        self.gss_ent['state'] = 'disabled'

        if self.mode == 1:
            self.play_ag_bttn.place(x=720, y=0)
        

    def main(self):
        self.gss_ent.bind('<Return>', lambda event: self.up_rvld(self.gss_ent.get(), 0))
        self.gss_bttn.bind('<Button-1>', lambda event: self.up_rvld(self.gss_ent.get(), 0))
        self.p_p_f.place(x=375, y=0)
        self.p_p_lbl.place(relx=.5, rely=.5, anchor='center')
        self.p_l_lbl.place(x=0, y=650)
        self.p_w_lbl.place(x=0, y=700)
        self.letters.place(x=400, y=100)
        self.turtleCa.place(x=0, y=0)
        self.session_lbl.place(x=400, y=0)
        self.inst_bttn.place(x=865, y=0)
        self.t.speed(0)
        self.t.hideturtle()
        self.message.place(x=400, y=500)
        self.root.title('Hangman')
        self.root.geometry("1000x750+10+10")
        self.root.resizable(False, False)
        self.start()

        tk.mainloop()

hangman_app = App(TARGET_WORD, WORD_FILE_NAME)

if __name__ == '__main__':
    hangman_app.main()
