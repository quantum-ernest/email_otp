from fastapi import FastAPI, responses
from starlette.middleware.cors import CORSMiddleware

from controllers.users import router as users_router
from controllers.auth import router as auth_router

app = FastAPI(title="IAM with OTP via Email")
app.include_router(users_router, prefix="/api/users", tags=["USERS"])
app.include_router(auth_router, prefix="/api/auth/otp", tags=["AUTH"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/", include_in_schema=False)
def root():
    return responses.RedirectResponse(url="/docs")
