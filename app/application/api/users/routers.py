from typing import Annotated
from punq import Container
from fastapi import APIRouter, Depends, HTTPException, status

from application.api.schemas import SErrorMessage
from application.api.users.filters import GetUsersFilters
from application.api.users.schemas import (
    SChangeUsername,
    SCreateUserIn,
    SCreateUserOut,
    SGetUser,
    SGetUsersQueryResponse,
)
from domain.exceptions.base import ApplicationException
from logic.commands.users import (
    ChangeUsernameCommand,
    CreateUserCommand,
    DeleteUserCommand,
)
from logic.init import init_container
from logic.mediator.base import Mediator
from logic.queries.users import GetUserQuery, GetUsersQuery


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


@user_router.get(
    "/users/",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": SGetUsersQueryResponse},
        status.HTTP_400_BAD_REQUEST: {"model": SErrorMessage},
    },
)
async def get_users(
    container: Annotated[Container, Depends(init_container)],
    filters: GetUsersFilters = Depends(),
) -> SGetUsersQueryResponse:
    """Get all users from specified group."""
    mediator: Mediator = container.resolve(Mediator)

    try:
        users, count = await mediator.handle_query(
            GetUsersQuery(filters=filters.to_infrastructure_filters())
        )
    except ApplicationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)

    return SGetUsersQueryResponse(
        count=count,
        limit=filters.limit,
        offset=filters.offset,
        items=[SGetUser.from_entity(user) for user in users],
    )


@user_router.get(
    "/{user_oid}/",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": SGetUser},
        status.HTTP_400_BAD_REQUEST: {"model": SErrorMessage},
    },
)
async def get_user(
    user_oid: str,
    container: Annotated[Container, Depends(init_container)],
):
    """Get user user info."""
    mediator: Mediator = container.resolve(Mediator)
    try:
        user = await mediator.handle_query(GetUserQuery(user_oid=user_oid))
    except ApplicationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)

    return SGetUser.from_entity(user)


@user_router.put(
    "/{user_oid}/",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": SGetUser},
        status.HTTP_400_BAD_REQUEST: {"model": SErrorMessage},
    },
)
async def change_username(
    user_oid: str,
    user_in: SChangeUsername,
    container: Annotated[Container, Depends(init_container)],
) -> SGetUser:
    mediator: Mediator = container.resolve(Mediator)

    try:
        user, *_ = await mediator.handle_command(
            ChangeUsernameCommand(
                user_oid=user_oid,
                new_username=user_in.new_username,
            )
        )
    except ApplicationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)

    return SGetUser.from_entity(user)


@user_router.delete(
    "/{user_oid}/",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": SErrorMessage},
    },
)
async def delete_user(
    user_oid: str,
    container: Annotated[Container, Depends(init_container)],
) -> None:
    """Delete user."""
    mediator: Mediator = container.resolve(Mediator)

    try:
        await mediator.handle_command(DeleteUserCommand(user_oid=user_oid))
    except ApplicationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
