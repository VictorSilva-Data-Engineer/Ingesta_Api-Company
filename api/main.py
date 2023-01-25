from fastapi import FastAPI
from router.routers import router
import uvicorn



#Handling error
from fastapi.exceptions import RequestValidationError
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

app = FastAPI(debug=True)

app.include_router(router)

# ************** Exception Handler **************
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),)

if __name__== '__main__':
   uvicorn.run("main:app",  host="127.0.0.1", port=8000)