from sqlalchemy import select, func

from app.database.models import async_session, User


async def get_user(tg_id: int) -> User | None:
    """Foydalanuvchining ro'yxatdan o'tganini tekshirish (tg_id bo'yicha)"""
    async with async_session() as session:
        return await session.scalar(
            select(User).where(User.tg_id == tg_id)
        )


async def add_user(
    tg_id: int,
    full_name: str,
    phone_number: str,
    direction: str,
    study_type: str,
    level: str = "Bakalavr",
    jshshir: str | None = None,
    passport_id: str | None = None,
) -> User:
    async with async_session() as session:
        user = User(
            tg_id=tg_id,
            full_name=full_name,
            phone_number=phone_number,
            jshshir=jshshir,
            passport_id=passport_id,
            level=level,
            direction=direction,
            study_type=study_type,
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user


async def get_all_users() -> list[User]:
    async with async_session() as session:
        result = await session.scalars(
            select(User).order_by(User.created_at.desc())
        )
        return list(result.all())


async def get_users_count() -> int:
    async with async_session() as session:
        result = await session.scalar(select(func.count()).select_from(User))
        return result or 0


async def delete_user(tg_id: int) -> bool:
    async with async_session() as session:
        user = await session.scalar(
            select(User).where(User.tg_id == tg_id).order_by(User.created_at.desc())
        )
        if user:
            await session.delete(user)
            await session.commit()
            return True
        return False
