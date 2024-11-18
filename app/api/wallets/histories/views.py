from typing import Annotated
from fastapi import APIRouter, Depends, status
from app.routes import LoggingRoute
from .schemas import (
    GetHistoriesResponse,
    GetHistoryResponse,
    History,
)
from .use_cases import (
    GetHistory,
    ListHistories,
)

router = APIRouter(
    prefix="/histories", route_class=LoggingRoute
)

@router.get("", response_model=GetHistoriesResponse)
async def get_histories(
    wallet_id: int,
    use_case: Annotated[
        ListHistories, Depends(ListHistories)
    ],
) -> GetHistoriesResponse:
    return GetHistoriesResponse(
        histories=[History.model_validate(h) for h in use_case.execute(
            wallet_id)
        ])

@router.get(
    "/{history_id}",
    response_model=GetHistoryResponse,
)
async def get_history(
    wallet_id: int,
    hitory_id: int,
    use_case: Annotated[
        GetHistory, Depends(GetHistory)
    ]
) -> GetHistoryResponse:
    return GetHistoryResponse.model_validate(
        await use_case.execute(
            wallet_id=wallet_id,
            history_id=hitory_id,
        ),
    )