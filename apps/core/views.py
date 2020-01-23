from user.serializers import UserSerializer
from .models import ProjectAudit, GoalAudit, TaskAudit, TaskDetailAudit, License, DepartmentModelPermission, \
    DepartmentRoleModelPermission, Role, Department, Invitation, Model, App, Permission
from django.db.models import Q
from user.models import UserModelPermission, User, UserRoleDepartment
from django.http import Http404

from apps.common_utils.Enums.model_enum import ModelEnum
from apps.common_utils.Enums.permission_enum import PermissionEnum
from apps.lib.get_object import get_object_or_404
from django.db import transaction
from rest_framework import status
from django.conf import settings
from lib.mailer import Mailer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import viewsets
from .serializers import GetAppModelsSerializer, DepartmentRoleModelPermissionSerializer, UserModelPermissionSerializer, \
    DepartmentModelPermissionSerializer, DepartmentSerializer, RoleSerializer, PermissionSerializer

from user.models import UserRoleDepartment
import requests


class GetAppModelsViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = GetAppModelsSerializer

    def get_queryset(self):
        app_id = self.request.data.get('app_id', None)
        models_instances = Model.objects.filter(app_id=app_id).all().order_by('-id')
        return models_instances

    def get_serializer_context(self):
        return {'request': self.request}


class GetUserPermissonsVieSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        app_id = request.data.get('app_id', None)
        user_id = request.data.get('user_id', None)
        department_id = request.data.get('department_id', None)
        user_instance = get_object_or_404(User, user_id)
        app_instance = get_object_or_404(App, app_id)
        department_instance = get_object_or_404(Department, department_id)

        # (Time to get user role)
        user_role_dept_instances = UserRoleDepartment.objects.filter(user_id=user_instance.id,
                                                                     department_id=department_instance.id)

        if user_role_dept_instances.exists():
            user_role_dept_instance = user_role_dept_instances.first()
            user_role_id = user_role_dept_instance.role_id
        else:
            return Response({'error': 'User role not found.'}, status=status.HTTP_400_BAD_REQUEST)

        if app_instance.name == 'Project':
            permission_list = []
            get_project_app_all_model_names = ModelEnum.get_project_app_all_model_names()

            for model_name in get_project_app_all_model_names:
                pass
                # model_instance = Model.objects.filter(name=model_name).first()
                #
                # # Now time to get Permission start
                # temp_perm_list = []
                #
                # # step1 :  Look at DepartmentModelPermission
                # department_model_perm_instances = DepartmentModelPermission.objects.filter(
                #     department_id=department_instance.id, model_id=model_instance.id)
                # for department_model_perm_instance in department_model_perm_instances:
                #     temp_perm_list.append(department_model_perm_instance.permission_id)
                #
                # # step2 :  Look at DepartmentRoleModelPermission
                #
                # department_role_model_permission_instances = DepartmentRoleModelPermission.objects.filter(
                #     department_id=department_instance.id,
                #     role_id=user_role_id, model_id=model_instance.id)
                #
                # for department_role_model_permission_instance in department_role_model_permission_instances:
                #     temp_perm_list.append(department_role_model_permission_instance.permission_id)
                #
                # # Now time to get Permission end
                # user_model_permission_instances = UserModelPermission.objects.filter(user_id=user_instance.id,
                #                                                                      model_id=model_instance.id)
                #
                # for user_model_permission_instance in user_model_permission_instances:
                #     temp_perm_list.append(user_model_permission_instance.permission_id)
                #
                # for sp_id in set(temp_perm_list):
                #     output = {}
                #     sp_instance = Permission.objects.get(id=sp_id)
                #
                #     output['model'] = model_instance.id
                #     output['model_name'] = model_instance.name
                #     output['permission'] = sp_instance.id
                #     output['permission_name'] = sp_instance.name
                #
                #     # allow remaining
                #     user_model_permission_instance = UserModelPermission.objects.filter(user_id=user_instance.id,
                #                                                                         model_id=model_instance.id).first()
                #     is_perm_allowed = True
                #     if user_model_permission_instance:
                #         if user_model_permission_instance.allow == False:
                #             is_perm_allowed = False
                #     output['allow'] = is_perm_allowed
                #
                # # if len(output) > 0:
                #     permission_list.append(output)

            return Response({'models_permissions': permission_list}, status=status.HTTP_200_OK)


