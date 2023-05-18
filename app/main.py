from fastapi import Depends, FastAPI, HTTPException, Request, status, Response
from fastapi.security import APIKeyHeader
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, PlainTextResponse
from starlette.middleware.base import BaseHTTPMiddleware

from .routers import diagnosis

app = FastAPI()

api_key_header = APIKeyHeader(name="X-API-Key")

app.include_router(diagnosis.router)

async def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key != "secret_api_key":
        raise HTTPException(status_code=401, detail="Invalid API key")


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        try:
            await verify_api_key(request.headers.get("X-API-Key"))
        except HTTPException as ex:
            return PlainTextResponse(str(ex), status_code=ex.status_code)

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
