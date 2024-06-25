from domain.entities.users import UserEntity
from domain.values.users import Phone, Username
from infrastructure.models.users import UserModel


def convert_user_entity_to_model(user: UserEntity) -> UserModel:
    return UserModel(
        oid=user.oid,
        phone=user.phone.as_generic_type(),
        username=user.username.as_generic_type(),
        password=user.password.as_generic_type(),
        created_at=user.created_at,
        is_verified=user.is_verified,
    )


def convert_user_model_to_entity(user: UserModel) -> UserEntity:
    return UserEntity(
        oid=user.oid,
        phone=Phone(value=user.phone),
        username=Username(value=user.username),
        password=user.password,
        created_at=user.created_at,
        is_verified=user.is_verified,
    )
