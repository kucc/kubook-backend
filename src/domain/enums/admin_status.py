from enum import Enum


class AdminStatus(Enum):
    ACTIVE = True
    INACTIVE = False

    def __init__(self, value):
        self.value = value

    def __str__(self):
        desc = "활성화된" if self.value else "비활성화된"
        return f"현재 {desc} 관리자입니다."


# 사용 예시
# print(AdminStatus.ACTIVE.value) # True
# print(AdminStatus.ACTIVE) # 현재 활성화된 관리자입니다.
