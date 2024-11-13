from enum import Enum


class BookCategoryStatus(Enum):
    A = ("인공지능", "Artificial Intelligence 관련 분야입니다.")
    B = ("데이터 분석", "Data Analysis 관련 분야입니다.")
    D = ("디자인", "Design 관련 분야입니다.")
    G = ("게임", "Game Development 관련 분야입니다.")
    H = ("하드웨어", "Hardware 관련 분야입니다.")
    L = ("언어", "Language 관련 분야입니다.")
    M = ("수학/통계", "Mathematics/Statistics 관련 분야입니다.")
    P = ("앱", "App Development 관련 분야입니다.")
    T = ("이론", "Theoretical 분야입니다.")
    W = ("웹", "Web Development 관련 분야입니다.")
    Z = ("기타", "Other 관련 분야입니다.")

    def __init__(self, category, description):
        self.category = category
        self.description = description

    def __str__(self):
        return self.category
