from django.db import models
from common_utils.base_entity import BaseEntityBasicAbstract, NameAbstract
from django.apps import apps


class Project(BaseEntityBasicAbstract, NameAbstract):
    company = models.ForeignKey('core.Company', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    text = models.TextField(null=True, blank=True)
    enabled = models.BooleanField(default=True)
    updated_by = models.ForeignKey('user.User', on_delete=models.DO_NOTHING)

    def as_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "updated_by_id": self.updated_by_id,
            "text": self.text,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "enabled": self.enabled
        }

    def with_tasks(self):
        goals = Goal.objects.filter(is_active=True, project_id=self.id).values_list('pk', flat=True)
        tasks = [t.for_list() for t in Task.objects.filter(is_active=True, goal_id__in=goals).order_by('-id')]
        return {
            "id": self.id,
            "name": self.name,
            "tasks": tasks
        }


class Goal(BaseEntityBasicAbstract, NameAbstract):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    details = models.TextField(null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    visibility = models.BooleanField(default=True)  # Internal organization can all time . But if client will see or not
    enabled = models.BooleanField(default=True)
    updated_by = models.ForeignKey('user.User', on_delete=models.DO_NOTHING)

    def as_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "updated_by_id": self.updated_by_id,
            "details": self.details,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "project": self.project_id
        }


class Task(BaseEntityBasicAbstract, NameAbstract):
    STATUS_CHOICES = (
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Closed', 'Closed')
    )
    PRIORITY_CHOICES = (
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low')
    )
    start_date = models.DateField()
    end_date = models.DateField()
    details = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Open')  # Open, Close, Pending, To be used
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='Low')  # Medium , High , Low
    enabled = models.BooleanField(default=True)
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE)
    owner = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='owner', null=True, blank=True)
    updated_by = models.ForeignKey('user.User', on_delete=models.DO_NOTHING)

    def as_json(self):
        User = apps.get_model('user', 'User')
        try:
            user_instance = User.objects.get(id=self.updated_by_id, is_active=True)
        except User.DoesNotExist:
            user_instance.full_name = 'Deleted User'

        try:
            owner_instance = User.objects.get(id=self.owner_id, is_active=True)
        except User.DoesNotExist:
            owner_instance.full_name = 'Not Assigned'

        comments = [i.as_json() for i in TaskDetail.objects.filter(task_id=self.id, is_active=True)]
        return {
            "id": self.id,
            "name": self.name,
            "created_by": user_instance.as_json(),
            "details": self.details,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "goal": self.goal_id,
            "owner": owner_instance.as_json(),
            "comments": comments,
            "created_at": self.created_at,
            "priority": self.priority,
            "status": self.status
        }

    def for_list(self):
        goal = Goal.objects.get(id=self.goal_id, is_active=True)
        return {
            "id": self.id,
            "name": self.name,
            "project_id": goal.project_id
        }


class TaskDetail(BaseEntityBasicAbstract):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    comment = models.TextField()
    path = models.CharField(max_length=150, null=True, blank=True)
    updated_by = models.ForeignKey('user.User', on_delete=models.DO_NOTHING)

    def as_json(self):
        User = apps.get_model('user', 'User')
        try:
            user_instance = User.objects.get(id=self.updated_by_id, is_active=True)
        except User.DoesNotExist:
            user_instance.full_name = 'Deleted User'
        return {
            'id': self.id,
            'task_id': self.task_id,
            'comment': self.comment,
            'created_by': user_instance.as_json(),
            'created_at': self.created_at
        }


class TaskFollower(BaseEntityBasicAbstract):  # Many to Many
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='follower_user')


class Issue(BaseEntityBasicAbstract):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    path = models.CharField(max_length=150, null=True, blank=True)
    target_date = models.DateField(null=True, blank=True)
    visibility = models.BooleanField(default=True)  # Internal organization can all time . But if client will see or not
    enabled = models.BooleanField(default=True)
    classification = models.CharField(max_length=255, null=True, blank=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    updated_by = models.ForeignKey('user.User', on_delete=models.DO_NOTHING)
    assigned_to = models.ForeignKey('user.User', on_delete=models.DO_NOTHING, related_name='issue_assigned', null=True, blank=True)
    company = models.ForeignKey('core.Company', on_delete=models.CASCADE)

    def as_json(self):
        User = apps.get_model('user', 'User')
        try:
            user_instance = User.objects.get(id=self.updated_by_id, is_active=True)
        except User.DoesNotExist:
            user_instance.full_name = 'Deleted User'

        comments = [i.as_json() for i in IssueDetail.objects.filter(issue_id=self.id)]
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'created_by': user_instance.as_json(),
            'task_id': self.task_id,
            'project_id': self.project_id,
            'comments': comments,
            'created_at': self.created_at
        }


class IssueDetail(BaseEntityBasicAbstract):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    comment = models.TextField()
    path = models.CharField(max_length=150, null=True, blank=True)
    updated_by = models.ForeignKey('user.User', on_delete=models.DO_NOTHING)

    def as_json(self):
        User = apps.get_model('user', 'User')
        try:
            user_instance = User.objects.get(id=self.updated_by_id, is_active=True)
        except User.DoesNotExist:
            user_instance.full_name = 'Deleted User'
        return {
            'id': self.id,
            'issue_id': self.issue_id,
            'comment': self.comment,
            'created_by': user_instance.as_json(),
            'created_at': self.created_at
        }


class TaskIssueResulation(BaseEntityBasicAbstract):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    comment = models.TextField()
    path = models.CharField(max_length=150, null=True, blank=True)
    updated_by = models.ForeignKey('user.User', on_delete=models.DO_NOTHING)
