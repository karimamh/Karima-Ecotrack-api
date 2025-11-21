from datetime import datetime, timedelta
from app.core.db import SessionLocal, engine, Base
from app.models import Zone, Source, Indicator, User
from app.core.security import hash_password


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Zones de base
        if not db.query(Zone).first():
            db.add_all(
                [
                    Zone(name="Paris", postal_code="75000", latitude=48.8566, longitude=2.3522),
                    Zone(name="Lyon", postal_code="69000", latitude=45.7640, longitude=4.8357),
                ]
            )
            db.commit()
        # Sources
        if not db.query(Source).filter_by(name="OpenAQ").first():
            db.add(Source(name="OpenAQ", kind="openaq", url="https://api.openaq.org"))
        if not db.query(Source).filter_by(name="Open-Meteo").first():
            db.add(Source(name="Open-Meteo", kind="openmeteo", url="https://api.open-meteo.com"))
        db.commit()
        # Admin par défaut
        if not db.query(User).filter_by(role="admin").first():
            db.add(User(email="admin@example.com", username="admin", hashed_password=hash_password("admin123"), role="admin"))
            db.commit()
        # Quelques indicateurs fictifs
        zone = db.query(Zone).first()
        src = db.query(Source).first()
        if zone and src and not db.query(Indicator).first():
            now = datetime.utcnow()
            for i in range(3):
                db.add(
                    Indicator(
                        source_id=src.id,
                        type="pm25",
                        value=12 + i,
                        unit="ug/m3",
                        timestamp=now - timedelta(hours=i),
                        zone_id=zone.id,
                    )
                )
            db.commit()
            print("Seed inséré")
        else:
            print("Données déjà présentes")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
