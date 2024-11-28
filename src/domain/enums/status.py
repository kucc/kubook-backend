from enum import Enum


class AdminStatus(Enum):
    ACTIVE = True
    INACTIVE = False

    def __str__(self):
        desc = "활성화된" if self.value else "비활성화된"
        return f"현재 {desc} 관리자입니다."

    def __call__(self):
        return self.value


# 사용 예시
# print(str(AdminStatus.ACTIVE)) # 현재 활성화된 관리자입니다.
# print(AdminStatus.ACTIVE())  # True
# print(AdminStatus.INACTIVE())  # False


class BookStatus(Enum):
    AVAILABLE = True
    INAVILABLE = False

    def __str__(self):
        desc = "이용 가능" if self.value else "이용 불가능한"
        return f"현재 {desc} 한 도서입니다."

    def __call__(self):
        return self.value

class BookRequestStatus(Enum):
    WAITING = 0
    PURCHASED = 1
    CANCELED = 2
    REJECTED = 3

    def __str__(self):
        status_descriptions = {
            0: "해당 도서 구매 요청은 대기 중입니다.",
            1: "해당 도서 구매 요청은 구매 완료되었습니다.",
            2: "해당 도서 구매 요청은 신청자 취소되었습니다.",
            3: "해당 도서 구매 요청은 관리자 반려되었습니다."
        }
        return status_descriptions.get(self.value, "잘못된 도서 구매 요청 상태입니다.")

    def __call__(self):
        return self.value

class ReturnStatus(Enum):
    RETURNED = True
    NOT_RETURNED = False

    def __str__(self):
        desc = "반납 완료된" if self.value else "대출 중인"
        return f"현재 {desc} 도서입니다."

    def __call__(self):
        return self.value


class ExtendStatus(Enum):
    EXTENDED = True
    NOT_EXTENDED = False

    def __str__(self):
        desc = "연장된" if self.value else "연장되지 않은"
        return f"대출이 {desc} 상태입니다."

    def __call__(self):
        return self.value


def is_valid_enum_value(enum: Enum, status) -> bool:
    return status in enum._member_map.values()
