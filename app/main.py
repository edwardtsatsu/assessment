from fastapi import Depends, FastAPI, HTTPException, Request, status, Response
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.config import settings

from .routers import diagnosis

app = FastAPI()

origins = [
    "*"
]  # this is because of the purpose of the assignment, I would have been specific to a domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.include_router(diagnosis.router)
api_key_header = APIKeyHeader(name="X-API-Key")


async def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key != settings.api_key:
        raise HTTPException(status_code=401, detail="Invalid API key received")


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        api_key = request.headers.get("X-API-Key")
        if not api_key:
            error_message = {"detail": "API key is missing in the request"}
            return JSONResponse(content=error_message, status_code=401)

        try:
            await verify_api_key(api_key)
        except HTTPException as ex:
            error_message = {"detail": "Invalid API key received"}
            return JSONResponse(content=error_message, status_code=ex.status_code)

        response = await call_next(request)
        return response


app.add_middleware(AuthMiddleware)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> Response:
    missing_fields = []
    for error in exc.errors():
        if error["type"] == "value_error.missing":
            missing_fields.append(error["loc"][-1])
            message = f"{error['loc'][-1]} field is required"
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST, content={"detail": message}
            )
    if missing_fields:
        message = f"{', '.join(missing_fields)} fields are required"
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"detail": message}
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Malformed JSON"},
        )
