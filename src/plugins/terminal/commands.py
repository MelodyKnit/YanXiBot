from psutil import cpu_percent, virtual_memory, disk_usage


async def system_status():
    return (f"Memory: {virtual_memory().percent}%\n"
            f"Disk: {disk_usage('/').percent}%\n"
            f"Cpu: {cpu_percent()}%")


commands = {
    "status": system_status
}

__all__ = [
    "commands"
]
