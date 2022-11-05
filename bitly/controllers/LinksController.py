from fastapi import APIRouter
from starlette.requests import Request

router = APIRouter()


@router.get("/links", name="links_get")
async def get(request: Request):
    return


@router.post("/links", name="links_post")
async def post(request: Request):
    return

links_router = router
