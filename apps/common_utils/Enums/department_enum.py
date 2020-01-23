from enum import Enum


class DepartmentNameEnum(Enum):
    # Owner of all apps, has ability to access any apps purchased, can't be deleted/modified
    OWNER = "AppsOwner"
    # Owner end

    # Project App default auto-generated departments, can be changed by user
    # Will be created when user purchase the Project App
    PROJECT_OWNER = "ProjectOwner"
    PROJECT_CONTRIBUTOR = "ProjectContributor"
    # Project App end

    # HR App default auto-generated departments, can be changed by user
    # Will be created when user purchase the HR App
    HR_HEAD = "HRHead"
    HR_RECRUIT = "HRRecruit"
    # HR App end

    # Sales App default auto-generated departments, can be changed by user
    # Will be created when user purchase the Sales App
    SALES_HEAD = "SalesHead"
    PAYMENT_RECEIVABLE = "PaymentReceivable"
    PAYMENT_PAYABLE = "PAYMENT_PAYABLE"
    REQUISITION = "REQUISITION"
    # Sales App end


    @classmethod
    def get_all(cls):
        return [
            cls.OWNER.value,
            cls.PROJECT_OWNER.value,
            cls.PROJECT_CONTRIBUTOR.value,
            cls.HR_HEAD.value,
            cls.HR_RECRUIT.value,
            cls.SALES_HEAD.value,
            cls.PAYMENT_RECEIVABLE.value,
            cls.PAYMENT_PAYABLE.value,
            cls.REQUISITION.value

        ]



# DEPARTMENT			Auto-generated, but user can change.
# ==================
# ID	NAME			CompanyId	(UNIQUE_KEY(ID,CompanyID),UNIQUE(CompanyId,Name))
# 1	PROJECT OWNER		1
# 2	PROJECT CONTRIBUTOR	1
# 3	HR HEAD			2
# 4	HR RECUITER		2
# 5	SALES			3
# 6	PAYMENT RECEIVABLE	3
# 7	PAYMENT PAYABLE		3
# 8	REQUISITION		    3