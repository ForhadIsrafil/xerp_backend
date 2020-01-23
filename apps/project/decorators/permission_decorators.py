import logging
from functools import wraps
import json
from apps.common_utils.Enums.permission_enum import PermissionEnum
from core.models import Model, DepartmentModelPermission, Department, DepartmentRoleModelPermission, Permission
from apps.lib.get_object import get_object_or_404
from user.models import UserRoleDepartment, UserModelPermission
from rest_framework.exceptions import PermissionDenied

logger = logging.getLogger(__file__)


def require_permissions(model_name):
    def outer_wrapper(func):
        @wraps(func)
        def wrapped(self, *args, **kwargs):

            request = self.request
            request_method = self.request.method

            if request_method == "GET":
                req_perm_name = PermissionEnum.VIEW.value
            elif request_method == "POST":
                req_perm_name = PermissionEnum.CREATE.value
            elif request_method == "PUT":
                req_perm_name = PermissionEnum.UPDATE.value
            elif request_method == "DELETE":
                req_perm_name = PermissionEnum.DELETE.value
            else:
                req_perm_name = PermissionEnum.VIEW.value

            if request.method == "GET":
                department_id = request.GET.get('department_id')
            else:
                department_id = request.data.get('department_id')

            department_instance = get_object_or_404(Department, department_id)

            user_instance = request.user

            # (Time to get user role)
            user_role_dept_instances = UserRoleDepartment.objects.filter(user_id=user_instance.id,
                                                                         department_id=department_instance.id)
            if user_role_dept_instances.exists():
                user_role_dept_instance = user_role_dept_instances.first()
                user_role_id = user_role_dept_instance.role_id
            else:
                raise PermissionDenied("You are not Authorized to access this information.")

            model_instance = Model.objects.filter(name=model_name).first()

            # Now time to get Permission start
            temp_perm_list = []

            # step1 :  Look at DepartmentModelPermission
            department_model_perm_instances = DepartmentModelPermission.objects.filter(
                department_id=department_instance.id, model_id=model_instance.id)
            for department_model_perm_instance in department_model_perm_instances:
                temp_perm_list.append(department_model_perm_instance.permission_id)

            # step2 :  Look at DepartmentRoleModelPermission

            department_role_model_permission_instances = DepartmentRoleModelPermission.objects.filter(
                department_id=department_instance.id,
                role_id=user_role_id, model_id=model_instance.id)

            for department_role_model_permission_instance in department_role_model_permission_instances:
                temp_perm_list.append(department_role_model_permission_instance.permission_id)

            user_model_permission_instances = UserModelPermission.objects.filter(user_id=user_instance.id,
                                                                                 model_id=model_instance.id)

            for user_model_permission_instance in user_model_permission_instances:
                temp_perm_list.append(user_model_permission_instance.permission_id)

            # Now time to get Permission end

            is_allow = False

            for sp_id in set(temp_perm_list):  # View, Create, Update
                perm_instance = Permission.objects.get(id=sp_id)

                # This 2 line only for checking if it is allowed START
                user_model_permission_instance = UserModelPermission.objects.filter(user_id=user_instance.id,
                                                                                    model_id=model_instance.id,
                                                                                    permission_id=perm_instance.id).first()
                if user_model_permission_instance:
                    if user_model_permission_instance.allow == 0 and perm_instance.name == req_perm_name:
                        raise PermissionDenied("You are not Authorized to access this information.")

                # This 2 line only for checking if it is allowed END

                if perm_instance.name == req_perm_name:
                    is_allow = True     # <<<=========   Only Here we can permit the request
                    break

            if is_allow:
                response = func(self, *args, **kwargs)
                return response
            else:
                raise PermissionDenied("You are not Authorized to access this information.")



        return wrapped

    return outer_wrapper
