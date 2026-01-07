import os
import asyncio

from aiohttp import web
from bot_service import run_bot


async def start_background_bot(app: web.Application):
    # ربات را به صورت task بک‌گراند ران می‌کنیم
    app["bot_task"] = asyncio.create_task(run_bot())


async def cleanup_background_bot(app: web.Application):
    # هنگام shut down سرویس، ربات را تمیز قطع می‌کنیم
    bot_task = app.get("bot_task")
    if bot_task:
        bot_task.cancel()
        try:
            await bot_task
        except asyncio.CancelledError:
            pass


async def healthcheck(request: web.Request):
    return web.Response(text="OK")


def main():
    app = web.Application()
    app.router.add_get("/", healthcheck)

    app.on_startup.append(start_background_bot)
    app.on_cleanup.append(cleanup_background_bot)

    port = int(os.environ.get("PORT", "8000"))
    web.run_app(app, port=port)


if __name__ == "__main__":
    main()
