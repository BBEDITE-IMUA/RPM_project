from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import User

async def register_user(session: AsyncSession, user_id: int, language: str):
    existing_user = await session.execute(select(User).filter(User.user_id == user_id))
    user = existing_user.scalar_one_or_none()
    if not user:
        new_user = User(user_id=user_id, language=language)
        session.add(new_user)
        await session.commit()
    else:
        user.language = language
        await session.commit()


async def get_user_language(session: AsyncSession, user_id: int):
    
    result = await session.execute(select(User).filter(User.user_id == int(user_id)))
    user = result.scalar_one_or_none()
    return user.language if user else None


async def is_user_exist(session: AsyncSession, user_id: int) -> bool:
    result = await session.execute(select(User).filter(User.user_id == user_id))
    return result.scalar_one_or_none() is not None
