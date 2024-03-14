import sys
from pygame.locals import *
import pygame
from Forza4.GUI import constants


class Tabellone:
    def _init_(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.display_surf = pygame.display.set_mode((constants.WINDOWWIDTH, constants.WINDOWHEIGHT))
        pygame.display.set_caption('Forza 4 contro IA')

        # pile di rettangoli per le pedine rosse e nere
        self.red_pile_rect = pygame.Rect(int(constants.SPACESIZE / 2), constants.WINDOWHEIGHT -
                                         int(3 * constants.SPACESIZE / 2), constants.SPACESIZE, constants.SPACESIZE)

        self.black_pile_rect = pygame.Rect(constants.WINDOWWIDTH - int(3 * constants.SPACESIZE / 2),
                                           constants.WINDOWHEIGHT - int(3 * constants.SPACESIZE / 2),
                                           constants.SPACESIZE, constants.SPACESIZE)

        # caricamento immagini dei gettoni rossi e neri e delle caselle del tabellone
        self.red_token_img = pygame.image.load('images/4row_red.png')
        self.red_token_img = pygame.transform.smoothscale(self.red_token_img, (constants.SPACESIZE,
                                                                               constants.SPACESIZE))

        self.black_token_img = pygame.image.load('images/4row_black.png')
        self.black_token_img = pygame.transform.smoothscale(self.black_token_img, (constants.SPACESIZE,
                                                                                   constants.SPACESIZE))

        self.board_img = pygame.image.load('images/4row_board.png')
        self.board_img = pygame.transform.smoothscale(self.board_img, (constants.SPACESIZE, constants.SPACESIZE))

        # caricamento e posizionamento centrale delle immagini per indicare chi vince
        self.human_winner_img = pygame.image.load('images/4row_humanwinner.png')
        self.computer_winner_img = pygame.image.load('images/4row_computerwinner.png')
        self.tie_winner_img = pygame.image.load('images/4row_tie.png')
        self.winner_rect = self.human_winner_img.get_rect()
        self.winner_rect.center = (int(constants.WINDOWWIDTH / 2), int(constants.WINDOWHEIGHT / 2))

    def process_game_over(self, winner, board):
        winner_img = self.computer_winner_img if winner == constants.COMPUTER else self.human_winner_img if winner == constants.HUMAN else self.tie_winner_img

        # loop infinito per mantenere la finestra di gioco aperta fino a quando si clicca sul mouse (inizio nuova
        # partita) o si chiude la finestra(fine del programma).
        while True:

            # mostra l'immagine che indica chi ha vinto sovrapponendola a quella del tabellone
            self.draw_board(board)
            self.display_surf.blit(winner_img, self.winner_rect)
            pygame.display.update()
            self.clock.tick()

            for event in pygame.event.get():  # loop per gestire gi eventi
                if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONUP:
                    return

    @staticmethod
    def get_new_board():  # crea e restituisce una configurazione vuota del tabellone
        board = []
        # iterazione sulle colonne del tabellone, crea una lista di liste che rappresentano le colonne e ogni elemento
        # delle colonne è inizializzato a empty per indicare una cella vuota
        for x in range(constants.BOARDWIDTH):
            board.append([constants.EMPTY] * constants.BOARDHEIGHT)
        return board