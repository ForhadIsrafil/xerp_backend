import logging
from django.db import transaction
from apps.common_utils.Enums.role_enum import RoleEnum
from core.models import Role

logger = logging.getLogger(__name__)


def init_role():
    names = RoleEnum.get_all()
    include_ids = []
    logger.info("Creating Roles")
    with transaction.atomic():
        for name in names:
            instance = Role.create_or_update(name=name)
            include_ids += [instance.pk]
