import logging

from django.db import transaction
from core.models import Model

logger = logging.getLogger(__name__)

from django.apps import apps
from django.conf import settings


def init_model():
    app_names = apps.get_models()

    include_ids = []
    logger.info("Creating Models")
    with transaction.atomic():
        for app_name in app_names:
            instance = Model.create_or_update(name=app_name.__name__)
            include_ids += [instance.pk]
