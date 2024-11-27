from sqlalchemy.orm import Session

from domain.schemas.user_schemas import DomainReqAdminDelUser
from repositories.models import User
from utils.crud_utils import delete_item


async def service_admin_delete_user(request: DomainReqAdminDelUser, db: Session):
    delete_item(User, request.user_id, db)
    return
