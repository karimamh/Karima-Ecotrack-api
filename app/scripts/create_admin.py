u200B
 
import argparse
from app.core.db import SessionLocal, engine
from app.core.db import Base
from app.models import User
from app.core.security import hash_password


def main():
    parser = argparse.ArgumentParser(description="Créer un admin")
    parser.add_argument("--email", required=True)
    parser.add_argument("--username", required=True)
    parser.add_argument("--password", required=True)
    args = parser.parse_args()

    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        exists = db.query(User).filter((User.email == args.email) | (User.username == args.username)).first()
        if exists:
            print("Utilisateur déjà présent")
            return
        user = User(
            email=args.email,
            username=args.username,
            hashed_password=hash_password(args.password),
            role="admin",
            is_active=True,
        )
        db.add(user)
        db.commit()
        print("Admin créé")
    finally:
        db.close()


if __name__ == "__main__":
    main()


