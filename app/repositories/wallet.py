from datetime import datetime
from sqlalchemy import (
    CheckConstraint,
    Enum,
    ForeignKey,
    Integer,
    select
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    selectinload,
    joinedload
)
from app.models import History, HistoryType, Wallet
from sqlalchemy.ext.asyncio import AsyncSession
from app.exceptions import AppException

class BaseORM(DeclarativeBase):
    pass

class HistoriyORM(BaseORM):
    __tablename__ = "histories"
    history_id: Mapped[int] = mapped_column(
        primary_key=True)
    name: Mapped[str]
    amount: Mapped[int] = mapped_column(
        Integer, CheckConstraint("amount > 0"))
    type: Mapped[HistoryType] = mapped_column(
        Enum(HistoryType))
    wallet_id: Mapped[int] = mapped_column(
        ForeignKey(
            "wallets.wallet_id", ondelete="CASCADE"
        ),
        index=True)
    history_at: Mapped[datetime]
    wallet: Mapped["WalletORM"] = relationship(
        back_populates="histories")
    
    @classmethod
    def from_entity(cls, history: History):
        return cls(
            history_id=history.history_id,
            name=history.name,
            amount=history.amount,
            type=history.type,
            wallet_id=history.wallet_id,
            history_at=history.history_at)
    
    def to_entity(self) -> History:
        return History.model_validate(self)
    
class WalletORM(BaseORM):
    __tablename__ = "wallets"
    wallet_id: Mapped[int] = mapped_column(
        primary_key=True)
    name: Mapped[str]
    histories: Mapped[
        list[HistoryORM]
    ] = relationship(
        back_populates="wallet",
        order_by=HistoriyORM.history_at.desc(),
        cascade=(
            "save-update, merge, expunge, delete, delete-orphan"
        ))

    @classmethod
    def from_entity(cls, wallet: Wallet):
        return cls(
            wallet_id=Wallet.wallet_id,
            name=Wallet.name,
            histories=Wallet.histories)

    def to_entity(self) -> Wallet:
        return Wallet.model_validate(self)

class WalletRepository:
    async def add(
        self, session: AsyncSession, name: str
    ) -> Wallet:
        wallet = WalletORM(name=name, histories=[])
        session.add(wallet)
        await session.flush()
        return wallet.to_entity()

    async def get_by_id(
        self,
        session: AsyncSession,
        wallet_id: int,
    ) -> Wallet | None:
        stmt = (
            select(WalletORM)
            .where(WalletORM.wallet_id == wallet_id)
            .options(
                selectinload(WalletORM.histories)
            ))
        wallet = await session.scalar(stmt)
        if not wallet:
            return None
        return wallet.to_entity()
    
    async def get_all(
        self, session: AsyncSession
    ) -> list[Wallet]:
        stmt = select(WalletORM).options(
            selectinload(WalletORM.histories))
        return [
            wallet.to_entity()
            for wallet in await session.scalars(stmt)
        ]
    
    async def add_history(
        self,
        session: AsyncSession,
        wallet_id: int,
        name: str,
        amount: int,
        type_: HistoryType,
        history_at: datetime,
    ) -> History:
        stmt = (
            select(WalletORM)
            .where(WalletORM.wallet_id == wallet_id)
            .options(
                selectinload(WalletORM.histories)
            ))
        wallet = await session.scalar(stmt)
        if not wallet:
            raise AppException()
        
        history = HistoriyORM(
            name=name,
            amount=amount,
            type=type_,
            history_at=history_at,
            wallet_id=wallet.wallet_id,
        )
        wallet.histories.append(history)
        await session.flush()
        return history.to_entity()