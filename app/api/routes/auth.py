from fastapi import APIRouter

router = APIRouter()

@router.post("/login")
def login():
    return {"message": "Login successful"}

@router.post("/register")
def register():
    return {"message": "Register successful"}

@router.post("/logout")
def logout():
    return {"message": "Logout successful"}