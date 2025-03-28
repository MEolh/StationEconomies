import tkinter as tk
import myNotebook as nb
from typing import Optional, Tuple
from config import config, appname
import l10n
import functools
import os
import logging

plugin_tl = functools.partial(l10n.translations.tl, context=__file__)
economy_label: Optional[tk.Label] = None
other_economies_label: Optional[tk.Label] = None
logger = None
plugin_name = None
main_frame: Optional[nb.Frame] = None # Riferimento al frame principale
label_titolo: Optional[tk.Label] = None # Nuovo riferimento per "Main economy:"
other_economies_title: Optional[tk.Label] = None # Nuovo riferimento per "Other economies:"

def plugin_start3(plugin_dir: str) -> str:
    global logger, plugin_name
    plugin_name = os.path.basename(os.path.dirname(__file__))
    logger = logging.getLogger(f'{appname}.{plugin_name}')
    if not logger.hasHandlers():
        level = logging.INFO
        logger.setLevel(level)
        logger_channel = logging.StreamHandler()
        logger_formatter = logging.Formatter(f'%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(lineno)d:%(funcName)s: %(message)s')
        logger_formatter.default_time_format = '%Y-%m-%d %H:%M:%S'
        logger_formatter.default_msec_format = '%s.%03d'
        logger_channel.setFormatter(logger_formatter)
        logger.addHandler(logger_channel)
    logger.info(f"Plugin StationEconomies loaded. The plugin folder is: {plugin_dir}")
    return "StationEconomies"

def plugin_app(parent: tk.Frame) -> nb.Frame:
    global economy_label, other_economies_label, main_frame, label_titolo, other_economies_title
    main_frame = nb.Frame(parent)
    main_frame.columnconfigure(0, weight=1)
    frame_principale = nb.Frame(main_frame)
    label_titolo = tk.Label(frame_principale, text=plugin_tl("Main economy:")) # Assegna il label alla variabile globale
    label_titolo.grid(row=0, column=0, sticky=tk.W, pady=(0, 2))
    economy_label = tk.Label(frame_principale, text=plugin_tl("Data not available"))
    economy_label.grid(row=1, column=0, sticky=tk.W, pady=(2, 0))
    frame_principale.grid(row=0, column=0, sticky=tk.NSEW, padx=5, pady=5)
    frame_altre = nb.Frame(main_frame)
    other_economies_title = tk.Label(frame_altre, text=plugin_tl("Other economies:")) # Assegna il label alla variabile globale
    other_economies_title.grid(row=0, column=0, sticky=tk.W, pady=(0, 2))
    other_economies_label = tk.Label(frame_altre, text=plugin_tl("Data not available"))
    other_economies_label.grid(row=1, column=0, sticky=tk.W, pady=(2, 0))
    frame_altre.grid(row=1, column=0, sticky=tk.NSEW, padx=5, pady=5)
    return main_frame

def journal_entry(cmdr: str, is_beta: bool, system: Optional[str], station: Optional[str], entry: dict, state: dict) -> Optional[str]:
    if entry.get('event') == 'Docked':
        station_name = entry.get('StationName')
        main_economy_localised = entry.get('StationEconomy_Localised')
        station_economies = entry.get('StationEconomies', [])
        if station_name:
            if logger:
                logger.info(f"Docked at: {station_name}")
            if main_economy_localised and economy_label:
                main_economy_proportion = 0.0
                for eco in station_economies:
                    if eco.get('Name_Localised') == main_economy_localised:
                        main_economy_proportion = eco.get('Proportion', 0.0)
                        break
                economy_label.config(text=f"{main_economy_localised}: {main_economy_proportion:.2f}")
            elif economy_label:
                economy_label.config(text=plugin_tl("Unknown"))
            if station_economies and other_economies_label:
                other_economies_info = []
                for eco in station_economies:
                    name_localised = eco.get('Name_Localised')
                    proportion = eco.get('Proportion')
                    if name_localised is not None and proportion is not None and name_localised != main_economy_localised:
                        other_economies_info.append(f"- {name_localised}: {proportion:.2f}")
                if other_economies_info:
                    other_economies_label.config(text="\n".join([plugin_tl("Other economies:")] + other_economies_info))
                else:
                    other_economies_label.config(text=plugin_tl("No other economies"))
            elif other_economies_label:
                other_economies_label.config(text=plugin_tl("Data not available"))
        return None
    elif entry.get('event') == 'Undocked':
        if economy_label:
            economy_label.config(text=plugin_tl("Data not available"))
        if other_economies_label:
            other_economies_label.config(text=plugin_tl("Data not available"))
        if logger:
            logger.info("Undocked.")
        return None

def update_labels():
    """Aggiorna il testo di tutti i label localizzati."""
    global economy_label, other_economies_label, label_titolo, other_economies_title
    if label_titolo:
        label_titolo.config(text=plugin_tl("Main economy:"))
    if other_economies_title:
        other_economies_title.config(text=plugin_tl("Other economies:"))
    if economy_label:
        current_text = economy_label.cget("text")
        if ":" in current_text:
            parts = current_text.split(":")
            proportion = parts[-1].strip()
            main_economy_key = [key for key, value in l10n.translations.translations[l10n.translations.current_lang]['messages'].items() if value == parts.strip() and '__file__' in key]
            economy_label.config(text=f"{plugin_tl(main_economy_key) if main_economy_key else plugin_tl('Unknown')}: {proportion}")
        else:
            economy_label.config(text=plugin_tl("Data not available"))
    if other_economies_label:
        current_text = other_economies_label.cget("text")
        if "\n" in current_text and current_text.startswith(plugin_tl("Other economies:")):
            lines = current_text.split("\n")
            updated_lines = [plugin_tl("Other economies:")]
            for line in lines[1:]:
                if "- " in line:
                    parts = line.split(":")
                    proportion = parts[-1].strip()
                    other_economy_key = [key for key, value in l10n.translations.translations[l10n.translations.current_lang]['messages'].items() if value == parts.replace("- ","").strip() and '__file__' in key]
                    updated_lines.append(f"- {plugin_tl(other_economy_key) if other_economy_key else parts.replace('- ','')}: {proportion}")
            other_economies_label.config(text="\n".join(updated_lines))
        else:
            other_economies_label.config(text=plugin_tl("Data not available") if current_text == plugin_tl("Data not available") else plugin_tl("No other economies"))

def prefs_changed(cmdr: str, is_beta: bool) -> None:
    """Aggiorna le label del plugin quando cambiano le preferenze (inclusa la lingua)."""
    if logger:
        logger.info("Language changed, updating plugin labels.")
    update_labels()

def plugin_stop() -> None:
    if logger:
        logger.info(f"Plugin {plugin_name} is closing.")
