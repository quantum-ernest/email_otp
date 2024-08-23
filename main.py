from fastapi import FastAPI, responses
from starlette.middleware.cors import CORSMiddleware

from controllers.users import router as users_router
from controllers.auth import router as auth_router

from config.database import Base, engine

Base.metadata.create_all(bind=engine)
app = FastAPI(title="OTP Authentication via Email")
app.include_router(auth_router, prefix="/api/auth/otp", tags=["AUTH"])
app.include_router(users_router, prefix="/api/users", tags=["USERS"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", include_in_schema=False)
def root():
    """
    Redirect the root URL to the API documentation.

    Returns:
        RedirectResponse: Redirects to the "/docs" URL.
    """
    return responses.RedirectResponse(url="/docs")
