import json
from apps.common_utils.Enums.department_enum import DepartmentNameEnum
from apps.common_utils.Enums.model_enum import ModelEnum
from apps.common_utils.Enums.role_enum import RoleEnum
from core.models import DepartmentModelPermission, Model, Role, Permission
from apps.lib.clock import Clock
from apps.lib.mailer import Mailer
from apps.lib.upload import upload_byte_file, upload_file_s3
from core.models import Company, Department, Country, City, State, Address
from project.serializers import CompanySerializer
from user.models import UserRoleDepartment
from .models import UserAWSBucketInfo, User
from django.conf import settings
from django.http import Http404
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt
from rest_framework import parsers, renderers
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from .user_query_manager import *
from boto.s3.key import Key
from django.apps import apps
from urllib.parse import urljoin
from boto.s3.connection import S3Connection, S3ResponseError
import os
import requests
from rest_framework.authtoken.models import Token

THUMBNAIL_SIDE_LIMIT = settings.THUMBNAIL_SIDE_LIMIT


class Countries(APIView):

    def get(self, request):
        countries = [c.as_json() for c in Country.objects.filter(is_active=True)]
        return Response(countries, status=status.HTTP_200_OK)


class ObtainAuthToken(ObtainAuthToken):
    serializer_class = TokenSerializer
    http_method_names = ['post']
    permission_classes = (AllowAny,)

    @csrf_exempt
    def post(self, request):
        data = get_login_data_formate(request.data)
        mode = request.data.get('mode', None)
        if mode == 'sml':
            sml_user = User.objects.filter(username=request.data.get('email')).first()
            if sml_user is None:
                data = {
                    "email": request.data.get('email', None),
                    "password": request.data.get('password', None)
                }
                serializer = UserSerializer(data=data, context={'request': request})
                if serializer.is_valid():
                    serializer.save()
                    user = User.objects.get(id=serializer.data['id'])
                    return Response(user.as_json(), status=status.HTTP_200_OK)

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            user = User.objects.filter(pk=serializer.validated_data['user'].id, is_active=True).first()

            if user is None:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            with transaction.atomic():
                user.save()
                if user.is_2f_auth_enabled == True:
                    # user_info_without_token = user.as_json()
                    return Response({'success': True}, status=status.HTTP_200_OK)
                else:
                    return Response(user.as_json(), status=status.HTTP_200_OK)
        return Response({'message': 'Cannot login with provided credentials.'},
                        status=status.HTTP_400_BAD_REQUEST)


