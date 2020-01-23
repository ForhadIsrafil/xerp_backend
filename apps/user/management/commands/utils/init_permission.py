import logging

from apps.common_utils.Enums.department_enum import DepartmentNameEnum
from apps.common_utils.Enums.model_enum import ModelEnum
from apps.common_utils.Enums.permission_enum import PermissionEnum
from django.db import transaction
from django.apps import apps
from core.models import Permission, DepartmentRoleModelPermission
from common_utils.Enums.role_enum import RoleEnum
from core.models import Model
from core.models import DepartmentModelPermission, Department, Role

logger = logging.getLogger(__name__)


def init_basic_permission():
    names = PermissionEnum.get_all()
    include_ids = []
    logger.info("Creating Permission")
    with transaction.atomic():
        for name in names:
            instance = Permission.create_or_update(name=name)
            include_ids += [instance.pk]


def init_department_model_permission():  #   GENERAL PERRMISSION START


#   ***********************************************   PROJECT DEPARTMENT START HERE ***********************************************

    # ====================   Start Setting Admin Permission(VIEW) for "PROJECT" department =========================

    view_model_dict = [ModelEnum.USER.value, ModelEnum.COMPANY.value, ModelEnum.PROJECT.value]

    department_id = Department.objects.get(name=DepartmentNameEnum.PROJECT.value).id
    permission_id = Permission.objects.get(name=PermissionEnum.VIEW.value).id

    for m in view_model_dict:
        model_id = Model.objects.get(name=m).id
        is_exist = DepartmentModelPermission.objects.filter(department_id=department_id, model_id=model_id,
                                                           permission_id=permission_id).exists()
        if not is_exist:
            instance = DepartmentModelPermission()
            instance.department_id = department_id
            instance.model_id = model_id
            instance.permission_id = permission_id
            instance.save()

    # ====================   End Setting Admin Permission(VIEW) for "PROJECT" department =========================



    # ====================   Start Setting Admin Permission(CREATE) for "PROJECT" department =========================

    create_model_dict = [ModelEnum.USER.value, ModelEnum.COMPANY.value, ModelEnum.PROJECT.value, ModelEnum.TASK.value]

    for m in create_model_dict:
        model_id = Model.objects.get(name=m).id
        is_exist = DepartmentModelPermission.objects.filter(department_id=department_id, model_id=model_id,
                                                           permission_id=permission_id).exists()
        if not is_exist:
            instance = DepartmentModelPermission()
            instance.department_id = department_id
            instance.model_id = model_id
            instance.permission_id = permission_id
            instance.save()


    # ====================   End Setting Admin Permission(CREATE) for "PROJECT" department =========================


    # ====================   Start Setting Admin Permission(UPDATE) for "PROJECT" department =========================

    update_model_dict = [ModelEnum.USER.value, ModelEnum.COMPANY.value, ModelEnum.PROJECT.value]

    for m in update_model_dict:
        model_id = Model.objects.get(name=m).id
        is_exist = DepartmentModelPermission.objects.filter(department_id=department_id, model_id=model_id,
                                                           permission_id=permission_id).exists()
        if not is_exist:
            instance = DepartmentModelPermission()
            instance.department_id = department_id
            instance.model_id = model_id
            instance.permission_id = permission_id
            instance.save()


    # ====================   End Setting Admin Permission(UPDATE) for "PROJECT" department =========================


    # ====================   Start Setting Admin Permission(DELETE) for "PROJECT" department =========================

    delete_model_dict = [ModelEnum.USER.value, ModelEnum.COMPANY.value, ModelEnum.PROJECT.value, ModelEnum.TASK.value]

    for m in delete_model_dict:
        model_id = Model.objects.get(name=m).id
        is_exist = DepartmentModelPermission.objects.filter(department_id=department_id, model_id=model_id,
                                                           permission_id=permission_id).exists()
        if not is_exist:
            instance = DepartmentModelPermission()
            instance.department_id = department_id
            instance.model_id = model_id
            instance.permission_id = permission_id
            instance.save()

    # ====================   End Setting Admin Permission(DELETE) for "PROJECT" department =========================


#   ***********************************************   PROJECT DEPARTMENT END HERE ***********************************************
