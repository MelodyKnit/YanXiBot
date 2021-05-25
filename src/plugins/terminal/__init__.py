from nonebot import on_command
from nonebot.permission import SUPERUSER
from subprocess import Popen, PIPE, STDOUT
from nonebot.adapters.cqhttp import Bot, MessageEvent
from .commands import commands
terminal = on_command("cmd", permission=SUPERUSER)


def decode(byte: bytes) -> str:
    try:
        return byte.decode("gbk")
    except UnicodeDecodeError:
        return byte.decode("utf-8")


@terminal.handle()
async def terminal_handle(bot: Bot, event: MessageEvent):
    cmd = event.get_plaintext()
    if cmd:
        if cmd in commands:
            output = await commands.get(cmd)()
            await terminal.finish(output)

        with Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT) as p:
            with p:
                output = decode(p.stdout.read())
        await terminal.finish(output)
