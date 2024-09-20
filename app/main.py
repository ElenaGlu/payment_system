from fastapi import FastAPI, Form, Request
from starlette import status
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from sqlalchemy import select
from app.database import async_session
from app.models import User
from app.utils.access import create_hash, create_token_redis
from exceptions import AppError, ErrorType

# import redis
#
# connection_redis = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)

app = FastAPI()
templates = Jinja2Templates(directory="templates")


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
async def login(
        request: Request,
        email: str = Form(),
        password: str = Form()
) -> HTMLResponse:
    """
    User authorization in the system
    :return:
    """
    # data_aff_network = {
    #     'name': name,
    #     'postback_url': postback_url,
    #     'offer_param': offer_param
    # }
    # try:
    #     aff_network_id = (await AffiliateNetwork.create(**data_aff_network)).id
    #     await add_keitaro_id(
    #         AffiliateNetwork,
    #         aff_network_id,
    #         create_aff_network_keitaro(data_aff_network)
    #     )
    #     return templates.TemplateResponse(
    #         request=request,
    #         name="offer.html",
    #         context={'network_id': aff_network_id}
    #     )
    # except IntegrityError:
    #     return HTMLResponse('Пользовательская сеть с таким именем уже существует')

    async with async_session() as session:
        user_email = (await session.execute(
            select(User).filter(User.email == email))).scalar()
        if user_email:
            password_hash = create_hash(password)
            if user_email.hashed_password == password_hash:
                data_token = create_token_redis(user_email.id)
                # connection_redis.setex(data_token, 2419200, '')
                return data_token.split(":")[2]
            else:
                raise AppError(
                {
                    'error_type': ErrorType.ACCESS_ERROR,
                    'description': 'Invalid email or password'
                }
            )
        else:
            raise AppError(
                {
                    'error_type': ErrorType.REGISTRATION_ERROR,
                    'description': 'User is not registered.It is necessary to register'
                }
            )


