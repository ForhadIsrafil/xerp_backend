from enum import Enum


class RoleEnum(Enum):
    MANAGER = "Manager"
    STAFF = "Staff"
    ACCOUNTANT = "Accountant"
    ADMIN = "Admin"
    SUPER_ADMIN = "Super Admin"

    @classmethod
    def get_all(cls):
        return [
            cls.MANAGER.value,
            cls.STAFF.value,
            cls.ACCOUNTANT.value,
            cls.ADMIN.value,
            cls.SUPER_ADMIN.value
        ]
