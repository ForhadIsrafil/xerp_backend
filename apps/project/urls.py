from django.urls import path
from .views import *

app_name = 'project'

urlpatterns = [
    path('project', view=ProjectViewSet.as_view({'post': 'create', 'get': 'list'}), name='project'),
    path('project/<int:id>', view=SingleProjectViewSet.as_view({'get': 'get', 'patch': 'patch', 'delete': 'destroy'}),
         name='single_project'),
    path('company/<int:company_id>/project', view=UserProjects.as_view({'get': 'list'}), name='user_projects'),
    path('projects-with-tasks', view=ProjectWithTasks.as_view({'get': 'get'}), name='project_with_tasks'),

    path('goal', view=GoalViewSet.as_view({'post': 'create', 'get': 'list'}), name='goal'),
    path('goal/<int:id>', view=SingleGoalViewSet.as_view({'get': 'get', 'patch': 'patch', 'delete': 'destroy'}),
         name='single_goal'),
    path('goal/project/<int:project_id>', view=ProjectGoals.as_view({'get': 'list'}), name='project_goals'),

    path('task', view=TaskViewSet.as_view({'post': 'create', 'get': 'list'}), name='task'),
    path('task/<int:id>', view=SingleTaskViewSet.as_view({'get': 'get', 'patch': 'patch', 'delete': 'destroy'}),
         name='single_task'),

    path('task-details', view=TaskDetailViewSet.as_view({'post': 'create', 'get': 'list'}), name='task_details'),
    path('task-details/<int:id>', view=SingleTaskDetailViewSet.as_view({'patch': 'patch', 'delete': 'destroy'}),
         name='single_task_details'),
    path('task/goal/<int:goal_id>', view=GoalTasks.as_view({'get': 'list'}), name='goal_tasks'),

    path('issue', view=IssueViewSet.as_view({'post': 'create', 'get': 'list'}), name='issue'),
    path('issue/<int:id>', view=SingleIssueViewSet.as_view({'get': 'get', 'patch': 'patch', 'delete': 'destroy'}),
         name='issue'),

    path('issue-details', view=IssueDetailsViewSet.as_view({'post': 'create', 'get': 'list'}), name='issue'),
    path('issue-details/<int:id>', view=SingleIssueDetailsViewSet.as_view({'patch': 'patch', 'delete': 'destroy'}),
         name='single_issue'),

    path('task-issue-resulation', view=TaskIssueResulationViewSet.as_view({'post': 'create', 'get': 'list'}),
         name='task_issue_resulation'),
    path('task-issue-resulation/<int:id>',
         view=SingleTaskIssueResulationViewSet.as_view({'patch': 'patch', 'delete': 'destroy'}),
         name='single_task_issue_resulation'),

    path('license', view=LicenseViewSet.as_view({'post': 'create', 'get': 'list'}), name='license'),
    path('license/<int:id>', view=SingleLicenseViewSet.as_view({'patch': 'patch', 'delete': 'destroy'}),
         name='single_license'),

    path('task-unfollow/<int:task_id>', view=TaskUnfollowViewSet.as_view({'delete': 'destroy'}), name='task_unfollow'),

    path('invite', view=SendInvitation.as_view({'post': 'create', 'get': 'get'}), name='send_invitation'),
    path('invite/<int:id>', view=SingleInvite.as_view({'patch': 'patch', 'delete': 'destroy'}), name='single_invitation'),
    path('registration-with-invitation', view=RegistrationWithInvitation.as_view({'post': 'create'}),
         name='registration_with_invitation'),
    path('accept-invitation', view=AcceptInvitation.as_view({'get': 'get'}), name='accept_invitation')

]
