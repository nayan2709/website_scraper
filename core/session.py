from contextvars import ContextVar, Token
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    create_async_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from core.config import config

# Context for managing session scope across async tasks
session_context: ContextVar[str] = ContextVar("session_context")


# Get the session context from the ContextVar
def get_session_context() -> str:
    return session_context.get()


# Set the session context and return a Token to reset later
def set_session_context(session_id: str) -> Token:
    return session_context.set(session_id)


# Reset the session context using a previously saved Token
def reset_session_context(context: Token) -> None:
    session_context.reset(context)


# Create an async engine for the database
engine = create_async_engine(config.DB_URL, pool_recycle=3600)

# Create an async session factory using the async engine
async_session_factory = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Prevents data from being expired after commit
)

# Define a scoped session with session management based on the context
session: async_scoped_session = async_scoped_session(
    session_factory=async_session_factory,
    scopefunc=get_session_context,  # Session is scoped to the context defined by get_session_context
)

# Declare the base for model classes
Base = declarative_base()
