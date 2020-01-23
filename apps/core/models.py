from django.db import models
from common_utils.base_entity import BaseEntityBasicAbstract, NameAbstract
from django.apps import apps
from project.models import Project, Goal, Task
from user.models import User
from core.xerpio.file_manager import FileManager

from apps.common_utils.Enums.app_enum import AppEnum


class BaseContact(BaseEntityBasicAbstract):
    name = models.CharField(max_length=1000)
    short_name = models.CharField(max_length=20, null=True, blank=True)
    parent = models.ForeignKey("self", null=True, blank=True, related_name="self", on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Country(BaseContact):
    phone_code = models.CharField(max_length=10, null=True, blank=True)

    def as_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "short_name": self.short_name,
            "phone_code": self.phone_code
        }

    @classmethod
    def load_from_json(cls, json_file_path):
        country_json_data = FileManager.read_json(json_file_path)
        countries = country_json_data.get('countries', [])
        total_countries = len(countries)
        for i, country in enumerate(countries):
            short_name = country['short_name']
            name = country['name']
            phone_code = country['phone_code']

            country_instances = cls.objects.filter(name=name, short_name=short_name)
            if country_instances.exists():
                country_instance = country_instances.first()
            else:
                country_instance = cls()

            country_instance.name = name
            country_instance.short_name = short_name
            country_instance.phone_code = phone_code
            country_instance.is_active = True
            country_instance.save()


class State(BaseContact):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    @classmethod
    def get_serializer(cls):
        BaseSerializer = super(State, cls).get_serializer()

        class StateSerializer(BaseSerializer):
            class Meta(BaseSerializer.Meta):
                fields = ('id', 'name', 'short_name', 'parent', 'is_active', 'country')
                read_only_fields = ('id',)

        return StateSerializer


class City(BaseContact):
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    @classmethod
    def get_serializer(cls):
        BaseSerializer = super(City, cls).get_serializer()

        class CitySerializer(BaseSerializer):
            class Meta(BaseSerializer.Meta):
                fields = ('id', 'name', 'short_name', 'parent', 'is_active', 'state')
                read_only_fields = ('id',)

        return CitySerializer


class Address(BaseEntityBasicAbstract):
    title = models.CharField(max_length=1000, null=True, blank=True)  # Home Address, Office Address etc
    full_address = models.TextField(null=True, blank=True)
    country = models.ForeignKey(Country, null=True, blank=True, on_delete=models.CASCADE)
    # city = models.ForeignKey(City, null=True, blank=True, on_delete=models.CASCADE)
    # state = models.ForeignKey(State, null=True, blank=True, on_delete=models.CASCADE)
    postal_code = models.CharField(max_length=100, null=True, blank=True)


class Company(BaseEntityBasicAbstract):
    name = models.CharField(max_length=100, unique=True)
    address = models.ForeignKey(Address, null=True, blank=True, on_delete=models.CASCADE)

    def as_json(self):
        try:
            checked_address = Address.objects.get(id=self.address_id)
        except Address.DoesNotExist:
            checked_address = None
        return {
            "id": self.id,
            "name": self.name,
            "address": checked_address.id  # Address.objects.get(id=self.address)
        }

    @classmethod
    def _create_company(cls, name=None, address=None):
        """
        Create and save a user . overwriting model info
        """
        company = cls(name=name)
        company.name = name
        company.address = address
        company.save()
        return company


class Department(BaseEntityBasicAbstract,
                 NameAbstract):  # Accounting , HR, Project (Auto-generated, but user can change.)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def as_json(self):
        return {
            "id": self.id,
            "name": self.name
        }

    @classmethod
    def create_or_update(cls, name, company, is_active=True):
        instances = cls.objects.filter(name=name)
        if instances.exists():
            instance = instances.first()
        else:
            instance = cls()

        instance.name = name
        instance.company = company
        instance.is_active = is_active
        instance.save()
        return instance


class Role(BaseEntityBasicAbstract, NameAbstract):  # Manager, Staff, Accountant, Admin  (user will Create)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def as_json(self):
        return {
            "id": self.id,
            "name": self.name
        }

    @classmethod
    def create_or_update(cls, name, company, is_active=True):
        instances = cls.objects.filter(name=name)
        if instances.exists():
            instance = instances.first()
        else:
            instance = cls()

        instance.name = name
        instance.company = company
        instance.is_active = is_active
        instance.save()
        return instance


class App(NameAbstract):  # System	Generated  .

    @classmethod
    def create_or_update(cls, name, is_active=True):
        instances = cls.objects.filter(name=name)
        if instances.exists():
            instance = instances.first()
        else:
            instance = cls()

        instance.name = name
        instance.is_active = is_active
        instance.save()
        return instance


class Model(NameAbstract):  # System	Generated
    app = models.ForeignKey(App, on_delete=models.CASCADE, null=True, blank=True)

    @classmethod
    def create_or_update(cls, name, is_active=True):
        instances = cls.objects.filter(name=name)
        if instances.exists():
            instance = instances.first()
        else:
            instance = cls()

        instance.name = name
        app_instance = App.objects.get(name=AppEnum.PROJECT.value)
        instance.app_id = app_instance.id
        instance.is_active = is_active
        instance.save()
        return instance


