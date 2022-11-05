

class FormatError:
    NOT_DICTIONARY = "Incorrect data format. Should be key-value dictionary."


class RegistrationError:
    EMAIL_IS_BUSY = "User with this email already exists"
    CREDENTIALS_VERIFICATION_FAILED = "Oops, something went wrong. Failed to verify that credentials are free."
    CREATE_NEW_USER_FAILED = "Oops, something went wrong. Failed to create a new user. Please try later."


class LoginError:
    INVALID_EMAIL = "Invalid email"
    INVALID_PASSWORD = "Invalid password"


class EnvVariable:
    DB_HOST = "DB_HOST"
    DB_NAME = "DB_NAME"
    DB_USER = "DB_USER"
    DB_PASSWORD = "DB_PASSWORD"
    DB_PORT = "DB_PORT"
