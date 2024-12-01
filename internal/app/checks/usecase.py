from internal.app.checks.repository import CheckRepository
from pkg.jwt_utils import decode_jwt

class CheckUseCase:
    def __init__(self, repo: CheckRepository):
        self.repo = repo

    async def get_checks(self, token: str):
        user_id = decode_jwt(token)
        if not user_id:
            raise ValueError("Invalid token")
        
        checks = await self.repo.get_checks_by_user_id(user_id)
        
        grouped_checks = {}
        for check in checks:
            paycheck_id = check['paycheck_id']
            if paycheck_id not in grouped_checks:
                grouped_checks[paycheck_id] = {
                    "paycheck_id": paycheck_id,
                    "creation_datetime": check["creation_datetime"],
                    "products": []
                }
            grouped_checks[paycheck_id]["products"].append({
                "product_id": check["product_id"],
                "product_name": check["product_name"],
                "price": check["price"]
            })
        return list(grouped_checks.values())