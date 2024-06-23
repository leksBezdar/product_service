from dataclasses import dataclass

import bcrypt

from domain.entities.users import User, VerificationToken
from domain.values.users import Email, Password, Username
from infrastructure.repositories.users.base import (
    BaseUserRepository,
    BaseVerificationTokenRepository,
)
from infrastructure.repositories.groups.base import (
    BaseGroupRepository,
)
from logic.commands.base import BaseCommand, CommandHandler
from logic.exceptions.users import (
    InvalidCredentialsException,
    TokenNotFoundException,
    UserAlreadyExistsException,
    UserNotFoundException,
)
from logic.exceptions.groups import (
    GroupNotFoundException,
)


@dataclass(frozen=True)
class UserLoginCommand(BaseCommand):
    username: str
    password: str


@dataclass(frozen=True)
class UserLoginCommandHandler(CommandHandler[UserLoginCommand, User]):
    user_repository: BaseUserRepository

    async def handle(self, command: UserLoginCommand) -> User:
        user = await self.user_repository.get_user_by_username(
            username=command.username
        )
        if user and await self.user_repository.check_password_is_valid(
            password=command.password, hashed_password=user.password.as_generic_type()
        ):
            return user

        raise InvalidCredentialsException()


@dataclass(frozen=True)
class DeleteUserCommand(BaseCommand):
    user_oid: str


@dataclass(frozen=True)
class DeleteUserCommandHandler(CommandHandler[DeleteUserCommand, None]):
    user_repository: BaseUserRepository

    async def handle(self, command: DeleteUserCommand) -> None:
        user = await self.user_repository.delete_user(user_oid=command.user_oid)

        if not user:
            raise UserNotFoundException(value=command.user_oid)

        user.delete()
        await self._mediator.publish(user.pull_events())


@dataclass(frozen=True)
class CreateVerificationTokenCommand(BaseCommand):
    user_oid: str


@dataclass(frozen=True)
class VerifyUserCommand(BaseCommand):
    user_oid: str
    token: str


@dataclass(frozen=True)
class VerifyUserCommandHandler(CommandHandler[VerifyUserCommand, None]):
    user_repository: BaseUserRepository
    token_repository: BaseVerificationTokenRepository

    async def handle(self, command: VerifyUserCommand) -> None:
        user = await self.user_repository.get_user_by_oid(user_oid=command.user_oid)
        if not user:
            raise UserNotFoundException(value=command.user_oid)

        if await self.token_repository.check_token_exists(token=command.token):
            await self.user_repository.verify_user(user_oid=user.oid)
        else:
            raise TokenNotFoundException()


@dataclass(frozen=True)
class CreateVerificationTokenCommandHandler(
    CommandHandler[CreateVerificationTokenCommand, None]
):
    user_repository: BaseUserRepository
    token_repository: BaseVerificationTokenRepository

    async def handle(self, command: CreateVerificationTokenCommand) -> None:
        user = await self.user_repository.get_user_by_oid(user_oid=command.user_oid)
        if not user:
            raise UserNotFoundException(value=command.user_oid)

        token = VerificationToken.create(
            email=Email(value=user.email.as_generic_type()),
            user_oid=command.user_oid,
        )
        await self.token_repository.add_token(token=token)

        await self._mediator.publish(token.pull_events())


@dataclass(frozen=True)
class CreateUserCommand(BaseCommand):
    username: str
    email: str
    password: str
    group_oid: str


@dataclass(frozen=True)
class CreateUserCommandHandler(CommandHandler[CreateUserCommand, User]):
    user_repository: BaseUserRepository
    group_repository: BaseGroupRepository

    async def handle(self, command: CreateUserCommand) -> User:
        group = await self.group_repository.get_group_by_oid(
            group_oid=command.group_oid
        )

        if not group:
            raise GroupNotFoundException(oid=command.group_oid)

        if await self.user_repository.check_user_exists_by_email_and_username(
            email=command.email, username=command.username
        ):
            raise UserAlreadyExistsException()

        hashed_password = bcrypt.hashpw(
            command.password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

        new_user = await User.create(
            username=Username(value=command.username),
            email=Email(value=command.email),
            password=Password(hashed_password),
            group_id=command.group_oid,
        )

        await self.user_repository.add_user(new_user)
        await self._mediator.publish(new_user.pull_events())

        return new_user
