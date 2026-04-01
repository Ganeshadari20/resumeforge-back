from fastapi import APIRouter

router = APIRouter()

@router.get("/companies")
def get_companies():
    """Mock list of companies."""
    return [
        "Google", "Amazon", "Microsoft", "Meta", "Apple", "Netflix", "Tesla"
    ]

@router.get("/roles")
def get_roles():
    """Mock list of roles."""
    return [
        "Software Engineer", "Data Scientist", "Product Manager", "UI/UX Designer", "DevOps Engineer"
    ]
