"""Entrypoint: starts the FruitAPI server."""
from app.app import create_app

app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
