import os
import asyncio

from aiohttp import web
from bot import run_bot


async def start_background_bot(app: web.Application):
    app["bot_task"] = asyncio.create_task(run_bot())


async def cleanup_background_bot(app: web.Application):
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
