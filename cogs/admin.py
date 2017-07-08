"""
tools for the bot admin
"""

import os
import sys
import json
import inspect

import discord
from discord.ext import commands


class Admin:
  def __init__(self, bot_):
    self.bot = bot_
    with open('config.json') as file_in:
      self.config = json.load(file_in)

  @commands.command(name="gitpull", hidden=True)
  async def gitpull(self):
    if not ctx.message.author.id in self.config['admin_ids']: return
    os.popen("git pull origin master")
    await self.bot.say("Done!")

  @commands.command(name="restart", hidden=True)
  async def restart(self):
    if not ctx.message.author.id in self.config['admin_ids']: return
    await self.bot.say("Restarting bot...")
    python = sys.executable
    os.execl(python, python, * sys.argv)

  @commands.command(name="exit", hidden=True)
  async def stop(self):
    if not ctx.message.author.id in self.config['admin_ids']: return
    await self.bot.say("Stopping bot...")
    sys.exit()

  @commands.command(name="oinvite", pass_context=True, hidden=True)
  async def get_server_invite(self, ctx, *server):
    if not ctx.message.author.id in self.config['admin_ids']: return
    if not self.bot.get_server(server[0]) is None:
      invite = await self.bot.create_invite(self.bot.get_server(server[0]))
      await self.bot.send_message(ctx.message.author, invite.url)

  @commands.command(pass_context=True, hidden=True)
  async def debug(self, ctx, *, code: str):
    """Evaluates code."""
    if not ctx.message.author.id in self.config['admin_ids']: return

    code = code.strip('` ')
    python = '```py\n{}\n```'
    result = None

    env = {
      'bot': self.bot,
      'ctx': ctx,
      'message': ctx.message,
      'server': ctx.message.server,
      'channel': ctx.message.channel,
      'author': ctx.message.author
    }

    env.update(globals())
    env.update(locals())

    try:
      result = eval(code, env)
      if inspect.isawaitable(result):
        result = await result
    except Exception as e:
      await self.bot.say(python.format(type(e).__name__ + ': ' + str(e)))
      return

    await self.bot.say(python.format(result))


def setup(bot):
  bot.add_cog(Admin(bot))
