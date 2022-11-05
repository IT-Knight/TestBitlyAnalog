from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from bitly.controllers import links_router, login_router, register_router

app = FastAPI(default_response_class=HTMLResponse)
app.debug = True

app.include_router(register_router)
app.include_router(login_router)
app.include_router(links_router)
