from collections import OrderedDict
from passlib.hash import sha256_crypt
from django.conf import settings


# Классы ошибок

class DataEntryError(Exception):
    """ Ошибка обработки данных, введённых пользователем в форме """
    @classmethod
    def as_str(cls) -> str: return "DATA_ENTRY_ERROR"

class NotValidData(Exception):
    """ Ошибка не валидных введённых данных """
    @classmethod
    def as_str(cls) -> str: return "NOT_VALID_DATA"
    
class ScheduleNotExists(Exception):
    """ Ошибка отсутсвия записи расписания в базе """
    @classmethod
    def as_str(cls) -> str: return "SCHEDULE_NOT_EXISTS"

class AlreadyExists(Exception):
    """ Ошибка существования записи """
    @classmethod
    def as_str(cls) -> str: return "ALREADY_EXISTS"

class PasswordDoNotMatch(Exception):
    """ Ошибка несовпадения паролей в форме """
    @classmethod
    def as_str(cls) -> str: return "DATA_ENTRY_ERROR"

class TimeOverlapping(Exception):
    """ Ошибка пересечения времени записи с существующей в базе """
    @classmethod
    def as_str(cls) -> str: return "TIME_OVERLAPPING"

class PasswordIncorrect(Exception):
    """ Ошибка ввода неправильного пароля в форме входа """
    @classmethod
    def as_str(cls) -> str: return "PASSWORD_INCORRECT"

class UserAlreadyExists(Exception):
    """ Ошибка существования пользователя """
    @classmethod
    def as_str(cls) -> str: return "USER_ALREADY_EXISTS"

class UserNotExists(Exception):
    """ Ошибка не существования пользователя """
    @classmethod
    def as_str(cls) -> str: return "USER_NOT_EXISTS"


# Константы

DIALING_CODES: dict[str, tuple[str, int]] = {
    "RU": ("+7", 12),
    "KZ": ("+7", 12),
    "BY": ("+375", 13)
}

RU_TRANSCRIPTS_FIELDS: dict[str, tuple[str, str]] = {
    "phone": ("номер телефона", "номером телефона"),
    "email": ("почта", "почтой"),
    "med_policy": ("медицинский полис", "медицинским полисом"),
    "passport": ("паспорт", "паспортом"),
}


# Вспомогательные функции

def create_password_hash(password):
    return sha256_crypt.using(salt=settings.PASSWORD_SALT, rounds=10**4).hash(password)


def encrypt_pwd_dict(data: OrderedDict):
    data["password"] = create_password_hash(data.get("password", ""))
    data["password_repeat"] = create_password_hash(data.get("password_repeat", ""))
    return data


def get_integrity_error_field(string_error: str) -> str:
    return string_error.split("Key (")[-1].split(")")[0] if "Key (" in string_error else ""


def check_password(password, hash):
    return True if create_password_hash(password=password) == hash else False

