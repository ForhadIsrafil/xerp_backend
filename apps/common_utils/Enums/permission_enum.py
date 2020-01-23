from enum import Enum


class PermissionEnum(Enum):
    VIEW = "View"
    CREATE = "Create"
    UPDATE = "Update"
    DELETE = "Delete"
    UPLOAD = "Upload"
    DOWNLOAD = "Download"
    REPORT = "Report"


    @classmethod
    def get_all(cls):
        return [
            cls.VIEW.value,
            cls.CREATE.value,
            cls.UPLOAD.value,
            cls.DOWNLOAD.value,
            cls.UPDATE.value,
            cls.DELETE.value,
            cls.REPORT.value
        ]
