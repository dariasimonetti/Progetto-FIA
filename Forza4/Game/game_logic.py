import random
from ..Game.state import *
from ..GUI.human_interaction import *
from ..GUI.animations import *
from ..GUI.constants import *


class ForzaQuattroGame:
    AI = -1
    PLAYER = 0

    def _init_(self, game_board, game_instance):
        self.game_instance = game_instance  # interfaccia grafica
        self.current_state = State(0, 0)  # stato inziale del gioco con posizione di ia e player impostate a 0

        # generazione numero randomico per decidere chi inizia
        random_number = random.randint(1, 2)
        if random_number == 2:
            self.turn = self.PLAYER
        else:
            self.turn = self.AI

        self.first = self.turn  # indica chi ha cominciato per prima il gioco
        self.board = game_board  # configurazione del tabellone

    def is_game_over(self):
        # se la partita è stata vinta da qualcuno
        if self.has_winning_state():
            # stampa chi ha vinto (~ è utilizzato per invertire i bit e cambiare il turno)
            print("Ha vinto l'IA!") if ~self.turn == self.AI else print("Congratulazioni, hai vinto!")
            return True

        # se la partita è finita in pareggio stampa un messaggio
        elif self.draw():
            print("Pareggio...Grazie... Torna a trovarci")
            return True
        return False

    def draw(self):
        # controlla se la partita è stata pareggiata
        return State.is_draw(self.current_state.game_position) and not self.has_winning_state()

    def has_winning_state(self):
        # controlla se la partita è stata vinta a prescindere che sia dall'ia o dall'umano
        return State.is_winning_state(self.current_state.ai_position) or State.is_winning_state(
            self.current_state.player_position)

    def next_turn(self):
        # controlla di chi è il turno e in base a ciò chiama la funzione corrispondente
        if self.turn == self.AI:
            self.query_ai(self.game_instance)
        else:
            self.query_player()

        # applica il complemento a 1 per il cambio di turno
        self.turn = ~self.turn

    def query_player(self):
        print("\nMossa del giocatore...")
        column = None
        # ciclo per ottenere la colonna in cui si vuole mettere la pedina
        while column is None:
            # column = input('Your move identify column [0-6]? ')
            try:
                # column = int(column)
                column = get_human_interaction(self.board, self.game_instance)  # ottiene la colonna attraverso
                # l'interfaccia grafica
                # controlla se la colonna è valida (compresa tra 0 e 6)
                if not 0 <= column <= 6:
                    raise ValueError
                # controlla se la colonna è piena (tramite una maschera bit a bit)
                if self.current_state.game_position & (1 << (7 * column + 5)):
                    raise IndexError
            except (ValueError, IndexError):
                print("Invalid move. Try again...")
                column = None

        # esecuzione della mossa
        drop_human_token(self.board, column, self.game_instance)

        # calcola la nuova posizione e la nuova posizione di gioco
        new_position, new_game_position = make_move(self.current_state.player_position,
                                                    self.current_state.game_position, column)

        # aggiorna lo stato corrente del gioco con la nuova posizione di gioco e incrementa la profondità di uno.
        self.current_state = State(self.current_state.ai_position, new_game_position, self.current_state.depth + 1)