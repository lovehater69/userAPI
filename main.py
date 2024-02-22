from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from router import user
from database.mongodb import mongo_db

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(user.router)

# Event handlers
@app.on_event("startup")
async def startup_event():
    print("Application started")

@app.on_event("shutdown")
async def shutdown_event():
    print("Application shutting down")
    # Close MongoDB connection
    mongo_db.client.close()

# Exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"message": "Validation error", "details": exc.errors()}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)