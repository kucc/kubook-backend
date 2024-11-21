from datetime import datetime

from pydantic import BaseModel, Field


class ServiceDate(BaseModel):
    '''
      # 서비스 기간 예시
      service = ServiceDate(start_date="2024-01-01", end_date="2024-12-31")

      # 서비스 기간 내에 있는지 확인
      print(service.is_service_duration())  # True 또는 False

      # Pydantic 모델로부터 `start_datetime`과 `end_datetime`에 접근 가능
      print(service.start_datetime)  # 2024-01-01 00:00:00
      print(service.end_datetime)    # 2024-12-31 23:59:59
    '''

    start_date: str = Field(..., title="도서 서비스 시작일", description="도서 대출 및 도서 구매 신청 시작일", \
                             examples=["2024-01-01", "2024-01-01 00:00:00"])
    end_date: str = Field(..., title="도서 서비스 종료일",  description="도서 대출 및 도서 구매 신청 종료일", \
                          examples=["2024-12-31", "2024-12-31 23:59:59"])

    # @property를 사용하여 날짜 객체로 변환
    @property
    def start_datetime(self) -> datetime:
        return datetime.strptime(self.start_date, "%Y-%m-%d").replace(hour=0, minute=0, second=0)

    @property
    def end_datetime(self) -> datetime:
        return datetime.strptime(self.end_date, "%Y-%m-%d").replace(hour=23, minute=59, second=59)

    def is_service_duration(self) -> bool:
        """현재 시간 기준으로 서비스 기간 내에 있는지 확인"""
        current_datetime = datetime.now()
        return self.start_datetime <= current_datetime <= self.end_datetime

class ExtendSetting(BaseModel):
    extend_days : int = Field(..., title="연장일수", description="1회 연장 시 추가되는 대출 기간", \
                              examples=[3, 7, 10], ge=1)
    extend_max_count : int = Field(..., title="최대 연장횟수", description="대출 1건 당 가능한 연장 횟수", \
                                   examples=[3, 7, 10], ge=1)

class LoanSetting(BaseModel):
    loan_days : int = Field(..., title="대출 기간", description="1회 당 대출 기간", \
                              examples=[3, 7, 10], ge=1)
    loan_max_count : int = Field(..., title="대출 가능 권수", description="1회당 대출 가능 권수", \
                                   examples=[3, 7, 10], ge=1)

class BookRequestSetting(BaseModel):
    request_max_count : int = Field(..., title="도서 구매 최대 권수", description="1인당 구매 가능한 최대 도서 권수", \
                                   examples=[3, 7, 10], ge=1)
    request_max_price : int = Field(..., title="도서 구매 최대 가격", description="1인당 구매 가능한 최고 도서 가격", \
                                   examples=[3, 7, 10], ge=1)






