from project.decorators.permission_decorators import require_permissions
from user.serializers import UserSerializer
from core.models import ProjectAudit, GoalAudit, TaskAudit, TaskDetailAudit, License, DepartmentModelPermission, \
    DepartmentRoleModelPermission, Company, Department, Invitation, Role
from django.db.models import Q
from user.models import UserModelPermission, User

from apps.common_utils.Enums.model_enum import ModelEnum
from apps.common_utils.Enums.permission_enum import PermissionEnum
from core.models import Permission, Model
from apps.lib.get_object import get_object_or_404
from django.db import transaction
from rest_framework import status
from django.conf import settings
from lib.mailer import Mailer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import viewsets
from django.http import Http404
from project.models import Project, Goal, Task, TaskDetail, Issue, IssueDetail, TaskIssueResulation, TaskFollower
from .serializers import ProjectSerializer, GoalSerializer, TaskSerializer, TaskDetailsSerializer, IssueSerializer, \
    IssueDetailSerializer, TaskIssueResulationSerializer, LicenseSerializer

from user.models import UserRoleDepartment
import requests
import json


class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProjectSerializer

    @transaction.atomic
    def create(self, request, format=None):
        serializer = ProjectSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            # Saving audit log after project create
            project_audit = ProjectAudit(start_date=request.data.get('start_date'),
                                         end_date=request.data.get('end_date'),
                                         text=request.data.get('text'),
                                         name=request.data.get('name'),
                                         action=request.method,
                                         updated_by_id=request.user.id,
                                         is_active=True,
                                         enabled=True)
            project_audit.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        user = User.objects.get(id=self.request.user.id, is_active=True)

        project_audit = ProjectAudit(action=self.request.method,
                                     updated_by_id=self.request.user.id)
        project_audit.save()
        projects = Project.objects.filter(is_active=True, company_id=user.company_id).order_by('-id')
        if self.request.GET.get('search') is not None:
            search_query = self.request.GET.get('search')
            projects = projects.filter(Q(name__icontains=search_query) |
                                       Q(text__icontains=search_query) |
                                       Q(start_date__icontains=search_query) |
                                       Q(end_date__icontains=search_query))

        if self.request.GET.get('start') and self.request.GET.get('end') is not None:
            start = self.request.GET.get('start')
            end = self.request.GET.get('end')
            projects = projects.filter(Q(start_date__range=(start, end)) and
                                       Q(end_date__range=(start, end)))

        if self.request.GET.get('enabled') is not None:
            enable_query = self.request.GET.get('enabled')
            projects = projects.filter(Q(enabled=enable_query))

        return projects

    def get_serializer_context(self):
        return {'request': self.request}


