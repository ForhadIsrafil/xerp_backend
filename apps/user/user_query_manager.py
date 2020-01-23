from .models import User


def get_login_data_formate(data):
    data = {
        "username": data.get('email', None),
        "password": data.get('password', None)
    }

    return data
