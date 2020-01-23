from django.apps import apps


def load_model(app_name, model_name):
    try:
        model = apps.get_model(app_name, model_name)
        return model
    except Exception as exp:
        return None