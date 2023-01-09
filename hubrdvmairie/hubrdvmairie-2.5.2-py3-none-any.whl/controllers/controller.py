from fastapi import APIRouter

from ..controllers.routes import external, internal, time_slots, websocket

router = APIRouter()


router.include_router(internal.router, tags=["Interne ANTS"])
router.include_router(external.router, tags=["API interfacées avec les éditeurs"])
router.include_router(
    time_slots.router, tags=["Annexe: Accès aux rendez-vous disponibles"]
)
router.include_router(websocket.router, tags=["Websocket"])
