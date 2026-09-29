from fastapi import Depends, FastAPI

from stage00.config import Settings, get_settings

app = FastAPI(title="Stage 00 · Python 백엔드")


@app.get("/health")
async def health(settings: Settings = Depends(get_settings)) -> dict[str, str]:
    return {"status": "ok", "app": settings.app_name}
