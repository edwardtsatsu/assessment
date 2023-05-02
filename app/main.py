from fastapi import FastAPI, Request, status, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from .routers import diagnosis

app = FastAPI()

app.include_router(diagnosis.router)


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
