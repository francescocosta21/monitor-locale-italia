"""Parole vuote italiane per il confronto dei testi (scikit-learn ha solo l'inglese)."""
PAROLE_VUOTE = sorted(set("""
a ad al alla alle allo agli ai all anche ancora avere aveva avevano c che chi ci coi col come con contro cosa così cui
da dal dalla dalle dallo dagli dai dall degli dei del della delle dello dell di dopo dove due e è ed era erano essere
fa fare fra gli già ha hanno ho i il in invece io l la le lei lo loro lui ma mai me mentre mi molto ne nei nel nella
nelle nello nell negli no noi non nostro o ogni oggi ora per perché più poi può proprio quale quali quando quanto
quella quelle quello quelli questa queste questo questi qui se sarà sei senza si sia siamo sono sopra sotto sta stato
stata stati state su sua sue sui sul sulla sulle sullo sull suo suoi tra tre tutti tutto tutta tutte uno una un uno
vi voi dell' all' dall' nell' sull' l' un' d' c' anni anno giorno giorni ieri domani ore ecco secondo dice detto
città comune via
""".split()))
