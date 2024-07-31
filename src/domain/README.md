# Domain

이 폴더는 비즈니스 로직과 데이터 모델을 포함합니다.

## 구조

- `schemas/`: Pydantic 모델 정의
- `services/`: 비즈니스 로직 구현

### Schemas

데이터 유효성 검사 및 직렬화를 위한 Pydantic 모델이 정의되어 있습니다.

### Services

비즈니스 로직을 구현하는 서비스 클래스가 포함되어 있습니다.

## 사용 팁

- 새로운 기능을 추가할 때 적절한 schema와 service를 생성하세요.
- schema와 service 간의 의존성을 주의깊게 관리하세요.