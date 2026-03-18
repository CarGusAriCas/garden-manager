"""Script para crear el usuario admin inicial."""
import sys
import os
sys.path.insert(0, os.path.abspath('.'))

import app.models.client
import app.models.employee
import app.models.task
import app.models.job, app.models.absence, app.models.user  # noqa
from app.core.database import SessionLocal
from app.models.user import User
from app.core.security import hash_password

db = SessionLocal()

# Verifica que no existe ya
existing = db.query(User).filter(User.email == "admin@gardenmanager.com").first()
if existing:
    print("⚠️  El admin ya existe.")
else:
    admin = User(
        email                = "admin@gardenmanager.com",
        hashed_password      = hash_password("Admin1234!"),
        role                 = "admin",
        is_active            = True,
        must_change_password = False,
    )
    db.add(admin)
    db.commit()
    print("✅ Admin creado:")
    print("   Email:      admin@gardenmanager.com")
    print("   Contraseña: Admin1234!")

db.close()