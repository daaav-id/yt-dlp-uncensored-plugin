# A yt-dlp plugin to handle some censored sites

## Supported sites:

- SxyPrn dot com (aka YourPorn)
- DoodStream
- FileMoon
- VidGuard
- Voe

## Installation:

Choose one of the following options:

* **User Plugins**
  * `${XDG_CONFIG_HOME}/yt-dlp/plugins/<package name>/yt_dlp_plugins/` (recommended on Linux/macOS)
  * `${XDG_CONFIG_HOME}/yt-dlp-plugins/<package name>/yt_dlp_plugins/`
  * `${APPDATA}/yt-dlp/plugins/<package name>/yt_dlp_plugins/` (recommended on Windows)
  * `${APPDATA}/yt-dlp-plugins/<package name>/yt_dlp_plugins/`
  * `~/.yt-dlp/plugins/<package name>/yt_dlp_plugins/`
  * `~/yt-dlp-plugins/<package name>/yt_dlp_plugins/`
* **System Plugins**
  * `/etc/yt-dlp/plugins/<package name>/yt_dlp_plugins/`
  * `/etc/yt-dlp-plugins/<package name>/yt_dlp_plugins/`
* **Executable location**: 
  * Binary: where `<root-dir>/yt-dlp.exe`, `<root-dir>/yt-dlp-plugins/<package name>/yt_dlp_plugins/`
  * Source: where `<root-dir>/yt_dlp/__main__.py`, `<root-dir>/yt-dlp-plugins/<package name>/yt_dlp_plugins/`\
 
In that directory clone this repository (or download the latest snapshot) in a new folder.

For example, this would work: `/etc/yt-dlp/plugins/yt-dlp-uncensored-plugin/`.
One working file will be: /etc/yt-dlp-plugins/yt-dlp-uncensored-plugin/yt_dlp_plugins/extractor/yourporn.py
