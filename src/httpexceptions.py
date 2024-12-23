from fastapi.exceptions import HTTPException


class BronirovshikHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class DateRangeHTTPException(BronirovshikHTTPException):
    status_code = 409
    detail = "Date range is invalid"


class HotelNotFoundHTTPException(BronirovshikHTTPException):
    status_code = 404
    detail = "Hotel not found"


class RoomNotFoundHTTPException(BronirovshikHTTPException):
    status_code = 404
    detail = "Room not found"


class HotelAlreadyExistHTTPException(BronirovshikHTTPException):
    status_code = 409
    detail = "Hotel already exist"


class RoomAlreadyExistHTTPException(BronirovshikHTTPException):
    status_code = 409
    detail = "Room already exist"


class UserAlreadyExistHTTPException(BronirovshikHTTPException):
    status_code = 409
    detail = "User already exist"


class UserNotFoundHTTPException(BronirovshikHTTPException):
    status_code = 404
    detail = "User not found"


class FacilityNotFoundHTTPException(BronirovshikHTTPException):
    status_code = 404
    detail = "Facility not found"


class TokenHasExpiredHTTPException(BronirovshikHTTPException):
    status_code = 401
    detail = "Token has been expired"


class InvalidTokenHTTPException(BronirovshikHTTPException):
    status_code = 401
    detail = "Invalid token"


class IncorrectPasswordHTTPException(BronirovshikHTTPException):
    status_code = 401
    detail = "Incorrect password"
