import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///albums.sqlite3"
Base = declarative_base()

class Album(Base):
    """Класс описывающий таблицу album"""
    __tablename__ = "album"

    id = sa.Column(sa.INTEGER, primary_key=True)
    year = sa.Column(sa.INTEGER)
    artist = sa.Column(sa.TEXT)
    genre = sa.Column(sa.TEXT)
    album = sa.Column(sa.TEXT)

def connect_db():
    """Создание сессии  с базой данных DB_PATH"""
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    Session = sessionmaker(engine)
    return Session()

def find_artist(artist):
    """Поиск альбомов указанного артиста"""
    session = connect_db()
    albums_list = session.query(Album).filter(Album.artist == artist).all()
    return albums_list

def check_album_in_db(artist, year, album):
    """Проверка на наличие альбома в базе данных"""
    session = connect_db()
    # Переменная с альбомом отфильтрованным по заданным критериям
    artist = session.query(Album).filter(Album.artist == artist, Album.year == year, Album.album == album).all()

    if artist:
        return True
    else:
        return False

def new_album(artist, year, genre, album):
    """Добавление нового альбома в базу данных"""
    session = connect_db()
    # Переменная со строкой содержащей альбом
    album_obj = Album(
        artist = artist,
        year = year,
        genre = genre,
        album = album
    )
    session.add(album_obj)
    session.commit()
    return "Альбом успешно добавлен в базу данных."