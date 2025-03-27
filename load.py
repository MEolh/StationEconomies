import tkinter as tk
import myNotebook as nb
from typing import Optional, Tuple
from config import config, appname # Importa appname
import l10n
import functools
import os
import logging

plugin_tl = functools.partial(l10n.translations.tl, context=__file__)

economy_label: Optional[tk.Label] = None
other_economies_label: Optional[tk.Label] = None
logger = None
plugin_name = None

def plugin_start3(plugin_dir: str) -> str:
    """
    Carica questo plugin in EDMarketConnector
    """
    global logger, plugin_name
    plugin_name = os.path.basename(os.path.dirname(__file__))
    logger = logging.getLogger(f'{appname}.{plugin_name}') # Usa appname direttamente dall'import
    if not logger.hasHandlers():
        level = logging.INFO
        logger.setLevel(level)
        logger_channel = logging.StreamHandler()
        logger_formatter = logging.Formatter(f'%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(lineno)d:%(funcName)s: %(message)s')
        logger_formatter.default_time_format = '%Y-%m-%d %H:%M:%S'
        logger_formatter.default_msec_format = '%s.%03d'
        logger_channel.setFormatter(logger_formatter)
        logger.addHandler(logger_channel)
        logger.info(f"Plugin StationEconomies caricato. Directory: {plugin_dir}")
        return "StationEconomies"

def plugin_app(parent: tk.Frame) -> nb.Frame:
    """
    Crea un frame contenitore con due widget TK disposti verticalmente
    per la finestra principale di EDMarketConnector
    """
    global economy_label, other_economies_label

    # Frame contenitore principale
    main_frame = nb.Frame(parent)
    main_frame.columnconfigure(0, weight=1) # Assicura che i widget si espandano orizzontalmente

    # Frame per l'economia principale
    frame_principale = nb.Frame(main_frame)
    label_titolo = tk.Label(frame_principale, text=plugin_tl("Economia principale:"))
    label_titolo.grid(row=0, column=0, sticky=tk.W, pady=(0, 2))
    economy_label = tk.Label(frame_principale, text=plugin_tl("Dati non disponibili"))
    economy_label.grid(row=1, column=0, sticky=tk.W, pady=(2, 0))
    frame_principale.grid(row=0, column=0, sticky=tk.NSEW, padx=5, pady=5) # Inserisci nel frame contenitore

    # Frame per le altre economie
    frame_altre = nb.Frame(main_frame)
    other_economies_title = tk.Label(frame_altre, text=plugin_tl("Altre economie:"))
    other_economies_title.grid(row=0, column=0, sticky=tk.W, pady=(0, 2))
    other_economies_label = tk.Label(frame_altre, text=plugin_tl("Dati non disponibili"))
    other_economies_label.grid(row=1, column=0, sticky=tk.W, pady=(2, 0))
    frame_altre.grid(row=1, column=0, sticky=tk.NSEW, padx=5, pady=5) # Inserisci nel frame contenitore

    return main_frame # Restituisci il frame contenitore principale

def journal_entry(cmdr: str, is_beta: bool, system: Optional[str], station: Optional[str], entry: dict, state: dict) -> Optional[str]:
    """
    Aggiorna i widget quando si verifica un evento 'Docked' nel journal.
    """
    if entry.get('event') == 'Docked':
        station_name = entry.get('StationName')
        main_economy_localised = entry.get('StationEconomy_Localised')
        station_economies = entry.get('StationEconomies', [])

        if station_name:
            if logger:
                logger.info(f"Arrivato alla stazione: {station_name}")

            if main_economy_localised and economy_label:
                # Trova la proporzione dell'economia principale
                main_economy_proportion = 0.0
                for eco in station_economies:
                    if eco.get('Name_Localised') == main_economy_localised:
                        main_economy_proportion = eco.get('Proportion', 0.0)
                        break
                # Aggiorna l'etichetta dell'economia principale con la proporzione
                economy_label.config(text=f"{main_economy_localised}: {main_economy_proportion:.2f}")
            elif economy_label:
                economy_label.config(text=plugin_tl("Sconosciuta"))

            if station_economies and other_economies_label:
                other_economies_info = []
                # Itera attraverso le economie, escludendo quella principale
                for eco in station_economies:
                    name_localised = eco.get('Name_Localised')
                    proportion = eco.get('Proportion')
                    if name_localised is not None and proportion is not None and name_localised != main_economy_localised:
                        # Formatta la stringa con nome localizzato e proporzione
                        other_economies_info.append(f"- {name_localised}: {proportion:.2f}")

                if other_economies_info:
                    # Unisce le informazioni delle altre economie in un'unica stringa
                    other_economies_label.config(text="\n".join([plugin_tl("Altre economie:")] + other_economies_info))
                else:
                    # Se non ci sono altre economie oltre alla principale
                    other_economies_label.config(text=plugin_tl("Nessuna altra economia"))
            elif other_economies_label:
                other_economies_label.config(text=plugin_tl("Dati non disponibili"))

        return None

    elif entry.get('event') == 'Undocked':
        # Quando si lascia la stazione, reimposta le label allo stato iniziale
        if economy_label:
            economy_label.config(text=plugin_tl("Dati non disponibili"))
        if other_economies_label:
            other_economies_label.config(text=plugin_tl("Dati non disponibili"))
        if logger:
            logger.info("Partito dalla stazione.")
        return None
