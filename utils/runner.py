from utils.commandMaker import CommandMaker


async def exec(ctx, name, bot):
    try:
        commandMaker = CommandMaker("text", ctx.guild, bot)
        output = commandMaker.run_text_command(name,ctx)
        await ctx.send(output)
    except Exception:
        try:
            commandMaker = CommandMaker("choice", ctx.guild, bot)
            output = commandMaker.run_choice_command(name)
            await ctx.send(output)
        except Exception:

            try:
                commandMaker = CommandMaker("embed", ctx.guild, bot)
                output = commandMaker.run_embed_command(name)
                await ctx.send(embed=output)
            except Exception:
                commandMaker = CommandMaker("ce", ctx.guild, bot)
                output = commandMaker.run_ce_command(name)
                await ctx.send(embed=output)
