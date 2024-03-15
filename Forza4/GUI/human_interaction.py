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

            elif event.type == MOUSEBUTTONUP and dragging_token:
                # il gettone viene rilasciato
                # se viene rilasciato nella parte alta dello schermo (sopra il tabellone) viene calcolata
                # la colonna dove è stato rilasciato
                if (tokeny < constants.YMARGIN and
                        constants.XMARGIN < tokenx < constants.WINDOWWIDTH - constants.XMARGIN):
                    column = int((tokenx - constants.XMARGIN) / constants.SPACESIZE)
                    return column
                # altrimenti si riporta il gettone come se non fosse stato mosso
                tokenx, tokeny = None, None
                dragging_token = False

                # se il gettone è in movimento e rilasciato in una posiizone valida viene ridisegnata la scacchiera con
                # il gettone rosso nelle nuove coordinate
            if tokenx is not None and tokeny is not None:
                game_instance.draw_board(board,
                                         {'x': tokenx - int(constants.SPACESIZE / 2),
                                          'y': tokeny - int(constants.SPACESIZE / 2), 'color': constants.RED})

                # altrimenti viene ridisegnata la scacchiera senza il gettone aggiunto
            else:
                game_instance.draw_board(board)

            pygame.display.update()
            game_instance.clock.tick()

