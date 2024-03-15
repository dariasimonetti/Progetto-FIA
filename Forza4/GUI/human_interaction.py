import sys
from pygame.locals import *
from Forza4.GUI import constants
from Forza4.GUI.animations import *


def get_human_interaction(board, game_instance):
    dragging_token = False  # indica se il giocatore sta spostando un gettone
    tokenx, tokeny = None, None  # coordinate del gettone
    while True:
        for event in pygame.event.get():  # ciclo per gestire gli eventi

            if event.type == QUIT:  # se il giocatore chiude la finestra il gioco termina
                pygame.quit()
                sys.exit()

            elif (event.type == MOUSEBUTTONDOWN and not dragging_token and
                  game_instance.red_pile_rect.collidepoint(event.pos)):
                # il giocatore comincia a muovere il gettone e vengono registrate le sue coordinate
                dragging_token = True
                tokenx, tokeny = event.pos

            elif event.type == MOUSEMOTION and dragging_token:
                # aggiorna la posizione del gettone mentre viene trascianto
                tokenx, tokeny = event.pos