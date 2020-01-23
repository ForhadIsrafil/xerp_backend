from enum import Enum


class AppEnum(Enum):
    PROJECT = "Project"
    HR = "HR"
    ACCOUNTING = "Accounting"


    @classmethod
    def get_all(cls):
        return [
            cls.PROJECT.value,
            cls.HR.value,
            cls.ACCOUNTING.value
        ]
