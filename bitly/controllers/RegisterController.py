from fastapi import APIRouter, Request, status
from starlette.responses import JSONResponse

from ..models.UserRegisterForm import UserRegisterForm
from ..models.constants import RegistrationError
from ..repositories.UserRepository import UserRepository
from ..utilities.auth.TokenHelper import TokenHelper

router = APIRouter()


@router.post("/register", summary="Create new user", name="register")
async def post(request: Request):
    form = UserRegisterForm(request)
    await form.load_data()

    if not form.is_valid:
        return JSONResponse(content=form.errors, status_code=400)

    try:
        is_present: bool = await UserRepository.verify_email_is_present(form.email)
        if is_present:
            return JSONResponse(content=[RegistrationError.EMAIL_IS_BUSY], status_code=400)
    except Exception as e:
        print(e)
        return JSONResponse(content=[RegistrationError.CREDENTIALS_VERIFICATION_FAILED],
                            status_code=500)

    new_user = form.get_mapped_user()
    is_user_added = await UserRepository.add(new_user)
    if not is_user_added:
        return JSONResponse(content=[RegistrationError.CREATE_NEW_USER_FAILED],
                            status_code=500)

    new_user.id = await UserRepository.get_user_id(new_user.email)

    response_body = {"username": new_user.username,
                     "email": new_user.email,
                     "access_token": TokenHelper.create_access_token(new_user)}
    return JSONResponse(content=response_body, status_code=status.HTTP_201_CREATED)

register_router = router
