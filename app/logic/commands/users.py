from dataclasses import dataclass

from domain.entities.users import UserEntity
from domain.values.users import Phone, Password, Username
from infrastructure.repositories.users.base import (
    IUserRepository,
)
from logic.commands.base import BaseCommand, CommandHandler
from logic.exceptions.users import (
    InvalidCredentialsException,
    UserAlreadyExistsException,
    UserNotFoundException,
    UsernameAlreadyExists,
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
        username = Username(value=command.username)
        phone = Phone(value=command.phone)
        password = Password(value=command.password)

        # TODO move existing check to entity layer
        if await self.user_repository.check_user_exists_by_phone_and_username(
            phone=phone.as_generic_type(), username=username.as_generic_type()
        ):
            raise UserAlreadyExistsException()

        new_user = await UserEntity.create(
            username=username,
            phone=phone,
            password=password,
        )

        await self.user_repository.add(new_user)
        await self._mediator.publish(new_user.pull_events())

        return new_user


@dataclass(frozen=True)
class ChangeUsernameCommand(BaseCommand):
    user_oid: str
    new_username: str


@dataclass(frozen=True)
class ChangeUsernameCommandHandler(CommandHandler[ChangeUsernameCommand, None]):
    user_repository: IUserRepository

    async def handle(self, command: ChangeUsernameCommand) -> None:
        user = await self.user_repository.get_by_oid(oid=command.user_oid)
        if not user:
            raise UserNotFoundException(value=command.user_oid)

        if command.new_username != user.username.as_generic_type():
            existing_usernames = await self.user_repository.get_existing_usernames()

            if command.new_username in existing_usernames:
                raise UsernameAlreadyExists(command.new_username)

            new_username = Username(value=command.new_username)
            await user.change_username(new_username=new_username)
            await self.user_repository.update(user)
            await self._mediator.publish(user.pull_events())


@dataclass(frozen=True)
class ChangePasswordCommand(BaseCommand):
    user_oid: str
    old_password: str
    new_password: str


@dataclass(frozen=True)
class ChangePasswordCommandHandler(CommandHandler[ChangePasswordCommand, None]):
    user_repository: IUserRepository

    async def handle(self, command: ChangePasswordCommand) -> None:
        user = await self.user_repository.get_by_oid(oid=command.user_oid)
        if not user:
            raise UserNotFoundException(value=command.user_oid)
        if not user.password.check_password(command.old_password):
            raise InvalidCredentialsException()

        new_password = Password(value=command.new_password)
        await user.change_password(new_password=new_password)
        await self.user_repository.update(user)
        await self._mediator.publish(user.pull_events())


@dataclass(frozen=True)
class RestoreUserCommand(BaseCommand):
    user_oid: str


@dataclass(frozen=True)
class RestoreUserCommandHandler(CommandHandler[RestoreUserCommand, None]):
    user_repository: IUserRepository

    async def handle(self, command: RestoreUserCommand) -> None:
        user = await self.user_repository.get_by_oid(oid=command.user_oid)
        if not user:
            raise UserNotFoundException(value=command.user_oid)

        await user.restore()
        await self.user_repository.restore(user)
        await self._mediator.publish(user.pull_events())


@dataclass(frozen=True)
class DeleteUserCommand(BaseCommand):
    user_oid: str


@dataclass(frozen=True)
class DeleteUserCommandHandler(CommandHandler[DeleteUserCommand, None]):
    user_repository: IUserRepository

    async def handle(self, command: DeleteUserCommand) -> None:
        user = await self.user_repository.get_by_oid(oid=command.user_oid)

        if not user:
            raise UserNotFoundException(value=command.user_oid)

        await user.delete()
        await self.user_repository.delete(oid=command.user_oid)
        await self._mediator.publish(user.pull_events())
