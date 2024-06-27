from datetime import datetime
from pydantic import BaseModel

from application.api.schemas import SBaseQueryResponse
from domain.entities.users import UserEntity


class SCreateUserIn(BaseModel):
    phone: str
    username: str
    password: str


class SCreateUserOut(BaseModel):
    oid: str
    phone: str
    username: str
    created_at: datetime
    is_verified: bool

    @classmethod
    def from_entity(cls, user: UserEntity) -> "SCreateUserOut":
        return cls(
            oid=user.oid,
            phone=user.phone.as_generic_type(),
            username=user.username.as_generic_type(),
            created_at=user.created_at,
            is_verified=user.is_verified,
        )


class SLoginIn(BaseModel):
    username: str
    password: str


class SLoginOut(BaseModel):
    oid: str
    phone: str
    username: str
    created_at: datetime
    is_verified: bool

    @classmethod
    def from_entity(cls, user: UserEntity) -> "SLoginOut":
        return cls(
            oid=user.oid,
            phone=user.phone.as_generic_type(),
            username=user.username.as_generic_type(),
            created_at=user.created_at,
            is_verified=user.is_verified,
        )


class SGetUser(BaseModel):
    oid: str
    phone: str
    username: str
    created_at: datetime
    is_verified: bool

    @classmethod
    def from_entity(cls, user: UserEntity) -> "SGetUser":
        return cls(
            oid=user.oid,
            phone=user.phone.as_generic_type(),
            username=user.username.as_generic_type(),
            created_at=user.created_at,
            is_verified=user.is_verified,
        )


class SGetUsersQueryResponse(SBaseQueryResponse[list[SGetUser]]): ...
