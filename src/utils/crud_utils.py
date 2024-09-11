from typing import Any, Dict
from fastapi import HTTPException, status
from sqlalchemy import delete, select, update
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session


# 여러 개의 데이터 조회
def get_list(model, db: Session):
    stmt = select(model).where(model.is_deleted == False).order_by(model.updated_at)
    try:
        result = db.scalars(stmt).all()
        if result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occurred during retrieve: {str(e)}"
        ) from e
    return result


# ID를 이용한 하나의 데이터 조회
def get_item(model, index: int, db: Session):
    stmt = select(model).where((model.id == index) and (not model.is_deleted))
    try:
        result = db.execute(stmt).scalar_one()
    except NoResultFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Item {index} not found") from e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Unexpected error occurred during retrieve: {str(e)}") from e

    return result


# column 이름과 value 값을 이용하여 filtering
def get_item_by_column(*, model, columns: Dict[str, Any], db: Session):
    stmt = select(model)

    for column_name, value in columns.items():
        if value is not None:
            if hasattr(model, column_name):
                stmt = stmt.where(getattr(model, column_name) == value)
            else:
                return None

    result = db.scalars(stmt).all()

    return result


# 데이터 생성
def create_item(model, req_data, db: Session):
    item = model(**req_data.dict())

    try:
        db.add(item)
        db.flush()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail=f"Integrity Error occurred during creating the new {model.__name__} item: {str(e)}") from e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Unexpected error occurred: {str(e)}") from e

    db.refresh(item)

    return item  # 커밋은 호출하는 곳에서 처리하도록 리턴


# 데이터 수정
def update_item(model, index: int, req_data, db: Session):
    item = get_item(model, index, db)

    try:
        current_item = item.__dict__
        if not isinstance(req_data, dict):
            new_item = req_data.dict()
        else:
            new_item = req_data

        for key, value in new_item.items():
            if value is not None and key in current_item:
                if isinstance(value, type(current_item[key])):
                    setattr(item, key, value)
                else:
                    raise HTTPException(
                        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        detail=f"Invalid value type for column {key}. Expected {type(current_item[key])}, got {type(value)}."
                    )
        db.add(item)
        db.flush()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail=f"Integrity Error occurred during update the new {model.__name__} item.: {str(e)}") from e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Unexpected error occurred during update: {str(e)}") from e
    db.refresh(item)

    return item  # 커밋은 호출하는 곳에서 처리하도록 리턴


# ID로 하나의 데이터 삭제(is_deleted = False)
def delete_item(model, index: int, db: Session):
    stmt = (update(model).where(model.id == index).values(is_deleted=True))
    try:
        db.execute(stmt)
        db.flush()

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Unexpected error occurred during delete: {str(e)}") from e
    else:
        db.commit()


# 여러 개의 데이터 삭제(is_deleted = False)
def delete_items(model, ids: list[int], db: Session):
    stmt = (
        update(model)
        .where(model.id.in_(ids))
        .values(is_deleted=True)
    )
    try:
        result = db.execute(stmt)
        db.flush()
        if result.rowcount == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="No items found for the provided IDs.")
    except Exception as e:
        db.rollback()  # 예외 발생 시 롤백
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Unexpected error occurred during delete: {str(e)}") from e
    else:
        db.commit()


# 데이터 완전 삭제 (개발 과정에서만 사용)
def delete_item_dba(model, index: int, db: Session):
    stmt = (delete(model).where(model.id == index))
    try:
        db.execute(stmt)
        db.flush()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Unexpected error occurred during delete: {str(e)}") from e
    else:
        db.commit()
