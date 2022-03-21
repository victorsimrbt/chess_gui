from chess import *
import tkinter as tk
from tkinter.font import *
from tkinter import *
import numpy as np
from tkinter.messagebox import *
import os

def_squares = []
move = None
pgn = ''
move_counter = 1
push_counter = 0


def select_squares(mainboard, square_idx, frame, details):
    global def_squares
    global move
    global pgn
    global move_counter, push_counter
    def_squares.append(square_idx)
    if len(def_squares) == 2:
        move = Move(def_squares[0], def_squares[1])
    if move:
        if move in list(mainboard.board.legal_moves):
            if push_counter % 2 == 0:
                pgn += str(move_counter)+'. '
                move_counter += 1
            pgn += str(mainboard.board.san(move)) + ' '

            pgnfont = Font(family="Trebuchet MS", size=10,
                           weight='bold')
            label = tk.Label(details, text=pgn,
                             font=pgnfont, bg='#263D42',
                             fg='white', wraplength=200)
            label.place(relx=0, rely=0.1)

            mainboard.board.push(move)
            mainboard.configure_images()
            mainboard.display_board(frame, details)

            push_counter += 1
        else:
            tk.messagebox.showwarning(
                title='Illegal Move', message='Illegal Move!')
        def_squares = []
        move = None
    if mainboard.board.is_game_over():
        tk.messagebox.showinfo(
            title='Game Over', message='Game Over. Board is Reset.')
        mainboard.board = Board()
        mainboard.configure_images()
        mainboard.display_board(frame, details)
        pgn = ''


class ChessBoard():
    def __init__(self):
        self.board = Board()
        self.squares = []
        self.configure_squares()

    def configure_squares(self):
        for i in range(64):
            square = Square(i, self.board)
            self.squares.append(square)

    def configure_images(self, idxs=np.arange(64)):
        for idx in idxs:
            self.squares[idx].get_img(self.board)

    def fine_configure(self, idx_list):
        for idx in idx_list:
            self.squares[idx].get_img()

    def display_board(self, frame, details, square_size=60):
        for square in self.squares:
            b = tk.Button(frame, image=square.image,
                          bg=square.color, borderwidth=0,
                          command=lambda idx=square.idx: select_squares(self, idx, frame, details))
            b.config(width=square_size, height=square_size)
            b.grid(row=square.row, column=square.column)


class Square():
    def __init__(self, idx, board):
        self.row = 8 - idx // 8
        self.column = idx % 8
        self.idx = idx

        if (self.row % 2 == self.column % 2):
            self.color = '#eeeed2'
        else:
            self.color = '#769656'
        self.get_img(board)

    def get_img(self, board):
        self.piece = board.piece_at(self.idx)
        piece = board.piece_at(self.idx)
        if piece:
            piece_symbol = piece.symbol()

            filename = ''
            if piece_symbol.isupper():
                filename = '_'

            filename += piece_symbol.lower()
            filename += '.png'

            self.image = PhotoImage(file=filename)
        else:
            self.image = PhotoImage()


os.chdir("pieces")

root = tk.Tk()
root.title('Chess GUI')
square_size = 80

canvas = tk.Canvas(root, height=500, width=700)
canvas.pack()

frame = tk.Frame(canvas, bg='white')
frame.place(width=500, height=500)

details = tk.Frame(canvas, bg='#263D42', width=700, height=500)
details.place(relx=500/700, rely=0)

chessboard = ChessBoard()
chessboard.display_board(frame, details)

fontStyle = Font(family="Trebuchet MS", size=15, weight='bold')
title = tk.Label(details, text="Chess GUI ",
                 font=fontStyle, bg='#263D42', fg='white')
title.place(relx=0, rely=0)
root.mainloop()
