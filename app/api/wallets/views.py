from typing import Annotated
from fastapi import APIRouter, Depends, Query, status
from app.routes import loggingRoute
from .schemas import (
    GetWalletResponse,
    GetWalletsResponseWithHistoies,
    GetWalletsResponse,
    Wallet,
)
from .usecases import (
    GetWallet,
    ListWallets,
)
from .histories.views import (
    router as histories_router
)

router = APIRouter(
    prefix="/v1/wallets", route_class=loggingRoute
)

@router.get("", response_model=GetWalletsResponse)
async def get_wallets(
    use_case: Annotated[
        ListWallets, Depends(ListWallets)
    ]
) -> GetWalletsResponse:
    return GetWalletsResponse(
        wallets = [Wallet.model_validate(w)
                   for w in await use_case.execute()]
    )

@router.get(
    "/{wallet_id}",
    response_model=GetWalletsResponseWithHistoies | GetWallet
)
async def get_wallet(
    wallet_id: int,
    use_case: Annotated[
        GetWallet, Depends(GetWallet)
    ],
    include_histories: bool = Query(
        False,
        description="収支項目一覧も返すか否か",
    ),
) -> (GetWalletsResponseWithHistoies | GetWalletResponse):
    result = await use_case.execute(
        wallet_id=wallet_id
    )
    if include_histories:
        return (
            GetWalletsResponseWithHistoies.model_validate(result)
        )
    return GetWalletResponse.model_validate(result)

router.include_router(
    histories_router, prefix="/{wallet_id}"
)