# Routes

이 폴더는 FastAPI 라우트(엔드포인트)를 정의합니다.

## 구조

- `endpoints/`: 각 기능별 라우터 파일
- `request/`: 요청 모델 (있는 경우)
- `response/`: 응답 모델 (있는 경우)

## 엔드포인트 추가 방법

1. `endpoints/` 폴더에 새 파일을 만듭니다.
2. FastAPI `APIRouter`를 사용하여 라우트를 정의합니다.
3. `__init__.py`에서 새 라우터를 등록합니다.

## 팁

- 경로 매개변수와 쿼리 매개변수를 명확히 구분하세요.
- 적절한 HTTP 메서드를 사용하세요 (GET, POST, PUT, DELETE 등).
- 응답 모델을 정의하여 API 문서화를 개선하세요.