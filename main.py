from fastapi import FastAPI, responses
from controllers.users import router as users_router
from controllers.auth import router as auth_router

app = FastAPI(title="IAM with OTP via Email")
app.include_router(users_router, prefix="/api/users", tags=["USERS"])
app.include_router(auth_router, prefix="/api/auth/otp", tags=["AUTH"])


@app.get("/", include_in_schema=False)
def root():
    return responses.RedirectResponse(url="/docs")
