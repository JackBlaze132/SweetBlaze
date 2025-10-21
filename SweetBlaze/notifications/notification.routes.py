from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
from datetime import datetime
import os
import uuid

from app.sockets.websocket_manager import manager  # Ajusta el import según tu estructura

router = APIRouter()

UPLOAD_DIR = "app/static/uploads"


@router.post("/notifications")
async def create_notification(
    title: str = Form(...),
    message: str = Form(...),
    type: str = Form(...),
    file: UploadFile = File(None)
):
    try:
        file_url = None

        if file:
            os.makedirs(UPLOAD_DIR, exist_ok=True)
            filename = f"{uuid.uuid4().hex}_{file.filename}"
            file_path = os.path.join(UPLOAD_DIR, filename)

            with open(file_path, "wb") as f:
                content = await file.read()
                f.write(content)

            file_url = f"http://localhost:8000/static/uploads/{filename}"

        notification = {
            "id": int(datetime.utcnow().timestamp() * 1000),
            "title": title,
            "message": message,
            "type": type,
            "timestamp": datetime.utcnow().isoformat(),
            "file_url": file_url
        }

        await manager.broadcast(notification)

        return JSONResponse(content={"success": True, "notification": notification})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


    await manager.broadcast(notification)

    return JSONResponse(content={"success": True, "notification": notification})
