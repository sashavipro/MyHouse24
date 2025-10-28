"""Config/api.py."""
from ninja import NinjaAPI
from ninja.security import SessionAuth

from src.users.api import router as users_router
from src.building.api import router as building_router
from src.finance.api import router as finance_router

api = NinjaAPI(version="1.0.0", auth=SessionAuth())

api.add_router("/users", users_router)
api.add_router("/buildings", building_router)
api.add_router("/finance", finance_router)
