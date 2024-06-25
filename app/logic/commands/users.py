from dataclasses import dataclass

from domain.entities.users import UserEntity
from domain.values.users import Phone, Password, Username
from infrastructure.repositories.users.base import (
    IUserRepository,
)
from logic.commands.base import BaseCommand, CommandHandler
from logic.exceptions.users import (
    UserAlreadyExistsException,
    UserNotFoundException,
)


@dataclass(frozen=True)
class CreateUserCommand(BaseCommand):
    username: str
    phone: str
    password: str


@dataclass(frozen=True)
class CreateUserCommandHandler(CommandHandler[CreateUserCommand, UserEntity]):
    user_repository: IUserRepository

    async def handle(self, command: CreateUserCommand) -> UserEntity:
        if await self.user_repository.check_user_exists_by_phone_and_username(
            phone=command.phone, username=command.username
        ):
            raise UserAlreadyExistsException()

        new_user = await UserEntity.create(
            username=Username(value=command.username),
            phone=Phone(value=command.phone),
            password=Password(value=command.password),
        )

        await self.user_repository.add(new_user)
        await self._mediator.publish(new_user.pull_events())

        return new_user


@dataclass(frozen=True)
class DeleteUserCommand(BaseCommand):
    user_oid: str


@dataclass(frozen=True)
class DeleteUserCommandHandler(CommandHandler[DeleteUserCommand, None]):
    user_repository: IUserRepository

    async def handle(self, command: DeleteUserCommand) -> None:
        user = await self.user_repository.delete(user_oid=command.user_oid)

        if not user:
            raise UserNotFoundException(value=command.user_oid)

        user.delete()
        await self._mediator.publish(user.pull_events())
