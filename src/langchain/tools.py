from src.database.database import Database

async def update_user_name_tool(thread_id: int, name: str) -> str:
    db = Database()
    # Aquí deberías tener un método async, pero para ejemplo lo dejamos sync
    # Si tu método es async, deberías adaptarlo con asyncio.run o similar
    #await db.save_user_name(thread_id, name)
    #return f"Nombre actualizado a {name}."
    pass