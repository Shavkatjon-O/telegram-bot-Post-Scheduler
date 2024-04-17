from aiogram import Router


def get_handlers_rounter() -> Router:
    from . import start, admin, chat, post, help

    router = Router()
    router.include_router(start.router)
    router.include_router(admin.router)
    router.include_router(chat.router)
    router.include_router(post.router)
    router.include_router(help.router)

    return router
