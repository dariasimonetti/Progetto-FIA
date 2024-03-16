import pygame

from ..GUI.constants import *


def animate_dropping_token(board, column, color, game_instance):
    x = XMARGIN + column * SPACESIZE  # coordinata x iniziale del gettone, calcolata in base alla colonna specificata
    y = YMARGIN - SPACESIZE  # coordinata y iniziale del gettone, impostata sopra la parte superiore del tabellone
    drop_speed = 2.0  # velocità caduta del gettone

    lowest_empty_space = game_instance.get_lowest_empty_space(board, column)  # indice della riga più bassa vuota
    # nella colonna

    while True:

        y += int(drop_speed)  # incrementa la coordinata y del gettone in base alla velocità di caduta
        drop_speed += 2  # incremento velocità di caduta per simulare accelerazione

        # Controlla se la coordinata y del gettone ha raggiunto o superato l'indice della riga identificato prima.
        # Se è vero, termina l'animazione.
        if int((y - YMARGIN) / SPACESIZE) >= lowest_empty_space:
            return

        # viene disegnata una nuova scacchiera durante ogni iteazione dell'animazione
        game_instance.draw_board(board, {'x': x, 'y': y, 'color': color})
        pygame.display.update()
        game_instance.clock.tick()


def animate_computer_moving(board, column, game_instance):
    x = game_instance.black_pile_rect.left  # coordinata x del gettone nero, corrispondente alla pila di gettoni
    y = game_instance.black_pile_rect.top  # coordinata y del gettone nero, corrispondente alla pila di gettoni
    speed = 2.0  # velocità del gettone

    # ciclo per animare il gettone nero spostandolo dalla pila fino alla parte superiore del tabellone,
    # aumentando la velocità dell'animazione
    while y > (YMARGIN - SPACESIZE):
        y -= int(speed)
        speed += 1
        # viene ridisegnata la scacchiera per ogni iterazione dell'animazione
        game_instance.draw_board(board, {'x': x, 'y': y, 'color': BLACK})
        pygame.display.update()
        game_instance.clock.tick()

    # spostamento del gettone lateralmente verso la colonna indicata
    y = YMARGIN - SPACESIZE
    speed = 2.0
    while x > (XMARGIN + column * SPACESIZE):
        x -= int(speed)
        speed += 1.0
        game_instance.draw_board(board, {'x': x, 'y': y, 'color': BLACK})
        pygame.display.update()
        game_instance.clock.tick()

    # chiamata alla funzione per l'animazione della caduta del gettone nero
    animate_dropping_token(board, column, BLACK, game_instance)