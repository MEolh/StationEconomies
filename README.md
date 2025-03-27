# StationEconomies

**Displays the type and proportion of economies of a docked station within EDMarketConnector.**

## Installation

1.  Download the **latest release** of the plugin from the [Releases](link_to_your_releases_page) page.
2.  Extract the contents of the downloaded `.zip` file into the EDMarketConnector plugins folder. You can locate this folder by navigating to 'File' > 'Settings' in the EDMC window and clicking the "Open" button on the "Plugins" tab. The default locations are:
    *   **Windows:** `%LOCALAPPDATA%\EDMarketConnector\plugins` (typically `C:\Users\<YourUsername>\AppData\Local\EDMarketConnector\plugins`)
    *   **Mac:** `~/Library/Application Support/EDMarketConnector/plugins` (in Finder, press <kbd>⌥</kbd> (Option) and choose Go → Library to open the `~/Library` folder)
    *   **Linux:** `$XDG_DATA_HOME/EDMarketConnector/plugins` or `~/.local/share/EDMarketConnector/plugins` if `$XDG_DATA_HOME` is not set.
3.  **Restart EDMarketConnector** for the new plugin to be loaded.

## Functionality

The StationEconomies plugin adds two labels to the main EDMarketConnector window. When docked at a starport, these labels will display:

*   **Main Economy:** The station's primary economy type and its proportion.
*   **Other Economies:** A list of all other economies present at the station along with their respective proportions.

If no station economy information is available in the game journal's 'Docked' event, the labels will display "Data not available".

## Compatibility

This plugin is **only compatible with EDMarketConnector version 4.0.0 and later**, which uses **Python 3.9+** [1]. Older versions of EDMC based on Python 2.7 are not supported [2, 3].

## Localization

This plugin includes translations for the following languages:

*   **English** (`en`)
*   **Italian** (`it`)
*   **German** (`de`)
*   **Spanish** (`es`)
*   **French** (`fr`)

These translations will be automatically used by EDMarketConnector if your EDMC language setting matches. If you would like to contribute translations for other languages, please feel free to submit a pull request. You can find information on how to create translation files in the [EDMC plugin documentation](https://github.com/EDCD/EDMarketConnector/blob/main/PLUGINS.md#localisation) [4].

## Acknowledgement

*   [EDMarketConnector (EDMC)](https://github.com/EDCD/EDMarketConnector) for providing the core application and comprehensive plugin development documentation [3, 5-7].

## Contact

For bug reports or feature requests, please **open a new Issue on this GitHub repository**. This is the preferred method for tracking plugin development and issues.

For other inquiries, you can contact me via email: eolh.michele@gmail.com
