from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy import select, update, delete
from fastapi import status, HTTPException
from sqlalchemy.orm import Session
from admin.schemas import *
from models import *

# Get the list of items


def get_list(model, current_user, db: Session, ):
    try:
        result = db.scalars(select(model).order_by(model.updated_at)).all()
        if result == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Unexpected error occurred during update: {str(e)}")
    return result


# Get the item by ID
def get_item(model, index: int, current_user, db: Session):
    stmt = select(model).where((model.id == index))
    try:
        result = db.scalar(stmt)
        if result == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Unexpected error occurred during update: {str(e)}")

    return result


# CREATE
def create_item(model, req_data, current_user, db: Session):

    try:
        item = model(**req_data.dict())
        db.add(item)
        db.commit()
        db.refresh(item)

        print(item.__dict__)
        return item
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail=f"Fail to create the new {model.__name__} item. {str(e)}")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Unexpected error occurred: {str(e)}")


# update
def update_item(model, req_data, index: int, current_user, db: Session):

    try:
        item = get_item(model, index, db)
        if item == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
        item_dict = item.__dict__
        data = req_data.dict()

        for key in data:
            if key in item_dict:
                if isinstance(data[key], type(item_dict[key])):
                    setattr(item, key, data[key])
                else:
                    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                        detail=f"Invalid value type for column '{key}'.")

        db.add(item)
        db.commit()
        db.refresh(item)
        return item
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail=f"Duplicate category_code or category_names are not allowed.: {str(e)}")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Unexpected error occurred during update: {str(e)}")

# delete


def delete_item(model, index: int, current_user, db: Session):
    item = get_item(model, index, db)
    if item == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    stmt = (update(model).where(model.id == index).values(is_valid=False))
    try:
        db.execute(stmt)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Unexpected error occurred during delete: {str(e)}")

# delete for dba


def delete_item_dba(model, index: int, current_user, db: Session):
    item = get_item(model, index, db)
    if item == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    stmt = (delete(model).where(model.id == index))
    try:
        db.execute(stmt)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Unexpected error occurred during delete: {str(e)}")
