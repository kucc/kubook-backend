# Core

이 폴더는 애플리케이션의 핵심 구성 요소와 설정을 포함합니다.

## 파일 설명

- `common.py`: 공통 유틸리티 함수와 상수
- `config.py`: 애플리케이션 설정 및 환경 변수
- `database.py`: 데이터베이스 연결 및 세션 관리
- `dependencies.py`: FastAPI 종속성 (의존성) 정의
- `logging_config.py`: 로깅 설정
- `ssh.py`: SSH 관련 유틸리티 (필요한 경우)

## 주의사항

- `config.py`에서 환경 변수를 올바르게 설정했는지 확인하세요.
- 데이터베이스 연결 문제 시 `database.py`를 확인하세요.