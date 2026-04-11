from fastapi import APIRouter

router = APIRouter()

@router.get("/test")
def test_route():
    return {
        "status": "success",
        "message": "API Router is connected to main app and is working fine."
    }