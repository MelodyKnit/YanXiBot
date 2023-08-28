from functools import wraps, partial
from typing_extensions import ParamSpec
from typing import Any, TypeVar, Callable, Coroutine

import anyio

P = ParamSpec("P")
R = TypeVar("R")


def run_sync(func: Callable[P, R]) -> Callable[P, Coroutine[Any, Any, R]]:
    @wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        return await anyio.to_thread.run_sync(partial(func, *args, **kwargs))

    return wrapper


def run_async(func: Callable[P, Coroutine[Any, Any, R]]) -> Callable[P, R]:
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        return anyio.from_thread.run(partial(func, *args, **kwargs))

    return wrapper