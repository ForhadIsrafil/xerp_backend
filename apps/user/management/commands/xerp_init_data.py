import os

from django.core.management.base import BaseCommand
from django.db import transaction
from user.management.commands.utils.init_model import init_model
from user.management.commands.utils.init_permission import init_basic_permission
import logging
from common_utils.Enums.app_enum import AppEnum
from core.models import App
from user.management.commands.utils.init_country import init_country

from apps.user.management.commands.utils.init_app import init_app

PROJECT_PATH = os.path.abspath(".")

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        # logger.info("Creating init_departments")
        # init_departments()

        # logger.info("Creating init_role")
        # init_role()

        logger.info("Creating init_app")
        init_app()

        logger.info("Creating init_model")
        init_model()

        logger.info("Creating init_country")
        init_country()

        logger.info("Creating init_basic_permission")
        init_basic_permission()

        # logger.info("Creating init_basic_permission")
        # init_basic_permission()
        #
        # logger.info("Creating init_department_role_model_permission")
        # init_department_model_permission()
