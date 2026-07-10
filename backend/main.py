# Tambahkan ini di backend/main.py

import os
from fastapi import Header, HTTPException

@app.get("/api/cron/sync-all")
def cron_sync_all(x_cron_secret: str = Header(None)):
    # Keamanan: hanya cron-job.org yang tahu secret ini
    expected_secret = os.getenv("CRON_SECRET", "my-secret-123")
    if x_cron_secret != expected_secret:
        raise HTTPException(403, "Forbidden")
    
    from services.scheduler_service import sync_all_users
    sync_all_users()
    return {"status": "sync triggered"}
