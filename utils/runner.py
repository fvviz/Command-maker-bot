from utils.commandMaker import CommandMaker
from utils.helperFuncs import *

async def exec(ctx, name, bot):
    try:
        commandMaker = CommandMaker("text", ctx.guild, bot)
        output = commandMaker.run_text_command(name,ctx)
        await ctx.send(output)
    except Exception:
        try:
            commandMaker = CommandMaker("choice", ctx.guild, bot)
            output = commandMaker.run_choice_command(ctx,name)
            await ctx.send(output)
        except Exception:

            try:
                commandMaker = CommandMaker("embed", ctx.guild, bot)
                output = commandMaker.run_embed_command(name)
                await ctx.send(embed=output)
            except Exception:
                try:
                    commandMaker = CommandMaker("ce", ctx.guild, bot)
                    output = commandMaker.run_ce_command(name)

                    if commandMaker.get_ce_image(ctx, name, "image") is not None:
                        img = commandMaker.get_ce_image(ctx, name, "image")
                        output.set_image(url=img)

                    if commandMaker.get_ce_image(ctx, name, "thumbnail") is not None:
                        img = commandMaker.get_ce_image(ctx, name, "thumbnail")
                        output.set_thumbnail(url=img)

                    auth_dict = commandMaker.get_ce_dict(ctx, name, "author")
                    footer_dict = commandMaker.get_ce_dict(ctx, name, "footer")

                    processed_output = process_embed(ctx, output, auth_dict, footer_dict)

                    await ctx.send(embed=processed_output)
                except:
                    commandMaker = CommandMaker("rate", ctx.guild, bot)
                    output = commandMaker.run_rate_command(ctx,name)
                    await ctx.send(output)










