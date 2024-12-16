class BronirovshikException(Exception):
    detail = "Pizdec oshibka"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(BronirovshikException):
    detail = "Объект не найден"


class NoRoomsAvailableException(BronirovshikException):
    detail = "Нет свободных комнат"
