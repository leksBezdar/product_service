from fastapi import FastAPI

from .healthcheck import healthcheck_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="product service",
        description="Ping? Are they playing table tennis?",
        debug=True,
    )

    app.include_router(healthcheck_router, prefix="/healthcheck", tags=["HEALTHCHECK"])

    return app