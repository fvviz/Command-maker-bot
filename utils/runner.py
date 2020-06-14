from utils.commandMaker import CommandMaker


async def run(ctx, name, bot):
    try:
        commandMaker = CommandMaker("text", ctx.guild, bot)
        output = commandMaker.run_text_command(name)
        await ctx.send(output)
    except Exception:
        try:
            commandMaker = CommandMaker("choice", ctx.guild, bot)
            output = commandMaker.run_choice_command(name)
            await ctx.send(output)
        except Exception:
            commandMaker = CommandMaker("embed", ctx.guild, bot)
            output = commandMaker.run_embed_command(name)
            await ctx.send(embed=output)