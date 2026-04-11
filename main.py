from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from api.routes import router


app = FastAPI(title="Mini-Preplexity")


app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000"
    ],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)


@app.get("/")
def root():
    return {
        "success": True,
        "message": "Your server is up and running"
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=5000, reload=True)