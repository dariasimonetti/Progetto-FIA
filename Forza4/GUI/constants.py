# definizione di alcune costanti usate in tutto il programma

BOARDWIDTH = 7  # larghezza griglia
BOARDHEIGHT = 6  # altezza della griglia

SPACESIZE = 50  # dimensione degli spazi espressa in pixel

FPS = 30  # fps necessari ad aggiornare la view
WINDOWWIDTH = 640  # larghezza in pizel della finestra
WINDOWHEIGHT = 480  # altezza in pixels

XMARGIN = int((WINDOWWIDTH - BOARDWIDTH * SPACESIZE) / 2)
YMARGIN = int((WINDOWHEIGHT - BOARDHEIGHT * SPACESIZE) / 2)

THISTLE = (196, 183, 203)  # colore thistle dello sfondo
WHITE = (255, 255, 255)  # colore testo

BGCOLOR = THISTLE
TEXTCOLOR = WHITE

RED = 'red'
BLACK = 'black'
EMPTY = None
HUMAN = 'human'
COMPUTER = 'computer'