class UserProjects(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProjectSerializer

    def get_object_or_404(self, model, look_up_for):
        try:
            return model.objects.get(pk=look_up_for)
        except:
            raise Http404

    def get_queryset(self):
        company_id = self.kwargs.get('company_id')
        company_instence = self.get_object_or_404(Company, company_id)
        projects = Project.objects.filter(company_id=company_instence.id, is_active=True).order_by('-id')
        if self.request.GET.get('search') is not None:
            search_query = self.request.GET.get('search')
            projects = projects.filter(Q(name__icontains=search_query) |
                                       Q(text__icontains=search_query) |
                                       Q(start_date__icontains=search_query) |
                                       Q(end_date__icontains=search_query))

        if self.request.GET.get('start') and self.request.GET.get('end') is not None:
            start = self.request.GET.get('start')
            end = self.request.GET.get('end')
            projects = projects.filter(Q(start_date__range=(start, end)) and
                                       Q(end_date__range=(start, end)))

        if self.request.GET.get('enabled') is not None:
            enable_query = self.request.GET.get('enabled')
            projects = projects.filter(Q(enabled=enable_query))

        return projects


class ProjectWithTasks(ViewSet):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = User.objects.get(id=request.user.id, is_active=True)
        projects = [p.with_tasks() for p in
                    Project.objects.filter(is_active=True, company_id=user.company_id).order_by('-id')]

        return Response(projects, status=status.HTTP_200_OK)


class SingleProjectViewSet(ViewSet):
    permission_classes = (IsAuthenticated,)

    def get(self, request, id):
        try:
            project_instance = Project.objects.get(id=id, is_active=True)
        except Project.DoesNotExist:
            raise Http404("Not Found")
        serializer = ProjectSerializer(project_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def patch(self, request, id):
        try:
            project_instance = Project.objects.get(is_active=True, id=id)
        except Project.DoesNotExist:
            raise Http404("Not Found")
        serializer = ProjectSerializer(project_instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            project_audit = ProjectAudit(start_date=request.data.get('start_date'),
                                         end_date=request.data.get('end_date'),
                                         text=request.data.get('text'),
                                         name=request.data.get('name'),
                                         action=request.method,
                                         updated_by_id=request.user.id,
                                         is_active=True,
                                         enabled=True)
            project_audit.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def destroy(self, request, id):
        try:
            project_instance = Project.objects.get(is_active=True, id=id)
        except Project.DoesNotExist:
            raise Http404("Not Found")
        project_instance.is_active = False
        project_instance.save()
        request.data['name'] = project_instance.name
        request.data['text'] = project_instance.text
        request.data['start_date'] = project_instance.start_date
        request.data['end_date'] = project_instance.end_date
        serializer = ProjectSerializer(project_instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            project_audit = ProjectAudit(action=request.method,
                                         updated_by_id=request.user.id)
            project_audit.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GoalViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = GoalSerializer

    @transaction.atomic
    def create(self, request):
        serializer = GoalSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            log_obj = GoalAudit(company_id=request.data.get('company'),
                                project_id=request.data.get('project'),
                                start_date=request.data.get('start_date'),
                                end_date=request.data.get('end_date'),
                                name=request.data.get('name'),
                                action=request.method,
                                updated_by_id=request.user.id,
                                is_active=True,
                                enabled=True)
            log_obj.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        user = User.objects.get(id=self.request.user.id, is_active=True)
        projects = Project.objects.filter(is_active=True, company_id=user.company_id).values_list('pk', flat=True)
        goals = Goal.objects.filter(is_active=True, project_id__in=projects).order_by('-id')
        if self.request.GET.get('search') is not None:
            search_query = self.request.GET.get('search')
            goals = goals.filter(Q(name__icontains=search_query) |
                                 Q(details__icontains=search_query) |
                                 Q(start_date__icontains=search_query) |
                                 Q(end_date__icontains=search_query))

        if self.request.GET.get('start') and self.request.GET.get('end') is not None:
            start = self.request.GET.get('start')
            end = self.request.GET.get('end')
            goals = goals.filter(Q(start_date__range=(start, end)) and
                                 Q(end_date__range=(start, end)))

        if self.request.GET.get('enabled') is not None:
            enable_query = self.request.GET.get('enabled')
            if enable_query is not '':
                goals = goals.filter(Q(enabled=enable_query))

        if self.request.GET.get('project') is not None:
            project_query = self.request.GET.get('project')
            goals = goals.filter(Q(project_id=project_query))

        log_obj = GoalAudit(action=self.request.method,
                            updated_by_id=self.request.user.id)
        log_obj.save()
        return goals

    def get_serializer_context(self):
        return {'request': self.request}


class ProjectGoals(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = GoalSerializer

    def get_queryset(self, *args, **kwargs):
        project_id = self.kwargs.get('project_id')
        try:
            project_instance = Project.objects.get(id=project_id, is_active=True)
        except Project.DoesNotExist:
            raise Http404("Not Found")
        goals = Goal.objects.filter(project_id=project_id, is_active=True).order_by('-id')
        return goals


class SingleGoalViewSet(ViewSet):
    permission_classes = (IsAuthenticated,)

    def get(self, request, id):
        try:
            goal_instance = Goal.objects.get(id=id, is_active=True)
        except Goal.DoesNotExist:
            raise Http404("Not Found")
        serializer = GoalSerializer(goal_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def patch(self, request, id):
        try:
            goal_instance = Goal.objects.get(id=id, is_active=True)
        except Goal.DoesNotExist:
            raise Http404("Not Found")
        serializer = GoalSerializer(goal_instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            log_obj = GoalAudit(company_id=request.data.get('company'),
                                project_id=request.data.get('project_id'),
                                start_date=request.data.get('start_date'),
                                end_date=request.data.get('end_date'),
                                name=request.data.get('name'),
                                action=request.method,
                                updated_by_id=request.user.id,
                                is_active=True,
                                enabled=True)
            log_obj.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def destroy(self, request, id):
        try:
            goal_instance = Goal.objects.get(id=id, is_active=True)
        except Goal.DoesNotExist:
            raise Http404("Not Found")
        goal_instance.is_active = False
        goal_instance.save()
        request.data['name'] = goal_instance.name
        request.data['details'] = goal_instance.details
        request.data['start_date'] = goal_instance.start_date
        request.data['end_date'] = goal_instance.end_date
        serializer = GoalSerializer(goal_instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            log_obj = GoalAudit(action=self.request.method,
                                updated_by_id=self.request.user.id)
            log_obj.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = TaskSerializer

    #@require_permissions(model_name='Task')
    @transaction.atomic
    def create(self, request):
        serializer = TaskSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            log_obj = TaskAudit(goal_id=request.data.get('goal'),
                                owner_id=request.data.get('owner'),
                                start_date=request.data.get('start_date'),
                                end_date=request.data.get('end_date'),
                                name=request.data.get('name'),
                                action=request.method,
                                updated_by_id=request.user.id,
                                is_active=True,
                                enabled=True,
                                status=True,
                                priority=True)
            log_obj.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #@require_permissions(model_name='Task')
    def get_queryset(self):
        user = User.objects.get(id=self.request.user.id, is_active=True)
        projects = Project.objects.filter(is_active=True, company_id=user.company_id).values_list('pk', flat=True)
        goals = Goal.objects.filter(is_active=True, project_id__in=projects).values_list('pk', flat=True)
        tasks = Task.objects.filter(is_active=True, goal_id__in=goals).order_by('-id')
        if self.request.GET.get('search') is not None:
            search_query = self.request.GET.get('search')
            tasks = tasks.filter(Q(name__icontains=search_query) |
                                 Q(details__icontains=search_query) |
                                 Q(start_date__icontains=search_query) |
                                 Q(end_date__icontains=search_query))

        if self.request.GET.get('start') and self.request.GET.get('end') is not None:
            start = self.request.GET.get('start')
            end = self.request.GET.get('end')
            tasks = tasks.filter(Q(start_date__range=(start, end)) and
                                 Q(end_date__range=(start, end)))

        if self.request.GET.get('status') is not None:
            tasks = tasks.filter(status=self.request.GET.get('status'))

        if self.request.GET.get('priority') is not None:
            tasks = tasks.filter(priority=self.request.GET.get('priority'))

        log_obj = TaskAudit(action=self.request.method,
                            updated_by_id=self.request.user.id)
        log_obj.save()
        return tasks

    def get_serializer_context(self):
        return {'request': self.request}


class GoalTasks(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = TaskSerializer

    def get_queryset(self, *args, **kwargs):
        goal_id = self.kwargs.get('goal_id')
        try:
            goal_instance = Goal.objects.get(id=goal_id, is_active=True)
        except Goal.DoesNotExist:
            raise Http404("Not Found")
        try:
            project_instance = Project.objects.get(id=goal_instance.project_id, is_active=True)
        except Project.DoesNotExist:
            raise Http404("Not Found")
        tasks = Task.objects.filter(goal_id=goal_id, is_active=True).order_by('-id')

        if self.request.GET.get('status') is not None:
            tasks = tasks.filter(status=self.request.GET.get('status'))

        if self.request.GET.get('priority') is not None:
            tasks = tasks.filter(priority=self.request.GET.get('priority'))

        return tasks


class SingleTaskViewSet(ViewSet):
    permission_classes = (IsAuthenticated,)

    def get(self, request, id):
        try:
            task_instance = Task.objects.get(id=id, is_active=True)
        except Task.DoesNotExist:
            raise Http404("Not Found")
        serializer = TaskSerializer(task_instance)
        return Response(task_instance.as_json(), status=status.HTTP_200_OK)

    @transaction.atomic
    def patch(self, request, id):
        try:
            task_instance = Task.objects.get(id=id, is_active=True)
        except Task.DoesNotExist:
            raise Http404("Not Found")
        serializer = TaskSerializer(task_instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            log_obj = TaskAudit(goal_id=request.data.get('goal'),
                                owner_id=request.data.get('owner'),
                                start_date=request.data.get('start_date'),
                                end_date=request.data.get('end_date'),
                                name=request.data.get('name'),
                                action=request.method,
                                updated_by_id=request.user.id,
                                is_active=True,
                                enabled=True,
                                status=True,
                                priority=True)
            log_obj.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def destroy(self, request, id):
        try:
            task_instance = Task.objects.get(id=id, is_active=True)
        except Task.DoesNotExist:
            raise Http404("Not Found")
        task_instance.is_active = False
        task_instance.save()
        request.data['name'] = task_instance.name
        request.data['details'] = task_instance.details
        request.data['start_date'] = task_instance.start_date
        request.data['end_date'] = task_instance.end_date
        serializer = TaskSerializer(task_instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            log_obj = TaskAudit(action=self.request.method,
                                updated_by_id=self.request.user.id)
            log_obj.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetailViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = TaskDetailsSerializer

    @transaction.atomic
    def create(self, request):
        serializer = TaskDetailsSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            log_obj = TaskDetailAudit(action=request.method,
                                      comment=request.data.get('comment'),
                                      path=request.data.get('path'),
                                      is_active=True)
            log_obj.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        log_obj = TaskDetailAudit(action=self.request.method)
        log_obj.save()
        return TaskDetail.objects.filter(is_active=True).order_by('-id')

    def get_serializer_context(self):
        return {'request': self.request}


class SingleTaskDetailViewSet(ViewSet):
    permission_classes = (IsAuthenticated,)

    @transaction.atomic
    def patch(self, request, id):
        try:
            task_detail_instance = TaskDetail.objects.get(id=id, is_active=True)
        except TaskDetail.DoesNotExist:
            raise Http404("Not Found")
        serializer = TaskDetailsSerializer(task_detail_instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            log_obj = TaskDetailAudit(action=request.method,
                                      comment=request.data.get('comment'),
                                      path=request.data.get('path'))
            log_obj.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def destroy(self, request, id):
        try:
            task_detail_instance = TaskDetail(id=id, is_active=True)
        except TaskDetail.DoesNotExist:
            raise Http404("Not Found")
        task_detail_instance.is_active = False
        task_detail_instance.save()
        request.data['comment'] = task_detail_instance.comment
        serializer = TaskDetailsSerializer(task_detail_instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            log_obj = TaskDetailAudit(action=self.request.method)
            log_obj.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IssueViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = IssueSerializer

    @transaction.atomic
    def create(self, request):
        serializer = IssueSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        user = User.objects.get(id=self.request.user.id)
        issues = Issue.objects.filter(is_active=True, company_id=user.company_id).order_by('-id')
        if self.request.GET.get('user') is not None:
            issues = issues.filter(updated_by=self.request.GET.get('user'))

        if self.request.GET.get('search') is not None:
            search_query = self.request.GET.get('search')
            issues = issues.filter(Q(title__icontains=search_query) |
                                   Q(description__icontains=search_query) |
                                   Q(target_date__icontains=search_query))

        if self.request.GET.get('start') and self.request.GET.get('end') is not None:
            start = self.request.GET.get('start')
            end = self.request.GET.get('end')
            issues = issues.filter(Q(target_date__range=(start, end)))

        if self.request.GET.get('enabled') is not None:
            enable_query = self.request.GET.get('enabled')
            if enable_query is not '':
                issues = issues.filter(Q(enabled=enable_query))

        return issues

    def get_serializer_context(self):
        return {'request': self.request}


class SingleIssueViewSet(ViewSet):
    permission_classes = (IsAuthenticated,)

    def get(self, request, id):
        try:
            issue_instance = Issue.objects.get(id=id, is_active=True)
        except Issue.DoesNotExist:
            raise Http404("Not Found")
        serializer = IssueSerializer(issue_instance)
        return Response(issue_instance.as_json(), status=status.HTTP_200_OK)

    @transaction.atomic
    def patch(self, request, id):
        try:
            issue_instance = Issue.objects.get(id=id, is_active=True)
        except Issue.DoesNotExist:
            raise Http404("Not Found")
        serializer = IssueSerializer(issue_instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def destroy(self, request, id):
        try:
            issue_instance = Issue.objects.get(id=id, is_active=True)
        except Issue.DoesNotExist:
            raise Http404("Not Found")
        issue_instance.is_active = False
        issue_instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class IssueDetailsViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = IssueDetailSerializer

    @transaction.atomic
    def create(self, request):
        request.user = request.user.id
        serializer = IssueDetailSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        return IssueDetail.objects.all().order_by('-id')

    def get_serializer_context(self):
        return {'request': self.request}


class SingleIssueDetailsViewSet(ViewSet):
    permission_classes = (IsAuthenticated,)

    @transaction.atomic
    def patch(self, request, id):
        issue_instance = get_object_or_404(IssueDetail, id)
        serializer = IssueDetailSerializer(issue_instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def destroy(self, request, id):
        issue_instance = get_object_or_404(IssueDetail, id)
        issue_instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TaskIssueResulationViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = TaskIssueResulationSerializer

    @transaction.atomic
    def create(self, request):
        serializer = TaskIssueResulationSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        return TaskIssueResulation.objects.all().order_by('-id')

    def get_serializer_context(self):
        return {'request': self.request}


class SingleTaskIssueResulationViewSet(ViewSet):
    permission_classes = (IsAuthenticated,)

    @transaction.atomic
    def patch(self, request, id):
        resulation_instance = get_object_or_404(TaskIssueResulation, id)
        serializer = TaskIssueResulationSerializer(resulation_instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def destroy(self, request, id):
        resulation_instance = get_object_or_404(TaskIssueResulation, id)
        resulation_instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LicenseViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = LicenseSerializer

    @transaction.atomic
    def create(self, request):
        serializer = LicenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        return License.objects.all().order_by('-id')

    def get_serializer_context(self):
        return {'request': self.request}


class SingleLicenseViewSet(ViewSet):
    permission_classes = (IsAuthenticated,)

    @transaction.atomic
    def patch(self, request, id):
        license_instance = get_object_or_404(License, id)
        serializer = LicenseSerializer(license_instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def destroy(self, request, id):
        license_instance = get_object_or_404(License, id)
        license_instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TaskUnfollowViewSet(ViewSet):
    permission_classes = (IsAuthenticated,)

    def destroy(self, request, task_id):
        task_follower_isnstance = TaskFollower.objects.filter(task_id=task_id, user_id=request.user.id).first()
        if task_follower_isnstance:
            task_follower_isnstance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class SendInvitation(ViewSet):
    permission_classes = (IsAuthenticated,)

    @transaction.atomic
    def create(self, request):
        department_id = request.data.get('department_id', None)
        email = request.data.get('email', None)
        role_id = request.data.get('role_id', None)
        if None in [department_id, email, role_id]:
            return Response({'error': 'Fields are can\'t be empty!'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.get(id=request.user.id, is_active=True)
        if user.username == email:
            return Response({'error': 'You can not send yourself invitation'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            dept_instance = Department.objects.get(id=department_id, company_id=user.company_id, is_active=True)
        except Department.DoesNotExist:
            return Response({'error': 'Department doesn\'t exist'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            role_instance = Role.objects.get(id=role_id, company_id=user.company_id, is_active=True)
        except Role.DoesNotExist:
            return Response({'error': 'Role doesn\'t exist'}, status=status.HTTP_400_BAD_REQUEST)

        invitation = Invitation(email=email, role_id=role_id, department_id=department_id)
        invitation.save()

        # existing user

        user_instance = User.objects.filter(username=email, is_active=True).first()

        if user_instance is not None:
            invitation_link = settings.ACCEPT_INVITATION_URL + '?email=' + email + '&department=' + str(department_id)
            subject = 'xERP: Accept the invitation.'
            email_body = "<strong> Welcome to xERP! </strong> " \
                         "<p>You are invited on a department. Here is the invitation link given below. Please use this link to registration/accept." \
                         "</p> <a href=" + invitation_link + ">click here</a>  <p> Thank you </p>"
        else:
            invitation_link = settings.INVITATION_URL + '?email=' + email + '&department=' + str(department_id)
            subject = 'xERP: Register with invitation.'
            email_body = "<strong> Welcome to xERP! </strong> " \
                         "<p>You are invited for regitstration. Here is the invitation link given below. Please use this link to registration/accept." \
                         "</p> <a href=" + invitation_link + ">click here</a>  <p> Thank you </p>"

        # sending Mail
        mailer = Mailer()
        response = mailer.send_email(recipient=email, subject=subject, html_message=email_body)

        if not response:
            err_response = {'error': 'Email sending process failed. Please try again'}
            return Response(err_response, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_201_CREATED)

    def get(self, request):
        user = User.objects.get(id=request.user.id, is_active=True)
        depts = Department.objects.filter(company_id=user.company_id, is_active=True).values_list('pk', flat=True)
        return Response(
            [i.as_json() for i in Invitation.objects.filter(department_id__in=depts, is_active=True).order_by('-id')],
            status=status.HTTP_200_OK)


class SingleInvite(ViewSet):
    permission_classes = (IsAuthenticated,)

    @transaction.atomic
    def patch(self, request, id):
        invite_instance = get_object_or_404(Invitation, id)
        if request.data.get('department_id') is not None:
            invite_instance.department_id = request.data.get('department_id')
        if request.data.get('role_id') is not None:
            invite_instance.role_id = request.data.get('role_id')
        invite_instance.save()
        return Response(invite_instance.as_json(), status=status.HTTP_200_OK)

    @transaction.atomic
    def destroy(self, request, id):
        invite_instance = get_object_or_404(Invitation, id)
        invite_instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RegistrationWithInvitation(ViewSet):
    permission_classes = (AllowAny,)

    @transaction.atomic
    def create(self, request):
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        phone_code = request.data.get('phone_code', None)
        cellphone = request.data.get('cellphone', None)
        department = request.data.get('department', None)

        if None in [email, password, cellphone]:
            return Response({'error': 'Credentials not given properly. '},
                            status=status.HTTP_400_BAD_REQUEST)

        invitation_instance = Invitation.objects.filter(email=email, department_id=department, is_active=True).last()
        if invitation_instance is not None:

            # user check
            user_instance = User.objects.filter(username=email, is_active=True).first()

            if user_instance is not None:
                Response({'error': 'You already registered on the system. Try accepting the invitation.'},
                         status=status.HTTP_400_BAD_REQUEST)
            else:
                # time to get company_instance
                company_instance = invitation_instance.department.company

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
                        "user[country_code]": phone_code
                    }
                    create_user_response = requests.post(url, data=data, headers=headers)
                    authy_response = json.loads(create_user_response.content.decode('utf-8'))
                    # ========================= AUTHY END =======================

                    user_instance = User.objects.filter(id=serializer.data['id']).first()
                    user_instance.authy_id = authy_response['user']['id']
                    user_instance.company_id = company_instance.id
                    user_instance.save()

                    user_role_instance = UserRoleDepartment(user_id=user_instance.id,
                                                            role_id=invitation_instance.role_id,
                                                            department_id=invitation_instance.department_id)
                    user_role_instance.save()

                    # setting up PERMISSION start
                    # @ ALL department ALL Model View Permission FOR DepartmentModelPermission

                    get_project_app_all_model_names = ModelEnum.get_project_app_basic_model_names()
                    view_permission_obj = Permission.objects.get(name=PermissionEnum.VIEW.value)
                    for model_name in get_project_app_all_model_names:
                        model_instances = Model.objects.filter(name=model_name).first()
                        if model_instances is not None:
                            user_model_instance = UserModelPermission(
                                user_id=user_instance.id,
                                model_id=model_instances.id,
                                permission_id=view_permission_obj.id)
                            user_model_instance.save()
                        else:
                            return Response({'error': model_name + ' Model not found.'},
                                            status=status.HTTP_400_BAD_REQUEST)

                    # setting up PERMISSION end

                    email_res = User.send_signup_mail(email)
                    if email_res != True:
                        return Response(email_res, status=status.HTTP_400_BAD_REQUEST)
                    invitation_instance.delete()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'error': 'No invitation was found for the provided email'},
                            status=status.HTTP_400_BAD_REQUEST)


class AcceptInvitation(ViewSet):
    permission_classes = (IsAuthenticated,)

    @transaction.atomic
    def get(self, request):
        email = self.request.data.get('email')
        department = self.request.data.get('department')

        if None in [email, department]:
            return Response({'error': 'Please provide email & department.'},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            invitation_instance = Invitation.objects.filter(email=email, department_id=department,
                                                            is_active=True).last()
            if invitation_instance is not None:
                user_instance = User.objects.filter(id=self.request.user.id, username=email, is_active=True).first()
                if user_instance is None:
                    return Response({'error': 'Invalid email'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    user_role_instance = UserRoleDepartment(user_id=user_instance.id,
                                                            role_id=invitation_instance.role_id,
                                                            department_id=invitation_instance.department_id)
                    user_role_instance.save()
                    invitation_instance.delete()
                    return Response(status=status.HTTP_200_OK)
            else:
                return Response({'error': 'No invitation was found'}, status=status.HTTP_400_BAD_REQUEST)