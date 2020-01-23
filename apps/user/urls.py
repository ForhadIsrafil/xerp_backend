from django.urls import path
from .views import *

app_name = 'user'

urlpatterns = [
    path('signin', view=ObtainAuthToken.as_view(), name='signin'),
    path('user/<int:user_id>', view=UserInfo.as_view(), name='user_info'),
    path('countries', Countries.as_view()),
    path('signup', view=UserRegister.as_view(), name='signup'),
    path('active-account', ActiveAccount.as_view(), name="active_account"),
    path('signout', view=Signout.as_view(), name='signout'),
    path('forget-password', ForgetPasswordView.as_view(),
         name='forget_password'),
    path('reset-password', ResetPasswordView.as_view(),
         name='reset_password'),
    path('change-password', ChangePasswordView.as_view(),
         name='reset_password'),
    path('upload', UploadView.as_view()),
    path('update-profile', UpdateProfileView.as_view()),
    path('company/create', CreateCompany.as_view()),
    path('company/<int:company_id>', CompanyInfo.as_view()),
    path('company/user/<int:user_id>', CompanyInfoByUser.as_view()),
    path('set-2f_enable-permission/<int:authy_id>', Set2FEnablePermissionView.as_view()),
    path('check-2f-token-code', Check2FTokenCodeView.as_view()),
]
