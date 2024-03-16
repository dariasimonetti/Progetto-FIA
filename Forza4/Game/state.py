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

    def __init__(self, ai_position, game_position, depth=0):
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

    @staticmethod
    def is_draw(position):
        # controllo pareggio: si scorrono tutte le colonne del tabellone e si controlla per ognuno l'ultimo spazio vuoto
        # (quello piu in alto), se è occupato per tutte le colonne allora c'è un pareggio
        return all(position & (1 << (7 * column + 5)) for column in range(0, 7))

    def terminal_node_test(self):
        # controllo se lo stato attuale del gioco è un nodo terminale, quindi la partita è terminata.

        # controllo se l'ia ha vinto
        if self.is_winning_state(self.ai_position):
            self.status = -1
            return True

        # controllo se ha vinto il giocatore umano
        elif self.is_winning_state(self.player_position):
            self.status = 1
            return True

        # controllo se è finita in pareggio
        elif self.is_draw(self.game_position):
            self.status = 0
            return True

        # se nessuno dei controlli è soddisfatto la partita è ancora in corso
        else:
            return False

    def calculate_heuristic(self):
        # valutazione euristica dello stato del gioco,  progettata per guidare l'algoritmo di ricerca verso mosse che
        # sembrano promettenti dalla prospettiva dell'IA

        if self.status == -1:  # l'IA ha vinto
            return 1000 - self.depth  # Punteggio più alto per vittoria, penalizzato dalla profondità (meno mosse sono
            # preferibili)

        elif self.status == 1:  # Il giocatore ha vinto
            return -1000 + self.depth  # Viene assegnato un unteggio più basso per la vittoria del giocatore
            # penalizzato dalla profondità

        elif self.status == 0:  # pareggio
            return 0  # punteggio neutro
        else:
            # Calcolo di una valutazione basata sulla posizione delle pedine sul tabellone

            # calcolo del punteggio dell'ia
            ai_score = self.calculate_positional_score(self.ai_position)

            # calcolo del punteggio del giocatore
            player_score = self.calculate_positional_score(self.player_position)

            # differenza dei punteggi resituita come valutazione
            return ai_score - player_score

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

    @staticmethod
    def score_near_winning(position, count_required, empty_space):

        # Calcola il punteggio per le combinazioni di pedine vicine alla vittoria.

        score = 0
        # ciclo che scorre ogni cella del tabellone
        for row in range(6):
            for col in range(7):

                # Per ogni cella del tabellone, il metodo controlla il valore della cella che sarà 1 se la cella è
                # occupata da quel giocatore, 0 altrimenti
                cell_value = (position >> (7 * col + row)) & 1

                # Per ogni cella del tabellone che contiene una pedina del giocatore corrente:
                if cell_value == 1:

                    # il metodo controlla se ci sono count_required pedine consecutive in una riga.
                    if col <= 7 - count_required:
                        # Il controllo si estende verso sinistra per verificare se ci sono abbastanza pedine consecutive
                        # e se ci sono abbastanza celle vuote sulla sinistra per formare una combinazione vincente.
                        if bin(position >> (7 * col + row)).count('1') == count_required:
                            score += empty_space

                    #  il metodo controlla se ci sono count_required pedine consecutive in una colonna.
                    if row <= 6 - count_required:
                        # il controllo si estende per verificare se ci sono abbastanza celle vuote per effettuare una
                        # mossa vicino alla vittoria
                        if bin(position >> (7 * col + row)).count('1') == count_required:
                            score += empty_space

                        # il metodo controlla diagonalmente verso destra
                    if col <= 7 - count_required and row <= 6 - count_required:
                        if bin(position >> (7 * col + row)).count('1') == count_required:
                            score += empty_space

                        # il metodo controlla diagonalmente verso sinistra
                    if col >= count_required - 1 and row <= 6 - count_required:
                        if bin(position >> (7 * col + row)).count('1') == count_required:
                            score += empty_space

                        # se count_required è uguale a 3, viene aggiunto un punteggio aggiuntivo per i blocchi di 3
                    if count_required == 3 and col <= 7 - count_required and row <= 6 - count_required:
                        if bin(position >> (7 * col + row)).count('1') == count_required - 1:
                            score += empty_space / 2  # Punteggio aggiuntivo per i blocchi di 3

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


