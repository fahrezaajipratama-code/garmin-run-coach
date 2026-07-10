@router.post("/register")
async def register(data: RegisterIn, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(400, "Email sudah terdaftar")
    
    u = User(email=data.email, password_hash=pwd.hash(data.password))
    db.add(u)
    db.commit()
    db.refresh(u)
    
    try:
        await login_garmin(db, u, data.garmin_email, data.garmin_password)
    except Exception as e:
        db.delete(u)
        db.commit()
        raise HTTPException(400, str(e))
        
    return {"token": make_token(u.id), "user_id": u.id}
