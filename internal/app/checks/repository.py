class CheckRepository:
    def __init__(self, db):
        self.db = db

    async def get_checks_by_user_id(self, user_id: str):
        query = """
        SELECT 
            pc.paycheck_id,
            pc.creation_datetime,
            p.id as product_id,
            p.name as product_name,
            p.price
        FROM public.paychecks pc
        JOIN public.products p ON pc.product_id = p.id
        WHERE pc.user_id = $1
        ORDER BY pc.creation_datetime DESC
        """
        async with self.db.pool.acquire() as conn:
            rows = await conn.fetch(query, user_id)
            return [dict(row) for row in rows]
