"""Giudizio di Claude sui candidati (una chiamata al giorno) e controllo "già uscito in Italia"."""
import json
import logging
import os
from typing import List

from pydantic import BaseModel

from . import config

log = logging.getLogger(__name__)

ISTRUZIONI = """Lavori per un giornalista italiano che scrive per un pubblico nazionale generalista e \
colto (lettori di un giornale online come Il Post). Cerca storie locali italiane da raccontare a tutto il \
paese prima degli altri media nazionali. Cerca STORIE, non notizie: vicende con personaggi, una trama, \
qualcosa di sorprendente o rivelatore dell'Italia, che reggano un articolo lungo o un racconto e che un \
lettore di un'altra regione non ha mai sentito.

Ricevi una lista di articoli di giornali locali italiani, già selezionati da segnali strutturali \
(lunghezza, permanenza in homepage, ripresa da altre testate, assenza dai media nazionali). \
Solo una piccola parte merita davvero: sii severo, l'asticella è alta.

Scala del voto:
- 9-10: storia straordinaria, originale, con personaggi e trama; la racconteresti subito.
- 7-8: storia originale e raccontabile, che dice qualcosa di non ovvio sull'Italia e interessa anche \
chi non vive lì.
- 5-6: notizia con qualche spunto, ma prevedibile o poco sviluppabile.
- 1-4: cronaca di routine (incidenti, furti, arresti senza storia dietro), sviluppi minori o passaggi \
procedurali di vicende in corso (udienze, rinvii, delibere, consigli comunali), polemiche politiche \
locali ordinarie, versioni locali di temi nazionali già noti, notizie che interessano solo chi vive lì, \
eventi e sagre, comunicati di enti e aziende, servizi di consumo, lanci d'agenzia ripresi. Un pezzo \
che parla di un luogo lontano dalla testata che lo pubblica è quasi sempre d'agenzia: abbassa il voto \
e dillo nella motivazione.

Per ciascun articolo dai:
- voto (1-10), secondo la scala.
- motivazione: una riga (massimo 20 parole) che spiega il voto.
- sinossi: due o tre frasi discorsive (45-55 parole) che raccontano di cosa parla la storia e perché \
colpisce, come le spiegheresti a un collega. Tono piano, senza enfasi. Usa solo le informazioni \
fornite: se il sommario manca, limitati a ciò che dice il titolo e non inventare dettagli.

Valuta ogni articolo in modo indipendente e restituisci una valutazione per ogni id ricevuto."""


def istruzioni():
    """Istruzioni di base più le preferenze espresse dal giornalista (data/preferenze.md)."""
    if config.PREFERENZE.exists():
        preferenze = config.PREFERENZE.read_text(encoding="utf-8").strip()
        if preferenze:
            return f"{ISTRUZIONI}\n\nPreferenze e giudizi espressi dal giornalista su selezioni passate, \
da tenere presenti:\n\n{preferenze}"
    return ISTRUZIONI


class Valutazione(BaseModel):
    id: int
    voto: int
    motivazione: str
    sinossi: str


class Esito(BaseModel):
    valutazioni: List[Valutazione]


SCHEMA = {
    "type": "object",
    "properties": {
        "valutazioni": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "voto": {"type": "integer"},
                    "motivazione": {"type": "string"},
                    "sinossi": {"type": "string"},
                },
                "required": ["id", "voto", "motivazione", "sinossi"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["valutazioni"],
    "additionalProperties": False,
}


def _scheda(i, a):
    t = a["t"]
    return {
        "id": i,
        "testata": f"{t['nome']} ({t['citta']}, {t['regione']}; {t['tipo']})",
        "titolo": a["titolo"],
        "sommario": (a.get("sommario") or "")[:500],
        "segnali": [s[2] for s in a["segnali"]],
        "altre_testate": [f"{b['t']['nome']}: {b['titolo']}" for b in a.get("ripresa", [])[:4]],
    }


def valuta(candidati):
    """Aggiunge a ogni candidato voto, motivazione e sinossi. Se la chiamata fallisce
    il monitor va avanti con i soli segnali strutturali."""
    if not candidati or not os.environ.get("ANTHROPIC_API_KEY"):
        log.warning("giudizio saltato (nessun candidato o chiave API assente)")
        return False
    import anthropic

    client = anthropic.Anthropic()
    schede = [_scheda(i, a) for i, a in enumerate(candidati)]
    try:
        with client.messages.stream(
            model=config.MODELLO,
            max_tokens=64000,
            system=istruzioni(),
            messages=[{"role": "user", "content": json.dumps(schede, ensure_ascii=False, indent=1)}],
            output_config={"effort": "medium", "format": {"type": "json_schema", "schema": SCHEMA}},
            extra_headers={"anthropic-beta": "server-side-fallback-2026-07-01"},
            extra_body={"fallbacks": "default"},
        ) as flusso:
            risposta = flusso.get_final_message()
    except anthropic.APIStatusError as e:
        log.error("giudizio: errore API %s: %s", e.status_code, e.message)
        return False
    except anthropic.APIConnectionError as e:
        log.error("giudizio: connessione non riuscita: %s", e)
        return False
    if risposta.stop_reason != "end_turn":
        log.error("giudizio: risposta non utilizzabile (stop_reason=%s)", risposta.stop_reason)
        return False
    testo = next((b.text for b in risposta.content if b.type == "text"), "")
    try:
        esito = Esito.model_validate_json(testo)
    except ValueError as e:
        log.error("giudizio: JSON non valido: %s", e)
        return False
    log.info("giudizio: %d valutazioni, token %s in / %s out", len(esito.valutazioni),
             risposta.usage.input_tokens, risposta.usage.output_tokens)
    for v in esito.valutazioni:
        if 0 <= v.id < len(candidati):
            candidati[v.id].update(voto=min(10, max(1, v.voto)), motivazione=v.motivazione, sinossi=v.sinossi)
    return True
