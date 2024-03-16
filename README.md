# Forza 4 (meno uno)
## Scopo del progetto:
Il Progetto ”Forza 4 (meno uno)” nasce con l’obiettivo di osservare un’inteligenza artificiale quando si scontra in un gioco competitivo con un avversario umano e per comprendere i retroscena e i meccanismi da cui è caratterizzata. Per farlo abbiamo deciso di osservare gli algoritmi di ricerca con avversari, in particolare l'algoritmo Alpha Beta.
L’algoritmo Alpha-Beta è una tecnica di potatura utilizzata per migliorare l’efficienza dell’algoritmo Minimax. Si basa sulla potatura di rami dell’albero di ricerca che sono sicuramente meno promettenti rispetto ad altri, senza compromettere la correttezza dell’algoritmo. Si è scelto di utilizzare direttamente questa tecnica poiché, a seguito di alcune ricerche, abbiamo constatato che l’algoritmo Minimax puro avrebbe richiesto tempo di calcolo esponenziale per analizzare l’intero albero di gioco.
## Struttura Repository:
Nella cartella Forza 4 sono presenti:
- file main: che consente all'applicazione di partire
- directory GUI: in cui sono presenti i file che permettono la rappresentazione tramite interfaccia grafica del tabellone di gioco, le animazioni e le interazioni con il tabellone da parte del giocatore umano
- directory Game: in cui sono presenti i file che contengono la logica di gioco e gli algoritmi di ricerca utilizzati dall'AI per la decisione delle mosse.
- directory docs: contiene la documentazione dettagliata del progetto
## Guida all'Installazione:
Clona la repository, inserendo il seguente link: https://github.com/dariasimonetti/Progetto-FIA , e installa le dipendenze del progetto
## Librerie utili:
Per far funzionare il gioco bisogna aver installato:
- Python 3.12
- Libreria pygame (da terminale di PyCharm: pip install pygame)
