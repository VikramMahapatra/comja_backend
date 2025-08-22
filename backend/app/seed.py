from sqlalchemy.orm import Session
from . import models, auth
from datetime import datetime, timezone

def seed_data(db: Session):
    # Super Admin
    if not db.query(models.User).filter_by(email="superadmin@zenzomato.com").first():
        superadmin = models.User(
            name="Super Admin",
            email="superadmin@zenzomato.com",
            password_hash=auth.get_password_hash("superadmin123"),
            role="superadmin",
            created_at=datetime.utcnow()
        )
        db.add(superadmin)

    # Restaurant Admin
    if not db.query(models.User).filter_by(email="restadmin@zenzomato.com").first():
        restadmin = models.User(
            name="Rest Admin",
            email="restadmin@zenzomato.com",
            password_hash=auth.get_password_hash("restadmin123"),
            role="restaurantadmin",
            created_at=datetime.now(timezone.utc)
        )
        db.add(restadmin)
        db.flush()
        # Restaurant
        restaurant = models.Restaurant(
            name="Pizza Palace",
            city="GenZ City",
            area="Downtown",
            address="123 Main St",
            phone="1234567890",
            status="approved",
            created_by=restadmin.id,
            created_at=datetime.now(timezone.utc)
        )
        db.add(restaurant)
        db.flush()
        # Menu
        menu = models.Menu(
            restaurant_id=restaurant.id,
            name="Pepperoni Pizza",
            description="Classic pepperoni pizza",
            price=12.99,
            image_url="https://example.com/pizza.jpg",
            created_at=datetime.now(timezone.utc)
        )
        db.add(menu)

    # Regular User
    if not db.query(models.User).filter_by(email="user@zenzomato.com").first():
        user = models.User(
            name="Test User",
            email="user@zenzomato.com",
            password_hash=auth.get_password_hash("user123"),
            role="user",
            created_at=datetime.now(timezone.utc)
        )
        db.add(user)

    db.commit()

if __name__ == "__main__":
    from database import SessionLocal
    db = SessionLocal()
    seed_data(db)
    print("Seed data inserted.")

