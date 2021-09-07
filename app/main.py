import uvicorn
import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.api.routers import api_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://thawing-springs-05749.herokuapp.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = f'{process_time:.2f}s'
    return response

app.include_router(api_router)

if __name__ == '__main__':
    uvicorn.run(app)
