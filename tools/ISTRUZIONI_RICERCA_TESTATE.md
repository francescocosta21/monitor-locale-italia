# Istruzioni per la ricerca delle testate locali italiane (per macroarea)

Stiamo costruendo un monitor di storie locali italiane per un giornalista che vuole trovare notizie locali da raccontare a un pubblico nazionale prima degli altri media nazionali. Il monitor scarica ogni 2 ore homepage e feed RSS di ~350 testate locali. Il tuo compito: compilare la lista delle testate per UNA macroarea.

Perimetro: tutte le notizie locali in senso ampio (fatti di cronaca, politica locale, economia del territorio, storie di persone, cultura).

## Tipi di testata (mescolali)
- `quotidiano_locale`: quotidiani locali e regionali (Il Gazzettino, L'Eco di Bergamo, Il Resto del Carlino, La Nuova Sardegna, Il Tirreno, Giornale di Brescia, L'Unione Sarda, Il Secolo XIX, Gazzetta del Sud, La Sicilia…). Includili tutti quelli rilevanti.
- `edizione_locale`: edizioni locali dei nazionali (Corriere Milano, Corriere del Veneto, Corriere Fiorentino, Corriere di Bologna, Corriere del Mezzogiorno, Corriere Torino, Repubblica Napoli/Palermo/Bologna/Firenze/Genova/Torino/Bari/Roma/Milano, La Stampa Torino e province, Il Messaggero Roma…). Serve l'URL della sezione locale.
- `sito_locale`: siti di notizie locali solo online. Rete Citynews (MilanoToday, RomaToday, NapoliToday… ne esistono circa 50: includi quelle dei capoluoghi più grandi e almeno una per regione dove esiste), siti provinciali e iperlocali indipendenti (es. Varese News, Bergamonews, Estense.com, Ravenna&Dintorni).
- `tv_locale`: redazioni regionali TGR Rai (rainews.it/tgr/<regione>) e le principali emittenti regionali con sito di notizie (Telelombardia, Antenna 3, TeleNorba, Videolina, Canale 10…).
- `settimanale`: settimanali locali e diocesani con notizie, solo se aggiornati spesso online.

ESCLUSI: testate nazionali (Corriere, Repubblica, Stampa, Fanpage, Il Post, Open, Il Fatto, TgCom24, Sky TG24, ANSA nazionale…: sono il termine di confronto "nazionale"), aggregatori, siti di comunicati stampa, blog personali.

## Criteri
- Copri TUTTE le regioni della macroarea e il maggior numero possibile di province (almeno una testata per provincia dove esiste qualcosa di serio; di più per le grandi città).
- Preferisci testate che pubblicano ogni giorno e fanno giornalismo originale.
- Verifica che la testata sia ANCORA ATTIVA nel 2026 (diverse testate hanno chiuso, cambiato proprietà o dominio).
- Annota sempre il gruppo editoriale: serve per non contare come "ripresa" un pezzo ripubblicato nello stesso gruppo. Valori tipici: GEDI, RCS, Caltagirone, Monrifs (QN), SAE, NEM (Nord Est Multimedia), Athesis, Citynews, Rai, Sesaab, Editoriale Bresciana, indipendente, altro (specifica).

## Verifica tecnica (obbligatoria)
Per ogni testata esegui lo script di verifica (puoi passare molti URL in una volta):

```
cd <cartella del progetto> && .venv/bin/python tools/verifica_testata.py https://www.a.it https://www.b.it 2>/dev/null
```

Restituisce una riga JSON per URL con status HTTP, url finale e feed RSS trovati (con numero di elementi). Se non trova un feed, cercalo tu (WebFetch sulla homepage, WebSearch "<testata> feed rss", percorsi come /rss, /feed/, /rss.xml, /rss/home). Status 403/429/timeout non sono motivi di esclusione (blocchi anti-bot): includi con nota. Una testata senza feed va tenuta se importante, con nota "senza feed" (il monitor userà homepage o Google News).

Lavora solo dentro la cartella del progetto indicata; se usi file temporanei mettili in una sottocartella con il nome della tua macroarea, per non scontrarti con gli altri agenti che lavorano in parallelo.

## Output
Scrivi un CSV UTF-8 con intestazione esattamente:

```
nome,url_homepage,feed_rss,stato,citta,tipo,gruppo,lingua,paywall,homepage_status,note
```

- `stato`: sigla della PROVINCIA (MI, RM, NA, BZ…); per testate regionali usa la provincia del capoluogo di regione e scrivi "regionale" nelle note
- `citta`: città della redazione principale
- `tipo`: uno dei valori sopra
- `lingua`: it (oppure de per l'Alto Adige, sl, fr se ce ne sono)
- `paywall`: si / no / misto / ?
- `homepage_status`: lo status HTTP restituito dallo script
- `note`: breve (es. "regionale Toscana", "senza feed", "forte su giudiziaria")

Metti tra virgolette i campi che contengono virgole. Scrivi il file con lo strumento Write nel percorso indicato nel prompt. Alla fine rispondi con: numero di testate, distribuzione per regione e per tipo, province scoperte, testate escluse perché chiuse (breve).
