from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from .models.base import Base as SqlAlchemyBase

__factory = None

def global_init(user, password, host, port, dbname, delete_db=False):
    global __factory

    if __factory:
        return

    # Используем pymysql вместо aiomysql, так как он синхронный
    conn_str = f'mysql+pymysql://{user}:{password}@{host}:{port}/{dbname}'
    print(f"Подключение к базе данных по адресу {conn_str}")

    # Создаем синхронный движок
    engine = create_engine(conn_str, pool_pre_ping=True)
    
    from . import __all_models
    # Создание всех таблиц синхронно
    if delete_db:
        SqlAlchemyBase.metadata.drop_all(engine)
    SqlAlchemyBase.metadata.create_all(engine)

    # Создаем фабрику синхронных сессий
    __factory = sessionmaker(bind=engine)

def create_session():
    global __factory
    return __factory()