from datetime import datetime
from app.models import History, HistoryType
from app.utils.datetime import utcnow

class ListHistories:
    async def execute(
        self, wallet_id: int
    ) -> list[History]:
        return []
    
class GetHistory:
    async def execute(
        self,
        wallet_id: int,
        history_id: int,
    ) -> History:
        return History(
            wallet_id = wallet_id,
            history_id = history_id,
            name = "",
            amount = 10,
            type = HistoryType.INCOME,
            history_at = utcnow(),
        )