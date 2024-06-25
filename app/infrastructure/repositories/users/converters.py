from typing import Any, Mapping
from domain.entities.users import UserEntity
from domain.values.users import Phone, Password, Username


def convert_user_entity_to_dict(user: UserEntity) -> dict:
    return {
        "oid": user.oid,
        "phone": user.phone.as_generic_type(),
        "username": user.username.as_generic_type(),
        "password": user.password.as_generic_type(),
        "created_at": user.created_at,
        "is_verified": user.is_verified,
    }


def convert_user_dict_to_entity(user_document: Mapping[str, Any]) -> UserEntity:
    return UserEntity(
        oid=user_document["oid"],
        phone=Phone(value=user_document["phone"]),
        username=Username(value=user_document["username"]),
        password=Password(value=user_document["password"]),
        created_at=user_document["created_at"],
        is_verified=user_document["is_verified"],
    )
