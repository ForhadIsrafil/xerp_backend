from django.urls import path
from .views import *

app_name = 'core'

urlpatterns = [
    path('get-app-models', view=GetAppModelsViewSet.as_view({'get': 'list'}), name='get_app_models'),
    path('get-user-permissions', view=GetUserPermissonsVieSet.as_view({'get': 'list'}), name='get_user_permissions'),
    path('update-user-permission', view=UpdateUserPermissionViewSet.as_view({'post': 'create'}),
         name='user_update_permission'),
    path('department-role-model-permission-crud', view=DepartmentRoleModelPermissionCrudViewSet.as_view(
        {'post': 'create', 'get': 'retrieve', 'patch': 'patch', 'delete': 'destroy'}),
         name='department_role_model_permission_crud'),
    path('user-model-permission-crud', view=UserModelPermissionCrudViewSet.as_view(
        {'post': 'create', 'get': 'list', 'patch': 'patch', 'delete': 'destroy'}), name='user_model_permission_crud'),

    path('department-model-permission',
         view=DepartmentModelPermissionViewSet.as_view({'post': 'create', 'get': 'list'}),
         name='department_model_permission'),
    path('department-model-permission/<int:id>',
         view=SingleDepartmentModelPermissionViewSet.as_view({'patch': 'patch', 'delete': 'destroy'}),
         name='single_department_model_permission'),

    path('department-role-model-permission',
         view=DepartmentRoleModelPermissionViewSet.as_view({'post': 'create', 'get': 'list'}),
         name='department_role_model_permission'),
    path('department-role-model-permission/<int:id>',
         view=SingleDepartmentRoleModelPermissionViewSet.as_view({'patch': 'patch', 'delete': 'destroy'}),
         name='single_department_role_model_permission'),

    path('department',
             view=DepartmentViewSet.as_view({'post': 'create', 'get': 'list'}),
             name='department'),
    path('department/<int:id>', view=SingleDepartmentViewSet.as_view({'patch': 'patch', 'delete': 'destroy'}),
             name='single_department'),

    path('role',
                 view=RoleViewSet.as_view({'post': 'create', 'get': 'list'}),
                 name='role'),
    path('role/<int:id>', view=SingleRoleViewSet.as_view({'patch': 'patch', 'delete': 'destroy'}),
             name='single_role'),

    path('users', view=GetCompanyUsers.as_view({'get': 'list'}), name='users'),
    path('permissions', view=PermissionViewSet.as_view({'get': 'list'}), name='permissions'),

]
