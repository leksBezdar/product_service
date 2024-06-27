from fastapi import FastAPI

from application.api.healthcheck import healthcheck_router
from application.api.users.routers import user_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="product service",
        description="Ping? Are they playing table tennis?",
        debug=True,
    )

    app.include_router(healthcheck_router, prefix="/healthcheck", tags=["HEALTHCHECK"])
    app.include_router(user_router, prefix="/users", tags=["USERS"])

    return app