def alphabeta_search(state, turn=-1, d=7):
    # algoritmo di ricerca con potatura alpha-beta

    # Definizione delle funzioni che rappresentano i nodi MAX e MIN nell'algoritmo MiniMax. Esplorano ricorsivamente i
    # nodi dell'albero di gioco e calcolano il valore associato ad ogni stato

    # la funzione max_value è responsabile di esplorare i nodi di tipo MAX nell'albero di gioco e restituire il valore
    # massimo ottenibile da tale nodo
    def max_value(state, alpha, beta, depth):
        if cutoff_search(state, depth):  # controlla se lo stato corrente è uno stato terminale o se la profondità
            # massima di ricerca è stata raggiunta
            return state.calculate_heuristic()  # in caso affermativo viene resituito il valore euristico dello stato

        v = -infinity  # valore massimo che il nodo MAX può ottenere esplorando i suoi figli

        # iterazione sui figli
        for child in state.generate_children(turn):

            if child in seen:  # se il figlio è stato già visto allora si passa al prossimo
                continue

            v = max(v, min_value(child, alpha, beta,
                                 depth + 1))  # viene calcolato il valore minimo che il nodo MIN può
            # ottenere esplorando i suoi figli. Il massimo tra il valore corrente di v e il valore calcolato per il
            # figlio viene quindi assegnato a v.

            seen[child] = alpha

            if v >= beta:  # Se il valore di v diventa maggiore o uguale a beta, viene eseguita la potatura Alpha-Beta
                # l'algoritmo restituisce immediatamente il valore di v, poiché il nodo MIN ignorerà completamente
                # questo ramo in quanto il suo valore non può essere superiore a beta.
                return v

            alpha = max(alpha, v)  # alpha viene aggiornata al massimo tra il suo valore corrente e il valore di v

        if v == -infinity:
            # Se il valore di v rimane -infinity, significa che non è stata trovata nessuna vittoria/sconfitta/pareggio
            # fino a questo punto
            return infinity
        return v

    # la funzione esplora i nodi di tipo MIN nell'albero di gioco e restituire il valore minimo ottenibile da tale nodo
    def min_value(state, alpha, beta, depth):

        if cutoff_search(state, depth):  # controlla se lo stato corrente è uno stato terminale o se la profondità
            # massima di ricerca è stata raggiunta
            return state.calculate_heuristic()  # in caso affermativo viene resituito il valore euristico dello stato

        v = infinity  # valore minimo che il nodo MIN può ottenere esplorando i suoi figli

        for child in state.generate_children(turn):
            if child in seen:
                continue

            v = min(v, max_value(child, alpha, beta, depth + 1))  # calcolo del valore massimo che il nodo MAX può
            # ottenere esplorando i suoi figli. Il minimo tra il valore corrente di v e il valore calcolato per il
            # figlio viene quindi assegnato a v.

            seen[child] = alpha

            if v <= alpha:  # Se il valore di v diventa mminore o uguale ad aplha, viene eseguita la potatura Alpha-Beta
                # l'algoritmo restituisce immediatamente il valore di v, poiché il nodo MAX ignorerà completamente
                # questo ramo in quanto il suo valore non può essere inferiore ad alpha.
                return v

            beta = min(beta, v)  # beta viene aggiornata al minimo tra il suo valore corrente e il valore di v

        if v == infinity:
            # Se il valore di v rimane infinity, significa che non è stata trovata nessuna vittoria/sconfitta/pareggio
            # fino a questo punto
            return -infinity
        return v

    # dizionario seen per tenere traccia degli stati già visitati.
    seen = {}

    # corpo dell'algoritmo:

    # funzione cutoff_search restituisce True se lo stato corrente è terminale o se la profondità massima di ricerca è
    # stata raggiunta, altrimenti restituisce False.
    cutoff_search = (lambda state, depth: depth > d or state.terminal_node_test())

    best_score = -infinity
    beta = infinity
    best_action = None

    for child in state.generate_children(turn):  # iterazione su tutti i figli dello stato corrente
        # per ogni figlio:
        v = min_value(child, best_score, beta, 1)  # calcolo del valore che rappresenta la valutazione dell'azione
        # per il giocatore corrente.

        if v > best_score:  # se v è maggiore del best score
            best_score = v
            best_action = child  # l'azione migliore sarà il figlio corrente

    # alla fine del ciclo best-action conterrà l'azione che l'algoritmo ritiene essere la migliore da svolgere
    return best_action


def make_move_opponent(position, mask, col):
    # metodo di supporto utilizzato per calcolare solo la nuova posizione del tabellone dopo che il giocatore avversario
    # ha effettuato una mossa in una determinata colonna

    new_mask = mask | (mask + (1 << (col * 7)))  # Calcola la nuova maschera aggiungendo la mossa del giocatore
    # umano alla maschera esistente

    # Ritorna la posizione corrente del giocatore e la nuova maschera della board.
    return position, new_mask


def print_board(state):
    # metodo di supporto per stampare una rappresentazione visiva del tabellone di gioco

    ai_board, total_board = state.ai_position, state.game_position
    for row in range(5, -1, -1):
        print("")
        for column in range(0, 7):
            if ai_board & (1 << (7 * column + row)):
                print("1", end='')
            elif total_board & (1 << (7 * column + row)):
                print("2", end='')
            else:
                print("0", end='')
    print("")
