from enum import Enum


class AdminStatus(Enum):
    ACTIVE = ("ACTIVE", "현재 활성화된 관리자입니다.")
    INACTIVE = ("INACTIVE", "현재 비활성화된 관리자입니다.")
    SUSPENDED = ("SUSPENDED", "현재 정지된 관리자입니다.")

    def __init__(self, status, description):
        self.status = status
        self.description = description

    def __str__(self):
        return self.status

# 사용 예시
# print(AdminStatus.ACTIVE.admin_status) # ACTIVE
# print(AdminStatus.ACTIVE.description) # 현재 활성화된 관리자입니다.
