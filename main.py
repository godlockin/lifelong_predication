from fastapi import FastAPI

from backend.framework.cors_middleware import add_cors_middleware
from backend.framework.time_middleware import TimingMiddleware
from backend.router.router import api_router

app = FastAPI()

add_cors_middleware(app)

app.add_middleware(TimingMiddleware)

app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8080, log_level="info", reload=True)
