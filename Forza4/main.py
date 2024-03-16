from Forza4.Game.game_logic import *
from GUI.graphic_game_logic import Tabellone
from GUI import constants


if __name__ == "_main_":
    print("Benvenuto a Forza 4")

    game_instance = Tabellone()

    while True:
        # Inizializzazione tabellone vuoto
        game_board = game_instance.get_new_board()
        game_instance.draw_board(game_board)
        game_instance.update_display()
        # Inizializzazione della logica di gioco
        game = ForzaQuattroGame(game_board, game_instance)
        # Ciclo per la gestione dei turni e aggiornamento grafico finchè il gioco non si conclude
        while not game.is_game_over():
            game.next_turn()
            print_board(game.current_state)
            game_instance.draw_board(game.board)
            game_instance.update_display()

        # Necessario alla GUI per far comparire chi ha vinto
        WINNER = '' if game.draw() else constants.COMPUTER if ~game.turn == -1 else constants.HUMAN
        game_instance.process_game_over(WINNER, game.board)