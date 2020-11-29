from authlib.integrations.starlette_client import OAuth
from fastapi.responses import HTMLResponse
from starlette.config import Config
from starlette.middleware.sessions import SessionMiddleware
from loginpass import create_fastapi_routes, Twitter, GitHub, Google

from fastapi import FastAPI

app = FastAPI()

config = Config(".env")
oauth = OAuth(config)

app.add_middleware(SessionMiddleware, secret_key=config.get("SECRET_KEY"))

backends = [Twitter, GitHub, Google]


@app.get("/", response_class=HTMLResponse)
async def root() -> str:
    tpl = '<li><a href="/login/{}">{}</a></li>'
    lis = [tpl.format(b.NAME, b.NAME) for b in backends]
    return "<ul>{}</ul>".format("".join(lis))


def handle_authorize(remote, token, user_info, request):
    return user_info


router = create_fastapi_routes(backends, oauth, handle_authorize)

app.include_router(router)