class License(BaseEntityBasicAbstract):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    app = models.ForeignKey(App, on_delete=models.CASCADE)


class Permission(NameAbstract):  # Create, Upload, Download, Update, Delete, Report, View

    def as_json(self):
        return {
            "id": self.id,
            "name": self.name
        }

    @classmethod
    def create_or_update(cls, name, is_active=True):
        instances = cls.objects.filter(name=name)
        if instances.exists():
            instance = instances.first()
        else:
            instance = cls()

        instance.name = name
        instance.is_active = is_active
        instance.save()
        return instance


class DepartmentModelPermission(BaseEntityBasicAbstract):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)


    class Meta:
        unique_together = ('department', 'model', 'permission')


class DepartmentRoleModelPermission(BaseEntityBasicAbstract):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('department', 'role', 'model', 'permission')

    @classmethod
    def create_or_update(cls, department_id, role_id, model_id, permission_id, is_active=True):
        instances = cls.objects.filter(department_id=department_id, role_id=role_id, model_id=model_id,
                                       permission_id=permission_id)
        if instances.exists():
            instance = instances.first()
        else:
            instance = cls()

        instance.is_active = is_active
        instance.department_id = department_id
        instance.role_id = role_id
        instance.model_id = model_id
        instance.permission_id = permission_id
        instance.save()
        return instance


class TaskIssueResulation(BaseEntityBasicAbstract):
    pass


class IssueDetails(BaseEntityBasicAbstract):
    pass


class Invitation(BaseEntityBasicAbstract):
    email = models.CharField(max_length=50)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('email', 'department')

    def as_json(self):
        return {
            'id': self.id,
            'email': self.email,
            'department': self.department_id,
            'role': self.role_id
        }


# ======================================= All Audit table here start  ==============================


class ProjectAudit(BaseEntityBasicAbstract, NameAbstract):
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    enabled = models.BooleanField(default=True)
    action = models.CharField(max_length=50)  # Create, Get, Update, Delete
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)


class GoalAudit(BaseEntityBasicAbstract, NameAbstract):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    visibility = models.BooleanField(default=True)  # Internal organization can all time . But if client will see or not
    enabled = models.BooleanField(default=True)
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    action = models.CharField(max_length=50)  # Create, Get, Update, Delete


class TaskAudit(BaseEntityBasicAbstract, NameAbstract):
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    status = models.BooleanField(default=True)  # Open, Close, Pending, To be used
    priority = models.BooleanField(default=True)  # Medium , High , Low
    enabled = models.BooleanField(default=True)
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+', null=True, blank=True)
    action = models.CharField(max_length=50)  # Create, Get, Update, Delete
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)


class TaskDetailAudit(BaseEntityBasicAbstract):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    action = models.CharField(max_length=50)  # Create, Get, Update, Delete
    path = models.CharField(max_length=150, null=True, blank=True)


class TaskFollowerAudit(BaseEntityBasicAbstract):  # Many to Many
    task = models.ForeignKey(Task, related_name='+', on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+', null=True, blank=True)
    action = models.CharField(max_length=50)  # Create, Get, Update, Delete


class IssueAudit(BaseEntityBasicAbstract):
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    attachment = models.FileField(max_length=500, null=True, blank=True, upload_to='media/file')
    description = models.TextField()
    path = models.CharField(max_length=150, null=True, blank=True)
    target_date = models.DateField(null=True, blank=True)
    visibility = models.BooleanField(default=True)  # Internal organization can all time . But if client will see or not
    classification = models.CharField(max_length=255, null=True, blank=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    action = models.CharField(max_length=50)  # Create, Get, Update, Delete


class IssueDetailsAudit(BaseEntityBasicAbstract):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    attachment = models.FileField(max_length=500, null=True, blank=True, upload_to='media/file')
    path = models.CharField(max_length=150, null=True, blank=True)
    action = models.CharField(max_length=50)  # Create, Get, Update, Delete


class TaskIssueResulationAudit(BaseEntityBasicAbstract):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    attachment = models.FileField(max_length=500, null=True, blank=True, upload_to='media/file')
    path = models.CharField(max_length=150, null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    action = models.CharField(max_length=50)  # Create, Get, Update, Delete


class LicenseAudit(BaseEntityBasicAbstract):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    app = models.ForeignKey(App, on_delete=models.CASCADE, null=True, blank=True)
    action = models.CharField(max_length=50)  # Create, Get, Update, Delete


class DepartmentModelPermissionAudit(BaseEntityBasicAbstract):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    model = models.ForeignKey(Model, on_delete=models.CASCADE, null=True, blank=True)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, null=True, blank=True)
    action = models.CharField(max_length=50)  # Create, Get, Update, Delete


class DepartmentRoleModelPermissionAudit(BaseEntityBasicAbstract):
    department = models.ForeignKey(Department, related_name='+', on_delete=models.CASCADE, null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True)
    model = models.ForeignKey(Model, on_delete=models.CASCADE, null=True, blank=True)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, null=True, blank=True)
    action = models.CharField(max_length=50)  # Create, Get, Update, Delete
# ======================================= All Audit table here end  ==============================
