from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from db.database import get_session
from models.category import Category, CategoryCreate, CategoryRead
from crud.category import create_category, get_categories, delete_category

router = APIRouter()


@router.post("/", response_model=CategoryRead)
def create(category: CategoryCreate, session: Session = Depends(get_session)):
    try:
        category_data = Category(**category.dict())
        return create_category(session, category_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[CategoryRead])
def read_all(session: Session = Depends(get_session)):
    return get_categories(session)


@router.delete("/{category_id}", response_model=CategoryRead)
def delete(category_id: int, session: Session = Depends(get_session)):
    category = delete_category(session, category_id)
    if not category:
        raise HTTPException(status_code=404, detail=f"Category with ID {category_id} not found")
    return category
