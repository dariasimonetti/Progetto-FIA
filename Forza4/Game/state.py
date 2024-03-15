infinity = float('inf')


class State:
    """
    State classe che rappresenta lo stato del gioco
    il tabellone è rappresentato come una bitboard 6x7
    -  -   -   -   -   -   -
    5  12  19  26  33  40  47
    4  11  18  25  32  39  46
    3  10  17  24  31  38  45
    2  9   16  23  30  37  44
    1  8   15  22  29  36  43
    0  7   14  21  28  35  42
    """

    status = 3

    def _init_(self, ai_position, game_position, depth=0):
        # inizializza gli attributi
        self.ai_position = ai_position
        self.game_position = game_position
        self.depth = depth

    @property  # decoratore di proprietà, il metoto diventa una proprietò di sola lettura
    def player_position(self):
        # esecuzione di uno XOR tra le due posizioni per ottenere la player position
        return self.ai_position ^ self.game_position

    @staticmethod
    def is_winning_state(position):
        # controlla se ci sono 4 pedine dello stesso giocatore allineate orizzontalmente
        m = position & (position >> 7)  # controllo allineamento
        if m & (m >> 14):  # controllo allineamento consecutivo
            return True
        # controllo per le diagonali inclinate da sinistra a destra
        m = position & (position >> 6)
        if m & (m >> 12):
            return True
        # controllo per le diagonali inclinate da sinistra a destra
        m = position & (position >> 8)
        if m & (m >> 16):
            return True
        # controllo per le pedine allineate verticalmente
        m = position & (position >> 1)
        if m & (m >> 2):
            return True
        # se nessuno dei controlli precedenti è andato a buon fine allora nessuno ha (ancora) vinto
        return False

    def calculate_positional_score(self, position):
        # calcola un punteggio basato sulla disposizione delle pedine sul tabellone per uno specifico giocatore
        score = 0

        # vengono aggiunti punti per le combinazioni di pedine vicine alla vittoria

        # 4 pedine dello stesso giocatore in una riga, con una cella vuota
        score += self.score_near_winning(position, 4, 3)

        # 3 pedine dello stesso giocatore in una riga, con una cella vuota
        score += self.score_near_winning(position, 3, 2)

        # 2 pedine dello stesso giocatore in una riga, con una cella vuota
        score += self.score_near_winning(position, 2, 1)  # 2 in una riga con una cella vuota

        return score


    def generate_children(self, who_went_first):
        # genera tutti i possibili stati successivi (figli) a partire dallo stato attuale del gioco

        for i in range(0, 7):  # itera attraverso le colonne del tabellone
            # l'iterzione comincia dal centro del tabellone muovendosi verso gli estremi cosi: [3,2,4,1,5,0,6]
            column = 3 + (1 - 2 * (i % 2)) * (i + 1) // 2

            # viene controllato se è possibile fare una mossa in quella colonna, verificando se la riga più alta della
            # colonna è libera, cioè se non c'è alcuna pedina in quella posizione
            if not self.game_position & (1 << (7 * column + 5)):

                if (who_went_first == -1 and self.depth % 2 == 0) or (who_went_first == 0 and self.depth % 2 == 1):
                    # Mossa dell'IA (MAX)
                    new_ai_position, new_game_position = make_move(self.ai_position, self.game_position, column)
                else:
                    # Mossa del giocatore (MIN)
                    new_ai_position, new_game_position = make_move_opponent(self.ai_position, self.game_position,
                                                                            column)

                # usiamo yield per restituire lo stato figlio corrente. Questo permette di iterare attraverso tutti
                # gli stati figli generati dalla funzione generate_children uno alla volta.
                yield State(new_ai_position, new_game_position, self.depth + 1)