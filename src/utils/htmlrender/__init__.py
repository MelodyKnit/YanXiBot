from imgkit import from_string
from ...utils import run_sync


async def html_to_image(html: str, options: dict | None = None, width=600) -> bytes:
    return await run_sync(from_string)(  # type: ignore
        html,
        None,
        options={
            "width": width,
            "encoding": "UTF-8",
        }
        | (options or {}),
    )