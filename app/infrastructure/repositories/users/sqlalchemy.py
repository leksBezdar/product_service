from dataclasses import dataclass
from typing import Iterable

from sqlalchemy import func, or_, select

from domain.entities.users import UserEntity
from infrastructure.exception_mapper import exception_mapper
from infrastructure.models.users import UserModel
from infrastructure.repositories.common.repository import ISqlalchemyRepository
from infrastructure.repositories.users.base import (
    IUserRepository,
)
from infrastructure.repositories.users.converters import (
    convert_user_entity_to_model,
    convert_user_model_to_entity,
)
from infrastructure.repositories.users.filters.users import GetUsersFilters


@dataclass(frozen=True)
class SqlAlchemyUserRepository(IUserRepository, ISqlalchemyRepository):
    _model: type[UserModel] = UserModel

    @exception_mapper
    async def add(self, user: UserEntity) -> None:
        user_model = convert_user_entity_to_model(user)
        async with self.get_session() as session:
            session.add(user_model)
            await session.commit()

    @exception_mapper
    async def get_by_oid(self, oid: str) -> UserEntity | None:
        async with self.get_session() as session:
            result = await session.execute(select(self._model).filter_by(oid=oid))
            user = result.scalars().first()

            if user:
                return convert_user_model_to_entity(user)

    @exception_mapper
    async def get_by_username(self, username: str) -> UserEntity | None:
        async with self.get_session() as session:
            result = await session.execute(
                select(self._model).filter_by(username=username)
            )
            user = result.scalars().first()

            if user:
                return convert_user_model_to_entity(user)

    @exception_mapper
    async def get_all(
        self, filters: GetUsersFilters
    ) -> tuple[Iterable[UserEntity], int]:
        async with self.get_session() as session:
            query = select(self._model).limit(filters.limit).offset(filters.offset)
            result = await session.execute(query)

            users = result.scalars().all()
            users = [convert_user_model_to_entity(user) for user in users]

            count = await session.execute(
                select([func.count()]).select_from(self._model)
            )
            count = count.scalar()

            return users, count

    @exception_mapper
    async def delete(self, oid: str) -> UserEntity | None:
        async with self.get_session() as session:
            result = await session.execute(select(self._model).filter_by(oid=oid))
            user = result.scalars().first()
            if user:
                await session.delete(user)
                await session.commit()

                return convert_user_model_to_entity(user)

    @exception_mapper
    async def check_user_exists_by_phone_and_username(
        self, phone: str, username: str
    ) -> bool:
        async with self.get_session() as session:
            result = await session.execute(
                select(self._model).filter(
                    or_(self._model.phone == phone, self._model.username == username)
                )
            )
            return result.scalars().first() is not None
