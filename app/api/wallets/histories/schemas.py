from datetime import datetime
from pydantic import Field, PositiveInt
from app.models import BaseModel, HistoryType
from app.models import UTCDatetime
from app.utils.datetime import utcnow

class History(BaseModel):
    history_id: int
    name: str
    amount: PositiveInt
    type: HistoryType = Field(
        ...,description="INCOME:収入、OUTCOME:支出")
    history_at: UTCDatetime = Field(
        ...,description="収支項目の発生日時(UTC)")
    
class GetHistoryResponse(History):
    pass

class GetHistoriesResponse(BaseModel):
    histories: list[History]
    
class MoveHistoryRequest(BaseModel):
    destination_id: int = Field(
        ...,description="移動先のWalletのID")

class MoveHistoryResponse(History):
    pass