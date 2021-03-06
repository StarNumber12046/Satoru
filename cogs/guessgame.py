import discord 
from discord.ext import commands

class GuessGame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def guessgame(self, ctx):
        "I'll try to guess a number you're thinking with the binary search!"

        emb = discord.Embed(title = "Guess Game", description = "I'll try to guess a number you're thinking!\nType a range so I can guess the number (ex. `0 - 200` or `45 - 56`)", colour = self.bot.colour)
        emb.set_author(name = ctx.author, icon_url = str(ctx.author.avatar_url_as(static_format = "png")))
        msg = await ctx.send(embed = emb)

        def check(message):
            return message.channel == ctx.channel and message.author == ctx.author

        end = False

        while not end:

            try:
                m = await self.bot.wait_for("message", check = check, timeout = 120)

            except KeyError:
                emb.description = "Time out!"
                emb.colour = discord.Colour.red()
                return await msg.edit(content = None, embed = emb)

            range = m.content

            if " " in range:
                range = range.split(" - ")

            else:
                range = range.split("-")

            if len(range) != 2:
                emb.description = "not a valid format! Give me a range using this format: `0 - 100` or `40 - 65`"
                await msg.edit(content = None, embed = emb)
                end = False

            else:
                end_ = []
                for num in range:
                    try:
                        num = int(num)
                    except ValueError:
                        end_.append(1)
                    else:
                        end_.append(0)

                if 1 in end_:
                    emb.description = "not a valid format! Give me a range using this format: `0 - 100` or `40 - 65`"
                    await msg.edit(content = None, embed = emb)
                    end = False

                else:
                    end = True

        rangeA = int(range[0])
        rangeB = int(range[1])

        if rangeA > rangeB:
            a = rangeA
            b = rangeB
            rangeA = b
            rangeB = a

        def reaction_check(reaction, user):
            return reaction.message.id == msg.id and user.id == ctx.author.id and str(reaction.emoji) in ["🇦", "🇧", "🇨"]

        passed = False

        count = 0

        while not passed:

            count += 1
            emb.description = f'Is your number **{round((rangeB + rangeA) / 2)}**?\n\n`A` (yes)\n`B` (major)\n`C` (minor)'
            
            await msg.edit(content = None, embed = emb)
            await msg.add_reaction("🇦")
            await msg.add_reaction("🇧")
            await msg.add_reaction("🇨")

            try:
                reaction, user = await self.bot.wait_for("reaction_add", check = reaction_check, timeout = 120)

            except KeyError:
                emb.description = "Time out!"
                emb.colour = discord.Colour.red()
                return await msg.edit(content = None, embed = emb)

            if str(reaction.emoji) == "🇦":
                passed = True

            elif str(reaction.emoji) == "🇧":
                rangeA = (rangeB + rangeA) / 2
                passed = False

            elif str(reaction.emoji) == "🇨":
                rangeB = (rangeB + rangeA) / 2
                passed = False

        emb.description = f"GG! I won in **{count}** tries!"
        await msg.edit(content = None, embed = emb)

def setup(bot):
    bot.add_cog(GuessGame(bot))