from fastapi import FastAPI, Form, Request
from starlette import status
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from app.utils.access import Access

# import redis
#
# connection_redis = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")


@app.get("/login", response_class=HTMLResponse)
async def load_start_page(request: Request) -> HTMLResponse:
    """
    Render start html-page
    """
    return templates.TemplateResponse(
        request=request,
        name="login.html"
    )


@app.post("/login", status_code=status.HTTP_200_OK)
async def user_login(
        request: Request,
        email: str = Form(),
        password: str = Form()
) -> HTMLResponse:
    """
    User authorization in the system
    :return:
    """
    obj_auth = Access()
    obj_auth = await (obj_auth.login(email, password))
    return templates.TemplateResponse(
        request=request,
        name="account.html",
        context=obj_auth
    )


@app.post("/account", status_code=status.HTTP_200_OK)
async def get_account(request: Request) -> HTMLResponse:
    """
    :return:
    """
    # user_data = json.loads(request.body)
    # token_user = user_connection.keys(pattern=f"*:{token_type}:{user_data['token']}")[0]
    # if token_user:
    #     profile_id = int(token_user.split(":")[0])
    #     del user_data['token']
    #     return func(profile_id, user_data)     обработка токена

    obj_auth = Access()
    obj_auth = await (obj_auth.account(1))
    return templates.TemplateResponse(
        request=request,
        name="pay.html",
        context=obj_auth
    )