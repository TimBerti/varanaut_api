import uvicorn
import jwt
from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routers import api_router


app = FastAPI()


@app.middleware("http")
async def auth(request: Request, call_next):
    try:
        payload = jwt.decode(request.headers['token'], settings.SECRET_KEY, algorithms=[
            settings.SECURITY_ALGORITHM])

        if datetime.fromtimestamp(payload.get('exp')) < datetime.now():
            return JSONResponse(content='Token expired.', status_code=403)

        response = await call_next(request)
        return response
    except:
        return JSONResponse(content='Could not validate token.', status_code=403)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

if __name__ == '__main__':
    uvicorn.run(app)
