import chess
import chess.pgn
import io
import os

# Save image status move play
import chess.svg
from cairosvg import svg2png

# Game chess display board
import time
from IPython.display import display, HTML, clear_output

# Conver img to gif and mp4
import os
import imageio
import shutil
import cv2

# Audio
from gtts import gTTS
from playsound import playsound

# Generate image board

def save_board_game(board, uci, cont):
  boardsvg = chess.svg.board(board=board)
  name_board = str(cont) + str(uci)
  name_file = name_board 
  f = open("./temp/" + name_file + ".svg", "w")
  f.write(boardsvg)
  f.close()

  svg_code = open("./temp/" + name_file + ".svg", "rt").read()
  svg2png(bytestring=svg_code,write_to="./multimedia/" + name_file + ".png")


def save_board_stats(board, cont):
  boardsvg = chess.svg.board(board=board)
  name_board = str(cont) + "statusboard" # NAME BOARD INIT
  name_file = name_board 
  f = open("./temp/" + name_file + ".svg", "w")
  f.write(boardsvg)
  f.close()

  svg_code = open("./temp/" + name_file + ".svg", "rt").read()
  svg2png(bytestring=svg_code,write_to="./multimedia/" + name_file + ".png")

# Generate audio moves

def audio(uci, cont):
    name_mp3 = str(cont) + uci + ".mp3"
    audio = gTTS(uci, lang="en", tld="com") # Convert texto to audio
    audio.save("./audios_generate/" + name_mp3) # Save audio file
    return name_mp3

# Generate video board game

def gif(name_fl):
  path = './multimedia/'
  archivos = sorted(os.listdir(path))
  img_array_png = []
  #Leer todos los archivos formato imagen desde path
  for x in range(0, len(archivos)):
      nomArchivo = archivos[x]
      dirArchivo = path + str(nomArchivo)
      # Asignar a variable leer_imagen, el nombre de cada imagen
      leer_imagen = imageio.imread(dirArchivo)
      # añadir imágenes al arreglo img_array
      img_array_png.append(leer_imagen)
  #Guardar Gif
  imageio.mimwrite("./video_generate/" + name_fl + ".gif", img_array_png, 'GIF', duration=1.0)

# Generate game board

def who(player):
    return "White" if player == chess.WHITE else "Black"


def display_board(board, use_svg):
    if use_svg:
        return board._repr_svg_()
    else:
        return "<pre>" + str(board) + "</pre>"


def get_move(prompt):
    uci = input(prompt)
    if uci and uci[0] == "q":
        raise KeyboardInterrupt()
    try:
        chess.Move.from_uci(uci)
    except:
        uci = None
    return uci


def human_player(board):
    display(board)
    uci = get_move("%s's move [q to quit]> " % who(board.turn))
    legal_uci_moves = [move.uci() for move in board.legal_moves]
    while uci not in legal_uci_moves:
        print("Legal moves: " + (",".join(sorted(legal_uci_moves))))
        playsound("./resources/ilegal_move.wav")
        uci = get_move("%s's move[q to quit]> " % who(board.turn))
    return uci


def play_game(player1, player2, visual="svg", pause=0.1, cont=0):
    """
    playerN1, player2: functions that takes board, return uci move
    visual: "simple" | "svg" | None
    """
    use_svg = (visual == "svg")
    board = chess.Board() # Notation Forsyth-Edwards
    save_board_stats(board, cont)
    try:
        while not board.is_game_over(claim_draw=True):
            if board.turn == chess.WHITE:
                uci = player1(board)
            else:
                uci = player2(board)
            name = who(board.turn)
            board.push_uci(uci)
            
            cont += 1
            save_board_game(board, uci, cont)
            name_a = audio(uci,cont)
            playsound("./audios_generate/" + name_a)

            board_stop = display_board(board, use_svg)

            html = "<b>Move %s %s, Play '%s':</b><br/>%s" % (
                       len(board.move_stack), name, uci, board_stop)
            if visual is not None:
                if visual == "svg":
                    clear_output(wait=True)
                display(HTML(html))
                if visual == "svg":
                    time.sleep(pause)
    except KeyboardInterrupt:
        msg = "Game interrupted!"
        return (None, msg, board)
    result = None
    if board.is_checkmate():
        msg = "checkmate: " + who(not board.turn) + " wins!"
        playsound("./resources/checkmate.wav")
        result = not board.turn
    elif board.is_stalemate():
        msg = "draw: stalemate"
        playsound("./resources/draw_stalemate.wav")
    elif board.is_fivefold_repetition():
        msg = "draw: 5-fold repetition"
        playsound("./resources/draw_5-fold_repetition.wav")
    elif board.is_insufficient_material():
        msg = "draw: insufficient material"
        playsound("./resources/draw_insufficient_material.wav")
    elif board.can_claim_draw():
        msg = "draw: claim"
        playsound("./resources/draw_claim.wav")
    if visual is not None:
        print(msg)
    return (result, msg, board)


def main():
    playsound("./resources/" + "start_game.wav")
    play_game(human_player, human_player)
    
    gif("game_board_gif")
if __name__ == "__main__":
    main()
    
