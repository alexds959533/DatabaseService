import uvicorn, sys
from fastapi import FastAPI

from core import api, settings
from core.db.mongodb_utils import connect_to_mongo, close_mongo_connection

#sys.path.append(".")

app = FastAPI(title="Сервис загрузки и хранения файлов")

app.include_router(api.router)

app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=True
    )

