from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import JSONResponse

from bitly.models.UserLoginForm import UserLoginForm
from bitly.models.constants import LoginError
from bitly.repositories.UserRepository import UserRepository
from bitly.utilities import PasswordHelper
from bitly.utilities.auth.TokenHelper import TokenHelper

router = APIRouter()


@router.post("/login", summary="Create token for user")
async def post(request: Request):
    form = UserLoginForm(request)
    await form.load_data()

    if not form.is_valid:
        return JSONResponse(content=form.errors, status_code=400)

    user = await UserRepository.get_by_email(form.email)
    if not user:
        return JSONResponse(content=LoginError.INVALID_EMAIL, status_code=400)

    is_password_correct = PasswordHelper.verify_password(form.password, user.hashed_password)
    if not is_password_correct:
        return JSONResponse(content=LoginError.INVALID_PASSWORD, status_code=400)

    # just create a new token if everything is correct

    # ONE TOKEN FOR ALL DEVICES? - BE based. OR. Unique token each time? - FE based.

    # sorry, too many attempts for login. Please try in 10 minutes.

    # TEMPORARY CACHE THAT CHECKS IF USER WAS LOGGED IN RECENTLY

    # you create this token once, and further you just refresh it

    # get existing token if not expired ? handle in FE

    # each login act should refresh both access and refresh tokens with limited attempts(5) handled by simple cache

    access_token = TokenHelper.create_access_token(user)

    return JSONResponse(content=access_token, status_code=200)  # or 201?

login_router = router
