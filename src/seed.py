import asyncio

from admin_app.seed import fill_database as fill_sqla_database


async def main():
    print("Start filling SQLModel database")
    await fill_sqla_database()
    print("End filling SQLModel database")



asyncio.run(main())