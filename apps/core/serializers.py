from rest_framework import serializers
from .models import Department, Role, DepartmentModelPermission, DepartmentRoleModelPermission, Permission, Model
from user.models import User, UserModelPermission
from user.serializers import UserSerializer
from django.db import transaction


class GetAppModelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = ('id', 'name', 'app')


class DepartmentRoleModelPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartmentRoleModelPermission
        fields = ('id', 'department', 'role', 'model', 'permission')

    @transaction.atomic
    def create(self, valid_data):
        instance = super(DepartmentRoleModelPermissionSerializer, self).create(valid_data)
        return instance

    def validate(self, data):
        data = super(DepartmentRoleModelPermissionSerializer, self).validate(data)
        return data


class UserModelPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModelPermission
        fields = ('id', 'user', 'model', 'permission', 'allow')

    @transaction.atomic
    def create(self, valid_data):
        instance = super(UserModelPermissionSerializer, self).create(valid_data)
        return instance

    def validate(self, data):
        data = super(UserModelPermissionSerializer, self).validate(data)
        return data


class DepartmentModelPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartmentModelPermission
        fields = ('id', 'department', 'model', 'permission')

    @transaction.atomic
    def create(self, valid_data):
        initial_data = self.initial_data
        department = initial_data.get('department')
        model = initial_data.get('model')
        permission = initial_data.get('permission')
        department_model_permission = DepartmentModelPermission(department_id=department, model_id=model,
                                                                permission_id=permission)
        department_model_permission.save()
        return department_model_permission

    def validate(self, data):
        data = super(DepartmentModelPermissionSerializer, self).validate(data)
        return data


class DepartmentRoleModelPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartmentRoleModelPermission
        fields = ('id', 'department', 'role', 'model', 'permission')

    @transaction.atomic
    def create(self, valid_data):
        instance = super(DepartmentRoleModelPermissionSerializer, self).create(valid_data)
        return instance

    def validate(self, data):
        data = super(DepartmentRoleModelPermissionSerializer, self).validate(data)
        return data


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('id', 'name', 'created_at')

    @transaction.atomic
    def create(self, valid_data):
        initial_data = self.initial_data
        name = initial_data['name']
        request = self.context.get('request')
        user = User.objects.get(id=request.user.id)

        department = Department(name=name, company_id=user.company_id)
        department.save()
        return department

    def validate(self, data):
        data = super(DepartmentSerializer, self).validate(data)
        return data


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ('id', 'name', 'created_at')

    @transaction.atomic
    def create(self, valid_data):
        initial_data = self.initial_data
        name = initial_data['name']
        request = self.context.get('request')
        user = User.objects.get(id=request.user.id)

        role = Role(name=name, company_id=user.company_id)
        role.save()
        return role

    def validate(self, data):
        data = super(RoleSerializer, self).validate(data)
        return data


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ('id', 'name')
