from dataclasses import dataclass

from domain.entities.groups import UserGroup
from domain.values.groups import Title
from infrastructure.repositories.groups.base import (
    BaseGroupRepository,
)
from logic.commands.base import BaseCommand, CommandHandler
from logic.exceptions.groups import (
    GroupAlreadyExistsException,
    GroupNotFoundException,
)


@dataclass(frozen=True)
class CreateGroupCommand(BaseCommand):
    title: str


@dataclass(frozen=True)
class CreateGroupCommandHandler(CommandHandler[CreateGroupCommand, UserGroup]):
    group_repository: BaseGroupRepository

    async def handle(self, command: CreateGroupCommand) -> UserGroup:
        if await self.group_repository.check_group_exists_by_title(command.title):
            raise GroupAlreadyExistsException(command.title)

        title = Title(value=command.title)
        new_group = UserGroup.create(title=title)

        await self.group_repository.add_group(new_group)
        await self._mediator.publish(new_group.pull_events())

        return new_group


@dataclass(frozen=True)
class DeleteGroupCommand(BaseCommand):
    group_oid: str


@dataclass(frozen=True)
class DeleteGroupCommandHandler(CommandHandler[DeleteGroupCommand, None]):
    group_repository: BaseGroupRepository

    async def handle(self, command: DeleteGroupCommand) -> None:
        group = await self.group_repository.delete_group(group_oid=command.group_oid)

        if not group:
            raise GroupNotFoundException(oid=command.group_oid)

        group.delete()
        await self._mediator.publish(group.pull_events())