class Signout(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class UserRegister(APIView):

    @transaction.atomic
    def post(self, request):

        email = request.data.get('email', None)
        password = request.data.get('password', None)
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        cellphone = request.data.get('cellphone', None)
        company_name = request.data.get('company_name', None)
        address = request.data.get('address', None)
        country = request.data.get('country', None)
        postal_code = request.data.get('postal_code', None)

        if None in [email, password, cellphone, company_name, address, country]:
            return Response({'error': 'Credentials not given properly. '},
                            status=status.HTTP_400_BAD_REQUEST)

        _company_instance = Company.objects.filter(name=company_name).first()
        if _company_instance is not None:
            return Response({"error": "Company name already exists! Try another name please."},
                            status=status.HTTP_400_BAD_REQUEST)

        country_instance = Country.objects.filter(id=country).first()
        if country_instance is None:
            return Response({"error": "The provided country doesn't exist!"},
                            status=status.HTTP_400_BAD_REQUEST)

        address_instance = Address(full_address=address, country_id=country_instance.id,
                                   postal_code=postal_code)
        address_instance.save()

        # New Company Creating start
        company_instance = Company(name=company_name, address_id=address_instance.id)
        company_instance.save()
        # New Company Creating end
        data = {
            "email": email,
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
            "cellphone": cellphone,
            "company_id": company_instance.id
        }
        serializer = UserSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()

            # ========================= AUTHY ==========================
            url = 'https://api.authy.com/protected/json/users/new'
            headers = {'X-Authy-API-Key': settings.X_AUTHLY_API_KEY}
            data = {
                "user[email]": email,
                "user[cellphone]": cellphone,
                "user[country_code]": 880
            }
            create_user_response = requests.post(url, data=data, headers=headers)
            authy_response = json.loads(create_user_response.content.decode('utf-8'))
            # ========================= AUTHY END ========================

            role_instance = Role(name=RoleEnum.SUPER_ADMIN.value, company_id=company_instance.id)
            role_instance.save()

            department_instance = Department(name=DepartmentNameEnum.PROJECT_OWNER.value,
                                             company_id=company_instance.id)
            department_instance.save()

            user_instance = User.objects.filter(id=serializer.data['id']).first()
            user_instance.authy_id = authy_response['user']['id']
            user_instance.company_id = company_instance.id
            user_instance.save()

            user_role_instance = UserRoleDepartment(user_id=user_instance.id, role_id=role_instance.id,
                                                    department_id=department_instance.id)
            user_role_instance.save()

            # setting up PERMISSION start
            # @ ALL department ALL Model ALl Permission FOR DepartmentModelPermission

            # get_project_app_all_model_names = ModelEnum.get_project_app_all_model_names()
            # permission_obj = Permission.objects.all()
            # for model_name in get_project_app_all_model_names:
            #     for permission_id in permission_obj:
            #
            #         model_instances = Model.objects.filter(name=model_name).first()
            #         if model_instances is not None:
            #             department_role_model_instance = DepartmentModelPermission(department_id=department_instance.id,
            #                                                                        model_id=model_instances.id,
            #                                                                        permission_id=permission_id.id)
            #             department_role_model_instance.save()

            # setting up PERMISSION end

            email_res = User.send_signup_mail(email)
            if email_res != True:
                return Response(email_res, status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def set_registered_user_permission(user_id):
    user = User.objects.get(id=user_id)
    for model in apps.get_models():
        pass


class ActiveAccount(APIView):
    # throttle_classes = (AnonRateThrottle,)
    permission_classes = (AllowAny,)

    @csrf_exempt
    def post(self, request, format=None):
        security_code = request.data.get('security_code')
        user = User.objects.filter(security_code=security_code).first()

        if user is not None:

            if user.is_active is not False:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            with transaction.atomic():
                user.is_active = True
                user.save()
                token, created = Token.objects.get_or_create(user=user)
                user.security_code = None
                user.save()

            response = {
                "message": "Account successfully activated.",
                'user': user.as_json(),
                "success": True
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {
                "message": "Invalid security code or Session expired.",
                "success": False
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class ForgetPasswordView(APIView):
    permission_classes = ()
    authentication_classes = ()

    def get_user_obj(self, email):
        try:
            return User.objects.get(username=email)
        except User.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        email = request.data.get("email", None)
        if email is None:
            return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)
        user = self.get_user_obj(email)
        serializer = ForgotPasswordTokenSerializer(user, data={}, partial=True)
        if serializer.is_valid():
            serializer.save()

            # sending Mail
            subject = 'MyFarm: Reset Password.'
            email_body = "<strong> Hello ! </strong> " \
                         "<p>You’ve requested to reset your password. Use This code for reset your password." \
                         "</p> CODE:   <strong>" + str(serializer.data['security_code']) + "</strong><p> Thank you </p>"
            mailer = Mailer()
            response = mailer.send_email(recipient=email, subject=subject, html_message=email_body)

            if not response:
                return Response({'error': 'Email sending process failed. Please try again'},
                                status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ResetPasswordView(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = ResetPasswordSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data, partial=False)
        if serializer.is_valid():
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    permission_classes = (IsAuthenticated,)

    def patch(self, request, format=None):

        req_user = request.user
        password = request.data.get('new_password')
        if not password:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        trim_pass = password.strip()
        if trim_pass == '':
            return Response(status=status.HTTP_400_BAD_REQUEST)

        req_user.set_password(raw_password=trim_pass)
        req_user.save()
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class UploadView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        aws_access_key_id = settings.AWS_ACCESS_KEY_ID
        aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY_ID

        conn = S3Connection(aws_access_key_id, aws_secret_access_key)

        file = request.FILES.get('file')

        # check UserAWSBucketInfo
        useraws_instance = UserAWSBucketInfo.objects.filter(user_id=request.user.id).first()
        if useraws_instance is not None:
            bucket_name = useraws_instance.name
            bucket_instance = conn.get_bucket(bucket_name)
        else:
            user_id = request.user.id
            bucket_name = str(user_id) + '-' + get_random_string(5).lower() + '-bucket'

            bucket_instance = conn.create_bucket(bucket_name)

            create_bucket_name = UserAWSBucketInfo(user_id=request.user.id, name=bucket_name)
            create_bucket_name.save()

        filename = upload_file_s3(file=file, bucket_instance=bucket_instance)

        file_link = 'https://s3.amazonaws.com/' + bucket_name + '/' + filename

        response = {
            'link': file_link
        }
        return Response(response, status=status.HTTP_200_OK)


class UpdateProfileView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        req_user = request.user
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')

        user = User.objects.get(id=req_user.id)

        if None in [first_name, last_name]:
            return Response({'error': 'first_name and last_name not given properly. '},
                            status=status.HTTP_400_BAD_REQUEST)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        response = {
            'user': user.as_json()
        }
        return Response(response, status=status.HTTP_200_OK)


class UserInfo(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, user_id):
        user = User.objects.filter(pk=user_id, is_active=True).first()
        if user is not None:
            return Response(user.user_data(), status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CreateCompany(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        req_user = request.user.id
        name = request.data.get('name', None)

        data = {
            "name": name,
            "is_active": True,
            "created_at": Clock.utc_now(),
            "user_id": req_user
        }

        serializer = CompanySerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyInfo(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, company_id):
        company = Company.objects.filter(pk=company_id, is_active=True).first()
        if company is not None:
            return Response(company.as_json(), status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CompanyInfoByUser(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, user_id):
        companies = [company.as_json() for company in
                     Company.objects.filter(user_id=user_id, is_active=True).order_by('-id')]
        if companies is not None:
            return Response(companies, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class Set2FEnablePermissionView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, authy_id):
        enabled = request.data.get('enabled', None)
        authy_instance = User.objects.filter(authy_id=authy_id).first()
        if authy_instance is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if enabled == '1':
            authy_instance.is_2f_auth_enabled = True
            authy_instance.save()
            return Response({'success': 'Two factor authentication enabled!'}, status=status.HTTP_201_CREATED)
        elif enabled == '0':
            authy_instance.is_2f_auth_enabled = False
            authy_instance.save()
            return Response({'success': 'Two factor authentication disable!'}, status=status.HTTP_201_CREATED)


class Check2FTokenCodeView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        authentication_token = request.data.get('authentication_token', None)
        authy_id = request.data.get('authy_id', None)

        verified_url = "https://api.authy.com/protected/json/verify/" + str(authentication_token) + "/" + str(
            authy_id)  # token / authy_id
        headers = {"X-Authy-API-Key": settings.X_AUTHLY_API_KEY}

        verified_response = requests.get(verified_url, data={}, headers=headers)
        if verified_response.status_code == 401:
            return Response({'error': 'Token expired! Try again.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user_instance = User.objects.filter(authy_id=authy_id).first()
            if user_instance is not None:
                without_token = user_instance.as_json()
                del without_token['token']
                return Response(without_token, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'User doesn\'t exist.'}, status=status.HTTP_400_BAD_REQUEST)
