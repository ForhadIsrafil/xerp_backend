from rest_framework import serializers
from core.models import License, DepartmentModelPermission, DepartmentRoleModelPermission, Company
from project.models import Project, Goal, Task, TaskDetail, Issue, IssueDetail, TaskIssueResulation
from user.models import User, UserModelPermission
from user.serializers import UserSerializer
from django.db import transaction


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'name')

    def create(self, validated_data):
        initial_data = self.initial_data
        name = initial_data.get('name')
        user = self.context.get('request')

        company = Company._create_company(name, user_id=user.user.id)
        return company


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'start_date', 'end_date', 'text', 'name', 'is_active', 'enabled', 'created_at')

    @transaction.atomic
    def create(self, valid_data):
        initial_data = self.initial_data
        text = initial_data['text']
        start_date = initial_data.get('start_date')
        end_date = initial_data.get('end_date')
        request = self.context.get('request')
        name = initial_data['name']
        company = initial_data['company']

        project = Project(name=name, text=text, start_date=start_date, end_date=end_date, updated_by_id=request.user.id,
                          company_id=company)
        project.save()
        return project

    def validate(self, data):
        data = super(ProjectSerializer, self).validate(data)
        return data

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['updated_by'] = UserSerializer(instance.updated_by).data
        return response


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ('id', 'details', 'project', 'start_date', 'end_date', 'name', 'created_at', 'enabled')

    @transaction.atomic
    def create(self, valid_data):
        initial_data = self.initial_data
        project_id = initial_data.get('project')
        start_date = initial_data.get('start_date')
        end_date = initial_data.get('end_date')
        user = self.context.get('request')
        name = initial_data.get('name')
        details = initial_data.get('details')

        goal = Goal(name=name, start_date=start_date, end_date=end_date, project_id=project_id,
                    details=details, updated_by_id=user.user.id)
        goal.save()
        return goal

    def validate(self, data):
        data = super(GoalSerializer, self).validate(data)
        return data

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['project'] = ProjectSerializer(instance.project).data
        response['updated_by'] = UserSerializer(instance.updated_by).data
        return response


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'details', 'status', 'priority', 'goal', 'owner', 'start_date', 'end_date', 'name')

    @transaction.atomic
    def create(self, valid_data):
        initial_data = self.initial_data
        goal = initial_data.get('goal')
        owner = initial_data.get('owner')
        start_date = initial_data.get('start_date')
        end_date = initial_data.get('end_date')
        name = initial_data.get('name')
        user = self.context.get('request')
        details = initial_data.get('details')

        task = Task(name=name, details=details, goal_id=goal, owner_id=owner, start_date=start_date, end_date=end_date,
                    updated_by_id=user.user.id)
        task.save()
        return task

    def validate(self, data):
        data = super(TaskSerializer, self).validate(data)
        return data

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['goal'] = GoalSerializer(instance.goal).data
        response['updated_by'] = UserSerializer(instance.updated_by).data
        response['owner'] = UserSerializer(instance.owner).data
        return response


class TaskDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskDetail
        fields = ('id', 'task', 'comment', 'path')
        extra_kwargs = {
            'attachment': {'write_only': True}}

    @transaction.atomic
    def create(self, valid_data):
        initial_data = self.initial_data
        task = initial_data.get('task')
        comment = initial_data.get('comment')
        path = initial_data.get('path')
        user = self.context.get('request')
        task_detail = TaskDetail(task_id=task, comment=comment, path=path, updated_by_id=user.user.id)
        task_detail.save()
        return task_detail

    def validate(self, data):
        data = super(TaskDetailsSerializer, self).validate(data)
        return data


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ('id', 'title', 'description', 'path', 'classification', 'enabled',
                  'task', 'project', 'company_id', 'assigned_to', 'target_date', 'created_at')
        extra_kwargs = {
            'attachment': {'write_only': True}}

    @transaction.atomic
    def create(self, valid_data):
        initial_data = self.initial_data
        title = initial_data.get('title')
        description = initial_data.get('description')
        path = initial_data.get('path')
        classification = initial_data.get('classification')
        task = initial_data.get('task')
        project = initial_data.get('project')
        target = initial_data.get('target_date')
        user = self.context.get('request')
        user_details = User.objects.get(is_active=True, id=user.user.id)
        company = user_details.company_id
        assigned_to = initial_data.get('assigned_to')

        issue = Issue(title=title, description=description, classification=classification, task_id=task,
                      project_id=project, path=path, updated_by_id=user_details.id, company_id=company,
                      target_date=target, assigned_to=assigned_to)
        issue.save()
        return issue

    def validate(self, data):
        data = super(IssueSerializer, self).validate(data)
        return data

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['project'] = ProjectSerializer(instance.project).data
        response['task'] = TaskSerializer(instance.task).data
        response['updated_by'] = UserSerializer(instance.updated_by).data
        response['assigned_to'] = UserSerializer(instance.assigned_to).data
        return response


class IssueDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueDetail
        fields = ('id', 'issue', 'comment')
        extra_kwargs = {
            'attachment': {'write_only': True}}

    @transaction.atomic
    def create(self, valid_data):
        print(valid_data)
        initial_data = self.initial_data
        issue = initial_data.get('issue')
        comment = initial_data.get('comment')
        user = self.context.get('request')
        user_details = User.objects.get(is_active=True, id=user.user)
        issue_details = IssueDetail(issue_id=issue, comment=comment, updated_by_id=user_details.id)
        issue_details.save()
        return issue_details

    def validate(self, data):
        data = super(IssueDetailSerializer, self).validate(data)
        return data


class TaskIssueResulationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskIssueResulation
        fields = ('id', 'task', 'comment', 'path', 'updated_by')
        extra_kwargs = {
            'attachment': {'write_only': True}}

    @transaction.atomic
    def create(self, valid_data):
        initial_data = self.initial_data
        task = initial_data.get('task')
        comment = initial_data.get('comment')
        path = initial_data.get('path')
        user = self.context.get('request')

        issue_resulation = TaskIssueResulation(task_id=task, comment=comment, path=path,
                                               updated_by_id=user.user.id)
        issue_resulation.save()
        return issue_resulation

    def validate(self, data):
        data = super(TaskIssueResulationSerializer, self).validate(data)
        return data


class LicenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = License
        fields = ('id', 'company', 'model')

    @transaction.atomic
    def create(self, valid_data):
        initial_data = self.initial_data
        company = initial_data.get('company')
        model = initial_data.get('model')
        license = License(company_id=company, model=model)
        license.save()
        return license

    def validate(self, data):
        data = super(LicenseSerializer, self).validate(data)
        return data
