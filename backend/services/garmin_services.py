import os, json
from garth import Client
from garth.exc import GarthException
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models import User, Activity, DailyMetric

async def login_garmin(db: Session, user: User, email: str, password: str):
    client = Client()
    try:
        client.login(email, password)
        oauth1 = client.garth.oauth1_token.as_dict()
        oauth2 = client.garth.oauth2_token.as_dict()
        
        # Simpan token ke database
        user.garmin_token1 = json.dumps(oauth1)
        user.garmin_token2 = json.dumps(oauth2)
        user.garmin_email = email
        db.commit()
        return True
    except GarthException as e:
        raise Exception(f"Garmin login failed: {e}")

def resume_client(user: User) -> Client:
    client = Client()
    if user.garmin_token1 and user.garmin_token2:
        try:
            # Load token dari database
            from garth.oauth1 import OAuth1Token
            from garth.oauth2 import OAuth2Token
            
            t1 = OAuth1Token(**json.loads(user.garmin_token1))
            t2 = OAuth2Token(**json.loads(user.garmin_token2))
            client.garth.oauth1_token = t1
            client.garth.oauth2_token = t2
            return client
        except Exception as e:
            raise Exception(f"Failed to resume session: {e}")
    raise Exception("Garmin not connected")
