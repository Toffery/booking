from fastapi.exceptions import HTTPException


class BronirovshikHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class HotelNotFoundHTTPException(BronirovshikHTTPException):
    status_code = 404
    detail = "Hotel not found"


class RoomNotFoundHTTPException(BronirovshikHTTPException):
    status_code = 404
    detail = "Room not found"


class HotelAlreadyExistHTTPException(BronirovshikHTTPException):
    status_code = 409
    detail = "Hotel already exist"
