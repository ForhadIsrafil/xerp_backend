import logging
from django.db import transaction
from apps.common_utils.Enums.app_enum import AppEnum
from core.models import App

logger = logging.getLogger(__name__)


def init_app():
    apps = AppEnum.get_all()
    include_ids = []
    logger.info("Creating Apps")
    with transaction.atomic():
        for app_name in apps:
            instance = App.create_or_update(name=app_name)
            include_ids += [instance.pk]

