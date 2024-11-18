from typing import Annotated
from fastapi import Depends
from sqlalchemy import Connection, inspect
from app.repositories import (
    BaseORM,
    WalletRepository as _WalletRepository,
)

async def craete_database_if_not_exist() -> None:
    def create_tables_if_not_exist(
        sync_conn: Connection
    ) -> None:
        if not inspect(sync_conn.engine).has_table(
            "wallets"
        ):
            BaseORM.metadata.create_all(
                sync_conn.engine)
    
    async with async_engine.connect() as conn:
        await conn.run_sync(
            create_tables_if_not_exist)

WalletRepository = Annotated[
    _WalletRepository, Depends(_WalletRepository)
]