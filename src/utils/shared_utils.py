from datetime import date

from fastapi import HTTPException, status
from sqlalchemy import and_, select
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound


def get_admin_status(user_id: int, db: Session) -> bool:
    """
    Check if the user with the given user_id is an admin and return their admin status.

    Args:
        user_id (int): The ID of the user to check
        db (Session): SQLAlchemy database session

    Returns:
        bool: True if the user is an active admin, False otherwise

    Raises:
        HTTPException:
            - 404: User not found
            - 500: Unexpected database error
    """
    from repositories.models import User

    if not isinstance(user_id, int) or user_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID"
        )

    try:
        stmt = select(User).where(and_(User.id == user_id, User.is_deleted == False))
        user = db.execute(stmt).scalar_one_or_none()

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        if not user.admin:
            return False

        # Get the most recent admin record
        latest_admin = max(user.admin, key=lambda admin: admin.created_at, default=None)
        if latest_admin is None:
            return False

        # Check admin status conditions
        is_active_admin = (
            not latest_admin.is_deleted and
            latest_admin.admin_status and
            latest_admin.expiration_date >= date.today()
        )

        return is_active_admin

    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        ) from NoResultFound
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error while checking admin status: {str(e)}"
        ) from e

def calculate_overdue_days(due_date: date) -> int:
    today = date.today()
    overdue = (today - due_date).days

    return max(overdue, 0)
