import sys
import selectors

# macOS asyncio/kevent hata yaması (Sunucu başlamadan önce uygulanmalı)
if sys.platform == "darwin":
    if hasattr(selectors, 'KqueueSelector'):
        selectors.DefaultSelector = selectors.SelectSelector

from streamlit.web import cli as stcli

if __name__ == "__main__":
    # Streamlit sunucusunu doğrudan bu yama ile başlatır
    sys.argv = ["streamlit", "run", "app.py"]
    sys.exit(stcli.main())
