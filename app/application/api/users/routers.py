from typing import Annotated
from punq import Container
from fastapi import APIRouter, Depends, HTTPException, status

from application.api.schemas import SErrorMessage
from application.api.users.schemas import (
    SCreateUserIn,
    SCreateUserOut,
)
from domain.exceptions.base import ApplicationException
from logic.commands.users import (
    CreateUserCommand,
)
from logic.init import init_container
from logic.mediator.base import Mediator


user_router = APIRouter()


@user_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {"model": SCreateUserOut},
        status.HTTP_400_BAD_REQUEST: {"model": SErrorMessage},
    },
)
async def create_user(
    user_in: SCreateUserIn,
    container: Annotated[Container, Depends(init_container)],
) -> SCreateUserOut:
    """Create new user."""
    mediator: Mediator = container.resolve(Mediator)

    try:
        user, *_ = await mediator.handle_command(
            CreateUserCommand(
                phone=user_in.phone,
                username=user_in.username,
                password=user_in.password,
            )
        )
    except ApplicationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)

    return SCreateUserOut.from_entity(user)
