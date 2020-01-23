import logging
from django.db import transaction
from apps.common_utils.Enums.department_enum import DepartmentNameEnum
from core.models import Department


logger = logging.getLogger(__name__)


def init_departments():
    pass
    # names = DepartmentNameEnum.get_all()
    # include_ids = []
    # logger.info("Creating Departments")
    # with transaction.atomic():
    #     for name in names:
    #         instance = Department.create_or_update(name=name)
    #         include_ids += [instance.pk]
