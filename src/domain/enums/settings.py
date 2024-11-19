from datetime import datetime
from enum import Enum

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

    # 시작일과 종료일을 문자열로 받아서 필드로 설정
    start_date: str = Field(..., alias='START_DATE')  # "2024-01-01" 형식
    end_date: str = Field(..., alias='END_DATE')  # "2024-12-31" 형식

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

    class Config:
        # Pydantic에서 alias를 사용하여, 필드 이름이 대문자로 되도록 설정
        allow_population_by_field_name = True

class ExtendSetting(Enum):
    EXTEND_DAY = 7
    EXTEND_MAX_COUNT = 1








