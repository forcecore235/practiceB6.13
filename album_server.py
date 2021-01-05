from bottle import run
from bottle import HTTPError
from bottle import route
from bottle import request

import album

@route("/albums/<artist>")
def albums(artist):
    """Поиск альбомов по исполнителю"""
    # Переменна со списком альбомов исполнителя artist
    albums_list = album.find_artist(artist)
    if not albums_list:
        message =  f"У исполнителя {artist} альбомов не найдено."
        result = HTTPError(404, message)
    else:
        albums_length = len(albums_list)
        albums_name = []
        for i in albums_list:
            albums_name.append(i.album)
        albums_str = ",\n".join(albums_name)
        result = f"Исполнитель {artist}\nАльбомов найдено {albums_length}:\n{albums_str}"
    return result

@route("/albums", method="POST")
def add_album():
    """Запись нового альбома"""
    # Записываем все нужные нам данные об альбоме в переменные
    artist = request.forms.get("artist")
    year = request.forms.get("year")
    genre = request.forms.get("genre")
    artist_album = request.forms.get("album")
    # Переменная с проверкой наличия альбома в бд
    find_artist = album.check_album_in_db(artist=artist, year=year, album=artist_album)
    # Проверка наличия нужных полей
    if artist == None or year == None or genre == None or artist_album == None:
        message = "Заполните все поля: artist, year, genre, album"
        return HTTPError(400, message)
    # Проверка наличия альбома в бд
    if find_artist:
        message = "Данный альбом уже есть в базе."
        return HTTPError(409, message)
    # Проверка пустой строки в поле artist
    if artist == "":
        message = "Имя исполнителя не может быть пустым."
        return HTTPError(400, message)
    # Проверка на наличие числа в поле year
    try:
        int(year)
    except ValueError as error:
        message = f"Ошибка {error}\nВ поле год выпуска альбома нужно указать число."
        return HTTPError(400, message)
    # Проверка корректности даты выхода альбома
    if int(year) < 1900:
        message = "Да в то время ещё балалайку не придумали. Укажите соответствующую дату."
        return HTTPError(400, message)
    # Проверка пустой строки в поле genre
    if genre == "":
        message = "Жанр не может быть пустой строкой."
        return HTTPError(400, message)
    # Проверка пустой строки в поле artist_album
    if artist_album == "":
        message = "Название альбома не может быть пустым."
        return HTTPError(400, message)
    # Если все проверки пройдены то записываем  альбом в бд и выводим сообщение об успешной записи
    album.new_album(artist, year, genre, artist_album)
    result = f"Альбом {artist_album} успешно добавлен."

    return result

if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)


# Для проверки установите httpie и введите в консоль:
# http -f POST http://localhost:8080/albums artist="Hyper" genre="EDM" album="Bully" year="2015"