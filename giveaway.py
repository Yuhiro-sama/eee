
import re
import discord
from discord.ext import commands
import asyncio
import random
from datetime import datetime
import datetime

# current date and time

time_regex = re.compile("(?:(\d{1,5})(h|s|m|d))+?")
time_dict = {"h":3600, "s":1, "m":60, "d":86400}


class TimeConverter(commands.Converter):
    async def convert(self, ctx, argument):
        args = argument.lower()
        matches = re.findall(time_regex, args)
        time = 0
        for v, k in matches:
            try:
                time += time_dict[k]*float(v)
            except KeyError:
                raise commands.BadArgument("{} is an invalid time-key! h/m/s/d are valid!".format(k))
            except ValueError:
                raise commands.BadArgument("{} is not a number!".format(v))
            if time != 0:
                return time
            if time == 0:
                await ctx.send("{} is an invalid time-key! h/m/s/d are valid!".format(argument))

class Giveaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def gstart(self, ctx, price:str = None, *, time:TimeConverter):
        
        
        colour = ctx.guild.me.top_role.colour
        if time == None:
            return await ctx.send("Specify a time")
        
        if price == None:
            return await ctx.send("Specify a price")

        await ctx.message.delete()
        
        #TIME 
        
        
        date = f"{str(ctx.message.created_at)}"
        

        # convert string to datetimeformat
        date = datetime.datetime.strptime(f"{str(date)[:-7]}", "%Y-%m-%d %H:%M:%S")

        # convert datetime to timestamp
        date = datetime.datetime.timestamp(date)

        times = date + time + 3600 # because of the time difference
        
        
        #BEFORE GIVEAWAYS ENDS
        before = discord.Embed(title=f"{price}",description=f"React with 🎉 to enter\nEnds : <t:{str(times)[:-2]}:R> (<t:{str(times)[:-2]}:F>)\n Hosted by : {ctx.author.mention}",color=colour , timestamp=ctx.message.created_at)
        before.set_footer(text=f"Created at")
        await ctx.send("🎉 GIVEAWAY 🎉")
        gmsg = await ctx.send(embed=before)
        # everyone mention 
        # await ctx.send(ctx.message.guild.default_role)

        await gmsg.add_reaction("🎉")
        await asyncio.sleep(time)

        nowy_gmsg = await ctx.channel.fetch_message(gmsg.id)

        users = await nowy_gmsg.reactions[0].users().flatten()
        users.pop(users.index(self.bot.user))
        if len(users) == 0:
            afters = discord.Embed(title=f"{price}",description=f"Already finished\nEnds : <t:{str(times)[:-2]}:R> (<t:{str(times)[:-2]}:F>)\n Hosted by : {ctx.author.mention}\n Winner : No winner", color=colour, timestamp=ctx.message.created_at)
            afters.set_footer(text=f"Created at")
            await gmsg.edit(embed=afters)
            await gmsg.clear_reaction("🎉")
            # await ctx.send("No winner")
            return
        winner = random.choice(users)
        
        if ctx.author == users:
            winner = random.choice(users)
        else:
            pass
            
        # AFTER GIVEAWAY'S ENDS
        after = discord.Embed(title=f"{price}",description=f"Already finished\nEnds : <t:{str(times)[:-2]}:R> (<t:{str(times)[:-2]}:F>)\n Hosted by : {ctx.author.mention}\n Winner : {winner.mention}", color=colour, timestamp=ctx.message.created_at)
        after.set_footer(text=f"Created at")
        await gmsg.edit(embed=after)
        # await gmsg.clear_reaction("🎉")
        await ctx.send(f"🎊 Good job {winner.mention} ! You win : {price}! 🎊")
        
        
    @commands.command()
    async def greroll(self, ctx, channel : discord.TextChannel = None, id_ : int = None):
        if not channel:
            return await ctx.send("Please specify a channel")
        if not id_:
            return await ctx.send("Please specify a ID")
        try:
            new_msg = await channel.fetch_message(id_)
        except:
            await ctx.send("The ID is wrong !")
        
        users = await new_msg.reactions[0].users().flatten()
        users.pop(users.index(self.bot.user))
        if len(users) == 0:
            return await ctx.send("No winner")
        winner = random.choice(users)

        await channel.send(f"🎊 Good job {winner.mention}! You win ! 🎊")

def setup(bot):
    bot.add_cog(Giveaway(bot))
            
            
            
            