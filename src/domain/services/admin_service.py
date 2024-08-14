from typing import Any, Dict

from admin.schemas import *
from fastapi import HTTPException, status
from models import *
from sqlalchemy import delete, select, update
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session


# Get the list of items
def get_list(model, db: Session):
    stmt = select(model).where((model.is_valid == True)).order_by(model.updated_at)
    try:
        result = db.scalars(stmt).all()
        if result == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Unexpected error occurred during retrieve: {str(e)}")
    return result


# Get the item by ID
def get_item(model, index: int, db: Session):
    stmt = select(model).where((model.id == index) and (model.is_valid == True))
    try:
        result = db.execute(stmt).scalar_one()
    except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Item {index} not found")
    except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Unexpected error occurred during retrieve: {str(e)}")
    
    return result


# CREATE
def create_item(model, req_data, db:Session):    
    item = model(**req_data.dict())

    try:
        db.add(item)
        db.flush()
            
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail=f"Integrity Error occurred during create the new {model.__name__} item. {str(e)}")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Unexpected error occurred: {str(e)}")
    else :
        db.commit()
        db.refresh(item)
        return item

# update
def update_item(model, index:int, req_data, db:Session):
    item = get_item(model, index, db)

    try:
        current_item = item.__dict__
        if type(req_data) != dict :
            new_item = req_data.dict()
        else: new_item = req_data

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
                        detail=f"Integrity Error occurred during update the new {model.__name__} item.: {str(e)}")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Unexpected error occurred during update: {str(e)}")
    else :
        db.commit()
        db.refresh(item)
        return item


# delete
def delete_item(model, index:int, db:Session):
    item = get_item(model, index, db)
    stmt = (update(model).where(model.id == index).values(is_valid=False))
    try:
        db.execute(stmt)
        db.flush()

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Unexpected error occurred during delete: {str(e)}")
    else:
        db.commit()
    
# delete for dba
def delete_item_dba(model, index:int, db:Session):
    item = get_item(model, index, db)
    stmt = (delete(model).where(model.id==index))
    try:
        db.execute(stmt)
        db.flush()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Unexpected error occurred during delete: {str(e)}")
    else:
        db.commit()

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
