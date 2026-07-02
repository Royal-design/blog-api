class UserNotFoundError(Exception):
    def __init__(self, message: str = "User not found"):
        self.message = message
        super().__init__(message)


class EmailAlreadyExistsError(Exception):
    def __init__(self, message: str = "Email already exists"):
        self.message = message
        super().__init__(message)


class InvalidCredentialsError(Exception):
    def __init__(self, message: str = "Invalid email or password"):
        self.message = message
        super().__init__(message)


class InvalidTokenException(Exception):
    def __init__(self, message: str = "Invalid or expired token"):
        self.message = message
        super().__init__(message)