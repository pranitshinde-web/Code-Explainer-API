from fastapi import FastAPI
from routes.explain_router import router as explain_router
from routes.improve_router import router as improve_router
from auth.auth_router import router as auth_router

app = FastAPI(title="Code Explainer API")

app.include_router(auth_router)
app.include_router(explain_router, prefix="/api")
app.include_router(improve_router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Code Explainer API is running!"}
