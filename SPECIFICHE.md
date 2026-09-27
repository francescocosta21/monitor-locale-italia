# Monitor storie locali italiane — specifiche

Creato il 2026-09-27 sullo stesso motore del monitor americano (`../monitor-locale`), con queste differenze.

## Scopo
Trovare storie locali italiane da raccontare a un pubblico nazionale prima degli altri media nazionali. Perimetro: tutte le notizie locali in senso ampio (cronaca, politica locale, economia del territorio, storie di persone, cultura).

## Output
- Email separata ogni mattina (5:10-6:00 ora italiana) all’indirizzo impostato nei segreti del repository, oggetto "Storie locali Italia · <data>".
- 10 storie: prima quelle con voto da 7 in su, poi le migliori con 6 e 5; mai sotto 5.
- Sinossi discorsiva di 2-3 frasi, segnali, voto con motivazione, testate che ne scrivono.
- Etichetta "Già sui nazionali?" (con link) se un pezzo simile è uscito sui nazionali: solo etichetta, nessuna penalità.
- Nessun link inviato due volte; sviluppi di storie già segnalate ammessi ed etichettati.

## Testate (~350)
Quotidiani locali, edizioni locali dei nazionali, siti locali online (Citynews e indipendenti), TGR e TV regionali. Lista in `data/testate.xlsx`. Esclusi i nazionali, che fanno da termine di confronto.

## Segnali
Come negli USA, meno Reddit: lunghezza anomala, permanenza in homepage (giro ogni 2 ore), ripresa da testate di gruppi editoriali diversi, divergenza dal nazionale. Almeno 2 su 4. "Fuori regione" al posto di "fuori stato"; ripresa in 3 o più altre regioni = storia nazionale.

Nazionali di confronto: Corriere, Repubblica, La Stampa, ANSA, Sky TG24, TgCom24, Open, Il Fatto, Rai News, Il Messaggero; via Google News Il Post, Fanpage, Il Giornale, Avvenire, Il Sole 24 Ore, Today. Le edizioni locali (es. milano.corriere.it, rainews.it/tgr) sono escluse dal confronto perché sono fonti.

Agenzie escluse: ANSA, Adnkronos, AGI, LaPresse, Dire, Italpress, Askanews, Nova (firma o intestazione del lancio).

Esclusioni per sezione: necrologi, meteo, oroscopo, contenuti sponsorizzati e pubbliredazionali.

## Social
Gruppi Facebook non accessibili; Reddit richiede un'app. Possibile aggiunta futura: canali Telegram pubblici locali (anteprima web t.me/s/…).

## Infrastruttura
Repository pubblico (minuti GitHub illimitati). Segreti: ANTHROPIC_API_KEY, GMAIL_APP_PASSWORD, GMAIL_UTENTE, EMAIL_DESTINATARIO. Giudizio: Claude Opus 5, 100 candidati al giorno. Preferenze del giornalista in `data/preferenze.md`.
