"""Costanti e percorsi del monitor. Le soglie dei segnali stanno qui per poterle ritoccare."""
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DATI = BASE / "data"
TESTATE_CSV = DATI / "testate.csv"
INVIATI_CSV = DATI / "inviati.csv"
PREFERENZE = DATI / "preferenze.md"   # giudizi del giornalista, letti da Claude ogni mattina
ARCHIVIO = DATI / "archivio"
STATO = BASE / "stato"          # cartella non versionata: il database vive nella cache di GitHub Actions
DB = STATO / "monitor.db"

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 14_6) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")
TIMEOUT = 12
WORKERS = 48
MAX_PAGINE_ARTICOLO_PER_TESTATA = 25   # pagine di articoli nuovi scaricate per testata a ogni giro

# Finestra e selezione
FINESTRA_ORE = 48
STORIE_EMAIL = 10
CANDIDATI_GIUDIZIO = 100
PESO_STRUTTURALE = 0.6
PESO_GIUDIZIO = 0.4
SEGNALI_MINIMI = 2
VOTO_PREFERITO = 7              # prima le storie da qui in su...
VOTO_MINIMO = 5                 # ...poi, per arrivare a STORIE_EMAIL, i voti immediatamente inferiori; mai sotto questo

# Soglie dei segnali
LUNGHEZZA_RAPPORTO = 1.8        # parole / mediana della testata
LUNGHEZZA_CAMPIONE_MINIMO = 10
HOMEPAGE_ORE_MINIME = 12
HOMEPAGE_TOP = 10               # posizione considerata "in alto"
INTERVALLO_ORE = 2
SIMILARITA_STESSA_STORIA = 0.40
SIMILARITA_NAZIONALE = 0.25
SIMILARITA_DOPPIONE_EMAIL = 0.28   # più larga: nell'email due pezzi sulla stessa vicenda non devono comparire entrambi
SIMILARITA_COPIA = 0.85            # stesso articolo ripubblicato: non conta come ripresa indipendente
LUNGHEZZA_RAPPORTO_MASSIMO = 10    # oltre: elenchi e raccolte automatiche, non pezzi lunghi
STATI_PER_NAZIONALE = 3            # ripresa in almeno 3 altre regioni: la storia è nazionale
RIPRESA_ALTRE_TESTATE = 2       # testate di gruppi diversi oltre a quella dell'articolo
REDDIT_PUNTEGGIO = 80           # upvote + 2 × commenti

# Esclusioni per sezione (necrologi, meteo, sponsorizzati; oroscopo come il meteo)
ESCLUSIONI_URL = (r"/(necrolog\w*|annunci-funebri|funebri|lutti|meteo|previsioni-meteo|oroscop\w*|"
                  r"sponsor\w*|contenuti-sponsorizzati|contenuto-sponsorizzato|pubbliredazional\w*|"
                  r"informazione-pubblicitaria|branded(-content)?|partner-content|promo|publireportage)(/|$|-)")
ESCLUSIONI_TITOLO = r"^(necrologi|meteo|previsioni meteo|oroscopo|contenuto sponsorizzato|informazione pubblicitaria)\b"

# Fonti nazionali per il segnale "divergenza dal nazionale"
NAZIONALI_FEED = {
    "Corriere della Sera": "https://xml2.corriereobjects.it/rss/homepage.xml",
    "Corriere cronache": "https://xml2.corriereobjects.it/rss/cronache.xml",
    "Repubblica": "https://www.repubblica.it/rss/homepage/rss2.0.xml",
    "Repubblica cronaca": "https://www.repubblica.it/rss/cronaca/rss2.0.xml",
    "La Stampa": "https://www.lastampa.it/rss/copertina.xml",
    "ANSA": "https://www.ansa.it/sito/notizie/topnews/topnews_rss.xml",
    "ANSA cronaca": "https://www.ansa.it/sito/notizie/cronaca/cronaca_rss.xml",
    "Sky TG24": "https://tg24.sky.it/rss/tg24.xml",
    "TgCom24": "https://www.tgcom24.mediaset.it/rss/homepage.xml",
    "Open": "https://www.open.online/feed/",
    "Il Fatto Quotidiano": "https://www.ilfattoquotidiano.it/feed/",
    "Rai News": "https://www.rainews.it/rss/ultimora",
    "Il Messaggero": "https://www.ilmessaggero.it/rss/home.xml",
}
NAZIONALI_GOOGLE_NEWS = ["ilpost.it", "fanpage.it", "ilgiornale.it", "avvenire.it", "ilsole24ore.com",
                         "today.it", "tg24.sky.it"]
LINGUA_NOTIZIE = "it"

# Province → regioni (per "fuori regione" e per riconoscere le storie ormai nazionali)
REGIONI = {
    "Piemonte": "TO VC NO CN AT AL BI VB", "Valle d'Aosta": "AO",
    "Lombardia": "VA CO SO MI BG BS PV CR MN LC LO MB", "Liguria": "IM SV GE SP",
    "Trentino-Alto Adige": "TN BZ", "Veneto": "VR VI BL TV VE PD RO",
    "Friuli-Venezia Giulia": "UD GO TS PN", "Emilia-Romagna": "PC PR RE MO BO FE RA FC RN",
    "Toscana": "MS LU PT FI LI PI AR SI GR PO", "Umbria": "PG TR", "Marche": "PU AN MC AP FM",
    "Lazio": "VT RI RM LT FR", "Abruzzo": "AQ TE PE CH", "Molise": "CB IS",
    "Campania": "CE BN NA AV SA", "Puglia": "FG BA TA BR LE BT", "Basilicata": "PZ MT",
    "Calabria": "CS CZ RC KR VV", "Sicilia": "TP PA ME AG CL EN CT RG SR",
    "Sardegna": "SS NU CA OR SU",
}
PROVINCIA_REGIONE = {p: r for r, sigle in REGIONI.items() for p in sigle.split()}

# Giudizio
MODELLO = "claude-opus-5"
