from dataclasses import dataclass

from domain.entities.users import UserEntity
from infrastructure.repositories.common.repository import IPostgresRepository
from infrastructure.repositories.users.base import (
    IUserRepository,
)


@dataclass(frozen=True)
class PostgresUserRepository(IUserRepository, IPostgresRepository):
    _model: type[UserEntity] = UserEntity
