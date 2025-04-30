import pygame
import chess
import chess.svg
import io
import cairosvg
import cv2
import numpy as np
from utils import ensure_dir
import os 

SQUARE_SIZE = 60
DIMENSION = 8

def board_to_surface(board):
    svg = chess.svg.board(board=board).encode("utf-8")
    png = cairosvg.svg2png(bytestring=svg)
    image = pygame.image.load(io.BytesIO(png))
    return pygame.transform.scale(image, (SQUARE_SIZE * DIMENSION, SQUARE_SIZE * DIMENSION))

def play_game(agent_fn, filename, depth=2):
    pygame.init()
    screen = pygame.display.set_mode((SQUARE_SIZE * DIMENSION, SQUARE_SIZE * DIMENSION))
    clock = pygame.time.Clock()
    board = chess.Board()
    video = []

    while not board.is_game_over():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        _, move = agent_fn(board.copy(), depth, board.turn)
        board.push(move)
        surface = board_to_surface(board)
        screen.blit(surface, (0, 0))
        pygame.display.flip()
        video.append(pygame.surfarray.array3d(screen).swapaxes(0, 1))
        clock.tick(2)

    save_video(video, filename)
    pygame.quit()

def save_video(frames, filename):
    ensure_dir(os.path.dirname(filename))
    height, width, _ = frames[0].shape
    out = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'mp4v'), 2, (width, height))
    for frame in frames:
        out.write(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
    out.release()
