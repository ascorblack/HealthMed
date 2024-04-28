from django.http import HttpRequest


def get_user_type(request: HttpRequest):
    """
    
      Функция, определяющая тип посетителя
    
    """
    user = request.user
    auth_status = user.is_authenticated
    
    if not auth_status:
        return "visitor"
    elif hasattr(request.user, "patient_id"):
        return "user"
    elif hasattr(request.user, "doctor_id"):
        return "doctor"
    else:
        return "visitor"
