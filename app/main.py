from fastapi import FastAPI, Form, Request
from starlette import status
from starlette.responses import HTMLResponse

app = FastAPI()


@app.post("/login", status_code=status.HTTP_200_OK)
async def login(
        request: Request,
        email: str = Form(),
        hashed_password: str = Form()
) -> HTMLResponse:
    """
    User authorization in the system
    :return:
    """
    pass
