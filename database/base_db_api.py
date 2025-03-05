from sqlalchemy.orm import Session

from .db_session import create_session

class BaseDBApi:
    _sess: Session

    def __init__(self):
        self._sess = create_session()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        if self._sess:
            self._sess.close()