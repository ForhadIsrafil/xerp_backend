from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from .models import User, UserRoleDepartment, UserModelPermission
from django.utils.crypto import get_random_string
from django.db import transaction, IntegrityError
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework import exceptions
from rest_framework import status
from django.apps import apps


# Create custom api exception
class CustomAPIException(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'error'

    def __init__(self, detail, status_code=None):
        self.detail = detail
        if status_code is not None:
            self.status_code = status_code


class TokenSerializer(AuthTokenSerializer):
    pass


class UserSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()
    departmentrole = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'email', 'cellphone', 'password', 'first_name', 'last_name', 'departmentrole')

        extra_kwargs = {'password': {'write_only': True}}

    def get_email(self, obj):
        return obj.username

    def get_departmentrole(self, obj):
        try:
            dept_role = UserRoleDepartment.objects.filter(user_id=obj.id)
        except UserRoleDepartment.DoesNotExist:
            return None
        return [dr.as_json() for dr in dept_role]

    def create(self, validated_data):
        initial_data = self.initial_data
        email = initial_data.get('email')
        password = initial_data.get('password')
        first_name = initial_data.get('first_name')
        last_name = initial_data.get('last_name')
        cellphone = initial_data.get('cellphone')

        if User.validate_unique_email(email):
            raise serializers.ValidationError({'email': 'This email already exists.'}, code='error')

        security_code = get_random_string(length=5)

        extra_fields = {
            'first_name': first_name,
            'last_name': last_name,
            'cellphone': cellphone
        }

        user = User._create_user(email, password, security_code, **extra_fields)
        return user


class ForgotPasswordTokenSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    security_code = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'email', 'security_code')  # name or username ?

    def get_security_code(self, user):
        return user.security_code

    def get_id(self, obj):
        return obj.id

    def get_email(self, obj):
        return obj.username

    def update(self, user, validated_data):
        user.security_code = get_random_string(length=5)
        user.save()
        return user


class ResetPasswordSerializer(serializers.Serializer):
    security_code = serializers.CharField(required=True, write_only=True)
    password = serializers.CharField(
        required=True,
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False, write_only=True
    )

    @transaction.atomic
    def validate(self, attrs):

        security_code = attrs.get('security_code')
        password = attrs.get('password')

        if security_code and password:
            user = User.objects.filter(security_code=security_code).first()
            if not user:
                raise CustomAPIException({'error': "Security code already used or expired."},
                                         status_code=status.HTTP_409_CONFLICT)
            else:
                user.set_password(raw_password=password)
                user.save()

                db_transaction = transaction.savepoint()
                user.security_code = ""
                user.save()

                try:
                    transaction.savepoint_commit(db_transaction)
                except IntegrityError:
                    transaction.savepoint_rollback(db_transaction)
        else:
            msg = _('Must include "security_code" and "password".')
            raise serializers.ValidationError(msg, code='error')

        return attrs


