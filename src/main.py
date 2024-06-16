import mcon

watchdog = mcon.from_config("./config.jsonc")


@watchdog.command("playerlist")
async def _(result: mcon.Command):
    pass


watchdog.start()