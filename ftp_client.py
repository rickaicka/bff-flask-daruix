from ftplib import FTP
import threading
import time


class FTPClient:

    _ftp = None
    _lock = threading.Lock()
    _last_connect = 0

    FTP_HOST = "177.153.60.157"
    FTP_PORT = 2100
    FTP_USER = "renato"
    FTP_PASS = "634845"

    TIMEOUT_RECONNECT = 300  # reconecta a cada 5 minutos

    @classmethod
    def get_connection(cls):

        with cls._lock:

            now = time.time()

            if cls._ftp is None or (now - cls._last_connect) > cls.TIMEOUT_RECONNECT:
                cls._connect()

            return cls._ftp

    @classmethod
    def _connect(cls):

        if cls._ftp:
            try:
                cls._ftp.quit()
            except:
                pass

        ftp = FTP()

        ftp.connect(cls.FTP_HOST, cls.FTP_PORT)   # ← aqui define porta
        ftp.login(cls.FTP_USER, cls.FTP_PASS)

        cls._ftp = ftp
        cls._last_connect = time.time()