class UpdateUserPermissionViewSet(ViewSet):
    @transaction.atomic
    def create(self, request):
        user_id = request.data.get('user_id', None)
        model_id = request.data.get('model_id', None)
        permission_id = request.data.get('permission_id', None)
        allow = request.data.get('allow', None)

        user_instance = get_object_or_404(User, user_id)
        model_instance = get_object_or_404(Model, model_id)
        permission_instance = get_object_or_404(Permission, permission_id)

        user_model_permission_instances = UserModelPermission.objects.filter(user_id=user_instance,
                                                                             model_id=model_instance,
                                                                             permission_id=permission_instance)

        if user_model_permission_instances.exists():
            user_model_permission_instance = user_model_permission_instances.first()
            user_model_permission_instance.allow = allow  # or just 'True if allow == 1 else False'
            user_model_permission_instance.save()
        else:
            user_model_permission_instance = UserModelPermission(user_id=user_instance.id, model_id=model_instance.id,
                                                                 permission_id=permission_instance.id, allow=allow)
            user_model_permission_instance.save()
        return Response(status=status.HTTP_200_OK)


class DepartmentRoleModelPermissionCrudViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = DepartmentRoleModelPermissionSerializer

    @transaction.atomic
    def create(self, request):
        serializer = DepartmentRoleModelPermissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def retrieve(self, request):
        department_id = request.data.get('department', None)

        department_model_permission_instances = DepartmentRoleModelPermission.objects.filter(
            department_id=department_id).all()
        user = get_object_or_404(User, request.data.get('user_id'))
        if user is not None:
            serializer = DepartmentRoleModelPermissionSerializer(department_model_permission_instances)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        department_id = self.request.data.gete4rtt('department', None)
        department_model_permission_instances = DepartmentRoleModelPermission.objects.filter(
            department_id=department_id).all()
        return department_model_permission_instances

    def get_serializer_context(self):
        return {'request': self.request}

    @transaction.atomic
    def patch(self, request):
        department = request.data.get('department', None)
        role = request.data.get('role', None)
        model = request.data.get('model', None)
        permission = request.data.get('permission', None)

        department_model_permission_instance = DepartmentRoleModelPermission.objects.filter(department=department,
                                                                                            role=role,
                                                                                            model=model,
                                                                                            permission=permission).first()

        user = get_object_or_404(User, request.data.get('user_id'))
        if user is not None and department_model_permission_instance is not None:
            serializer = DepartmentRoleModelPermissionSerializer(department_model_permission_instance,
                                                                 data=request.data,
                                                                 partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def destroy(self, request):
        department = request.data.get('department', None)
        role = request.data.get('role', None)
        model = request.data.get('model', None)
        permission = request.data.get('permission', None)

        department_model_permission_instance = DepartmentRoleModelPermission.objects.filter(department=department,
                                                                                            role=role,
                                                                                            model=model,
                                                                                            permission=permission).first()
        user = get_object_or_404(User, request.data.get('user_id'))
        if user is not None and department_model_permission_instance is not None:
            department_model_permission_instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserModelPermissionCrudViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserModelPermissionSerializer

    @transaction.atomic
    def create(self, request):
        serializer = UserModelPermissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        user_id = self.request.data.get('user', None)
        user_model_permission_instances = UserModelPermission.objects.filter(user=user_id).all().order_by('-id')
        return user_model_permission_instances

    def get_serializer_context(self):
        return {'request': self.request}

    @transaction.atomic
    def patch(self, request):
        user_id = request.data.get('user', None)
        model = request.data.get('model', None)
        permission = request.data.get('permission', None)

        user_model_permission_instance = UserModelPermission.objects.filter(user=user_id, model=model,
                                                                            permission=permission).first()

        user = get_object_or_404(User, request.data.get('user'))
        if user is not None and user_model_permission_instance is not None:
            serializer = UserModelPermissionSerializer(user_model_permission_instance, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def destroy(self, request):
        user_id = request.data.get('user', None)
        model = request.data.get('model', None)
        permission = request.data.get('permission', None)

        user_model_permission_instance = UserModelPermission.objects.filter(user=user_id, model=model,
                                                                            permission=permission).first()

        user = get_object_or_404(User, request.data.get('user'))
        if user is not None and user_model_permission_instance is not None:
            user_model_permission_instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class DepartmentModelPermissionViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = DepartmentModelPermissionSerializer

    @transaction.atomic
    def create(self, request):
        serializer = DepartmentModelPermissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        return DepartmentModelPermission.objects.all().order_by('-id')

    def get_serializer_context(self):
        return {'request': self.request}


class SingleDepartmentModelPermissionViewSet(ViewSet):
    permission_classes = (IsAuthenticated,)

    @transaction.atomic
    def patch(self, request, id):
        department_model_permission_instance = get_object_or_404(DepartmentModelPermission, id)
        serializer = DepartmentModelPermissionSerializer(department_model_permission_instance, data=request.data,
                                                         partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def destroy(self, request, id):
        department_model_permission_instance = get_object_or_404(DepartmentModelPermission, id)
        department_model_permission_instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DepartmentRoleModelPermissionViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = DepartmentRoleModelPermissionSerializer

    @transaction.atomic
    def create(self, request):
        serializer = DepartmentRoleModelPermissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        return DepartmentRoleModelPermission.objects.all().order_by('-id')

    def get_serializer_context(self):
        return {'request': self.request}


class SingleDepartmentRoleModelPermissionViewSet(ViewSet):
    permission_classes = (IsAuthenticated,)

    @transaction.atomic
    def patch(self, request, id):
        department_role_model_permission_instance = get_object_or_404(DepartmentRoleModelPermission, id)
        serializer = DepartmentRoleModelPermissionSerializer(department_role_model_permission_instance,
                                                             data=request.data,
                                                             partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def destroy(self, request, id):
        department_role_model_permission_instance = get_object_or_404(DepartmentRoleModelPermission, id)
        department_role_model_permission_instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DepartmentViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = DepartmentSerializer

    @transaction.atomic
    def create(self, request):
        if request.data.get('name') is '':
            return Response({'error': 'Provide a department title!'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = DepartmentSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        user = User.objects.get(id=self.request.user.id, is_active=True)
        return Department.objects.filter(company_id=user.company_id, is_active=True).order_by('-id')

    def get_serializer_context(self):
        return {'request': self.request}


class SingleDepartmentViewSet(ViewSet):
    permission_classes = (IsAuthenticated,)

    @transaction.atomic
    def patch(self, request, id):
        try:
            department_instance = Department.objects.get(id=id, is_active=True)
        except Department.DoesNotExist:
            raise Http404("Not Found")
        serializer = DepartmentSerializer(department_instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def destroy(self, request, id):
        try:
            department_instance = Department.objects.get(id=id, is_active=True)
        except Department.DoesNotExist:
            raise Http404("Not Found")
        department_instance.is_active = False
        department_instance.save()
        request.data['name'] = department_instance.name
        serializer = DepartmentSerializer(department_instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoleViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = RoleSerializer

    @transaction.atomic
    def create(self, request):
        if request.data.get('name') is '':
            return Response({'error': 'Provide a Role name!'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = RoleSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        user = User.objects.get(id=self.request.user.id, is_active=True)
        return Role.objects.filter(company_id=user.company_id, is_active=True).order_by('-id')

    def get_serializer_context(self):
        return {'request': self.request}


class SingleRoleViewSet(ViewSet):
    permission_classes = (IsAuthenticated,)

    @transaction.atomic
    def patch(self, request, id):
        try:
            role_instance = Role.objects.get(id=id, is_active=True)
        except Role.DoesNotExist:
            raise Http404("Not Found")
        serializer = RoleSerializer(role_instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def destroy(self, request, id):
        try:
            role_instance = Role.objects.get(id=id, is_active=True)
        except Department.DoesNotExist:
            raise Http404("Not Found")
        role_instance.is_active = False
        role_instance.save()
        request.data['name'] = role_instance.name
        serializer = RoleSerializer(role_instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PermissionViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = PermissionSerializer

    def get_queryset(self):
        return Permission.objects.all().order_by('id')

    def get_serializer_context(self):
        return {'request': self.request}


class GetCompanyUsers(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_queryset(self):
        user = User.objects.get(id=self.request.user.id, is_active=True)
        return User.objects.filter(company_id=user.company_id).order_by('-id')

    def get_serializer_context(self):
        return {'request': self.request}