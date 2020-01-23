from enum import Enum


class ModelEnum(Enum):
    USER = "User"
    USERAWSBUCKETINFO = "UserAWSBucketInfo"
    COMPANY = "Company"
    PROJECT = "Project"
    GOAL = "Goal"
    TASK = "Task"
    TASKDETAIL = "TaskDetail"
    TASKFOLLOWER = "TaskFollower"
    ISSUE = "Issue"
    ISSUEDEATILS = "IssueDetails"
    TASKISSUERESULATION = "TaskIssueResulation"
    LICENSE = "License"
    DEPARTMENT = "Department"
    ROLE = "Role"

    @classmethod
    def get_all(cls):
        return [
            cls.USER.value,
            cls.USERAWSBUCKETINFO.value,
            cls.COMPANY.value,
            cls.PROJECT.value,
            cls.GOAL.value,
            cls.TASK.value,
            cls.TASKDETAIL.value,
            cls.TASKFOLLOWER.value,
            cls.ISSUE.value,
            cls.ISSUEDEATILS.value,
            cls.TASKISSUERESULATION.value,
            cls.LICENSE.value,
            cls.DEPARTMENT.value,
            cls.ROLE.value,
        ]

    @classmethod
    def get_project_app_all_model_names(cls):
        return [
            cls.USER.value,
            cls.USERAWSBUCKETINFO.value,
            cls.COMPANY.value,
            cls.PROJECT.value,
            cls.GOAL.value,
            cls.TASK.value,
            cls.TASKDETAIL.value,
            cls.TASKFOLLOWER.value,
            cls.ISSUE.value,
            cls.ISSUEDEATILS.value,
            cls.TASKISSUERESULATION.value,
            cls.LICENSE.value,
            cls.DEPARTMENT.value,
            cls.ROLE.value
        ]

    @classmethod
    def get_project_app_basic_model_names(cls):
        return [
            cls.COMPANY.value,
            cls.PROJECT.value
        ]
