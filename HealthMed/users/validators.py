from .defs import DIALING_CODES
from rest_framework.serializers import ValidationError, Serializer


def validate_phone(self: Serializer, phone) -> str:
    phone = "".join(filter(lambda x: x in "+1234567890", phone))
    for country_code, values in DIALING_CODES.items():
        start_phone, len_phone = values
        if phone.startswith(start_phone) and phone.__len__() == len_phone:
            return phone

    raise ValidationError({"phone", "Incorrect phone number format!"})


def string_contain_only_digits(string) -> bool:
    filter_string = "".join(filter(lambda x: x.isdigit(), string))
    return True if filter_string == string else False


def validate_passport(self: Serializer, string) -> str:
    if string_contain_only_digits(string=string): return string
    else: raise ValidationError({"passport": "Incorrect passport format!"})


def validate_med_policy(self: Serializer, string) -> str:
    if string_contain_only_digits(string=string): return string
    else: raise ValidationError({"med_policy": "Incorrect med policy format!"})

