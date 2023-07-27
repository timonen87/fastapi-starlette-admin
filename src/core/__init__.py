# Alembic needs to import models and Base another directory that real "db"
# because it identifies as circular dependency. Needs to looking forward a
# better solution
# from admin_app import models
from models import user, post, comment

from core.base import Base