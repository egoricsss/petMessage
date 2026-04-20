from fastapi import FastAPI, Depends, HTTPException, status


def check_auth(token: str) -> bool:
    return token == "secret"


app = FastAPI()


@app.get("/profile")
async def get_profile(is_auth: bool = Depends(check_auth)) -> str:
    if is_auth:
        return "User is authorized"
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
