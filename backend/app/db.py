"""SQLModel engine + session for the user store. Owner: Person A.

SQLite is the only persistent store in the app (users/officers). Conversation state and
verification packets remain in-memory (app/models/store.py) for the demo.
"""
from sqlmodel import SQLModel, Session, create_engine

from app.config import DATABASE_URL

# check_same_thread=False so FastAPI's threadpool can share the SQLite connection pool.
_connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, echo=False, connect_args=_connect_args)


def init_db() -> None:
    """Create tables. Import models first so they register on SQLModel.metadata."""
    from app.models.user import User  # noqa: F401  (registers the table)
    SQLModel.metadata.create_all(engine)


def get_session():
    """FastAPI dependency yielding a DB session."""
    with Session(engine) as session:
        yield session
