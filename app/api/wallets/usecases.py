from app.models import Wallet
from app.database import (
    AsyncSession,
    WalletRepository
)
from app.exceptions import NotFound

class ListWallets:
    def __init__(
        self,
        session: AsyncSession,
        repo: WalletRepository,
    ) -> None:
        self.session = session
        self.repo = repo

    async def execute(self) -> list[Wallet]:
        async with self.session() as session:
            wallets = await self.repo.get_all(session)
        return wallets
    
class GetWallet:
    def __init__(
        self,
        session: AsyncSession,
        repo: WalletRepository,
    ) -> None:
        self.session = session
        self.repo = repo

    async def execute(
        self, wallet_id: int
    ) -> Wallet:
        async with self.session() as session:
            wallet = self.repo.get_by_id(
                session, wallet_id)
            if not wallet:
                raise NotFound("wallet", wallet_id)
        return wallet

class CreateWallet:
    def __init__(
        self,
        session: AsyncSession,
        repo: WalletRepository,
    ) -> None:
        self.session = session
        self.repo = repo
    
    async def execute(self, name: str) -> Wallet:
        async with self.session as session:
            wallet = await self.repo.add(session, name)
            return wallet