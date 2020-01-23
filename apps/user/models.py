from django.db import models
from django.contrib.auth.models import User as BaseUser
from django.apps import apps
from rest_framework.authtoken.models import Token
from common_utils.base_entity import BaseEntityBasicAbstract
from lib.mailer import Mailer
from django.conf import settings
from apps.common_utils.base_entity import NameAbstract


class User(BaseUser):
    cellphone = models.CharField(max_length=30)
    security_code = models.TextField(null=True, blank=True)
    image_url = models.CharField(max_length=255, null=True, blank=True)
    is_2f_auth_enabled = models.BooleanField(default=False)
    authy_id = models.CharField(max_length=50, null=True, blank=True)
    company = models.ForeignKey('core.Company', null=True, blank=True, on_delete=models.CASCADE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def as_json(self):
        token, created = Token.objects.get_or_create(user=self)
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.get_full_name(),
            "email": self.username,
            "cellphone": self.cellphone,
            "is_active": self.is_active,
            "token": token.key,
            "image_url": self.image_url,
            "is_2f_auth_enabled": self.is_2f_auth_enabled,
            "authy_id": self.authy_id,
            "company": self.company.as_json()
        }

    def user_data(self):
        dept_role = UserRoleDepartment.objects.filter(user_id=self.id)
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.get_full_name(),
            "email": self.username,
            "cellphone": self.cellphone,
            "is_active": self.is_active,
            "image_url": self.image_url,
            "company": self.company.as_json(),
            "departmentrole": [dr.as_json() for dr in dept_role]
        }

    def get_full_name(self):
        return (self.first_name + ' ' + self.last_name).strip()

    @classmethod
    def _create_user(cls, email=None, password=None, security_code=None, **extra_fields):
        """
        Create and save a user . overwriting model info
        """
        user = cls(username=email, **extra_fields)
        user.set_password(password)
        user.is_active = False
        user.is_admin = False
        user.security_code = security_code
        user.save()
        return user

    @classmethod
    def validate_unique_email(cls, email):
        return True if cls.objects.filter(username=email).exists() else False

    @classmethod
    def send_signup_mail(cls, email):
        user = User.objects.filter(username=email).first()
        if user is None:
            err_response = {'error': 'User not found.'}
            return err_response

        # sending Mail
        activation_link = settings.ACCOUNT_ACTIVATION_URL + str(user.security_code)
        subject = 'xERP: Signup email varification.'
        email_body = "<strong> Welcome to xERP! </strong> " \
                     "<p>You’ve requested for a new account. Here is the varification link given below. Please use this link to activate you account." \
                     "</p> <a href=" + activation_link + ">click here</a>  <p> Thank you </p>"
        mailer = Mailer()
        response = mailer.send_email(recipient=email, subject=subject, html_message=email_body)

        if not response:
            err_response = {'error': 'Email sending process failed. Please try again'}
            return err_response
        return True


class UserAWSBucketInfo(BaseEntityBasicAbstract, NameAbstract):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)


class UserRoleDepartment(BaseEntityBasicAbstract):  # Parvez	Sales		Manager
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    role = models.ForeignKey('core.Role', on_delete=models.CASCADE)
    department = models.ForeignKey('core.Department', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'department', 'role')

    def as_json(self):
        return {
            'id': self.id,
            'department': self.department.as_json(),
            'role': self.role.as_json()
        }


class UserModelPermission(BaseEntityBasicAbstract):  # Parvez	Chart of Account	Update
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    model = models.ForeignKey('core.Model', on_delete=models.CASCADE)
    permission = models.ForeignKey('core.Permission', on_delete=models.CASCADE)
    allow = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'model', 'permission')
