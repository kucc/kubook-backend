from sqlalchemy import and_
from sqlalchemy.orm import Session


# FILTERING LOGIC CODE 간소화 함수
def filters_by_query(query, model, q):
    for attr, value in q.__dict__.items():
        if value:
            if isinstance(value, str):
                query = query.filter(getattr(model, attr).ilike(f"%{value}%"))
            elif isinstance(value, (int, bool)):
                if attr != 'rating':
                    query = query.filter(getattr(model, attr) == value)
                else:
                    filter_expression = and_(value + 1 > getattr(model, attr), getattr(model, attr) >= value)
                    query = query.filter(filter_expression)
    return query


# order_by 간소화 함수
def orders_by_query(query, model, o):
    for attr, value in o.__dict__.items():
        try:
            if value is None:
                continue
            if value is False:
                query = query.order_by(getattr(model, attr).asc())
            if value is True:
                query = query.order_by(getattr(model, attr).desc())
        except AttributeError:
            continue
    return query


