이 폴더 안에 있는 파일들은 database 연결을 도와주기 위한 파일들입니다.
이 파일들을 다른 파일에서 import할 경우 에러가 발생할 수 있습니다. 왜냐하면, 이 파일들이 다른 패키지들을 import하지 않은 경우가 있기 때문입니다. 이를 해결하기 위해서는 아래 코드를 활용해보세요! 주의사항: 어떤 파일에서 사용되지 않은 import가 있으면 꼭 제거해주세요! 항상 '꼭 필요한가?'를 생각하고 코딩하시면 좋습니다.


from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, DateTime, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

# Repositories

이 폴더는 데이터베이스 작업을 추상화하는 리포지토리 패턴을 구현합니다.

## 주요 파일

- `base.py`: 기본 리포지토리 클래스
- 각 엔티티별 리포지토리 (e.g., `book.py`, `user.py`)

## 사용 방법

1. `base.py`의 `BaseRepository`를 상속받아 새 리포지토리를 만듭니다.
2. CRUD 작업을 위한 메서드를 구현합니다.

## 팁

- 복잡한 쿼리는 여기서 구현하고, 서비스 레이어에서 호출하세요.
- 데이터베이스 트랜잭션을 적절히 관리하세요.