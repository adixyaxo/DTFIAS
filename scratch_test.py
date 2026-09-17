from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

try:
    app.mount("/static", StaticFiles(directory="does_not_exist"), name="static")
    print("Mounted successfully")
except Exception as e:
    print(f"Failed to mount: {type(e).__name__} - {e}")
