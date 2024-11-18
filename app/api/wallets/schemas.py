from pydantic import Field
from app.models import BaseModel
from .histories.schemas import History

class Wallet(BaseModel):
    wallet_id: int
    name: str
    balance: int = Field(
        ...,description="現在時点の予算")

class GetWalletsResponse(BaseModel):
    wallets: list[Wallet]
    
class GetWalletResponse(Wallet):
    pass

class GetWalletsResponseWithHistoies(Wallet):
    hisotries: list[History] = Field(
        ...,description="関連する収支項目一覧")