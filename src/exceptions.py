class BronirovshikException(Exception):
    detail = "Pizdec oshibka"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(BronirovshikException):
    detail = "Объект не найден"


class NoRoomsAvailableException(BronirovshikException):
    detail = "Нет свободных комнат"


class UserNotFoundException(BronirovshikException):
    detail = "Пользователь не найден"


class WrongPasswordException(BronirovshikException):
    detail = "Неверный пароль"


class UserAlreadyExistException(BronirovshikException):
    detail = "Пользователь с таким никнеймом или почтой уже существует"


class DateRangeException(BronirovshikException):
    detail = "Неверный диапазон дат"


class RoomNotFoundException(BronirovshikException):
    detail = "Такого номера не существует"


class HotelNotFoundException(BronirovshikException):
    detail = "Такого отеля не существует"
