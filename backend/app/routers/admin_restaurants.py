from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from .. import models, database
from ..dependencies import require_role, get_db

router = APIRouter(prefix="/admin/restaurants", tags=["admin"])

@router.get("/")
def list_restaurants_admin(
    status: str = Query(None, description="Filter by status: approved, pending, rejected"),
    area: str = Query(None, description="Filter by area"),
    city: str = Query(None, description="Filter by city"),
    name: str = Query(None, description="Search by restaurant name"),
    db: Session = Depends(get_db),
    superadmin=Depends(require_role("superadmin"))
):
    query = db.query(models.Restaurant)
    if status:
        query = query.filter(models.Restaurant.status == status)
    if area:
        query = query.filter(models.Restaurant.area.ilike(f"%{area}%"))
    if city:
        query = query.filter(models.Restaurant.city.ilike(f"%{city}%"))
    if name:
        query = query.filter(models.Restaurant.name.ilike(f"%{name}%"))
    return query.all()
