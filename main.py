import discord
from discord import client
from discord import message
from discord.ext import commands
from discord.ext.commands.core import command
from discord.utils import get
import os
from replit import db

if 'gMembers' in db.keys():
  del db["gMembers"]

#database function for members
def update_gMembers(nuMember):
  if 'gMembers' in db:
    gMembers = db['gMembers']
    gMembers.append(nuMember)
    db['gMembers'] = gMembers
  else:
    db['gMembers'] = [nuMember]

intents=discord.Intents.all()
client = commands.Bot(command_prefix='$',intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

#greet new member
@client.event
async def on_member_join(member):
    print(member)
    channel = discord.utils.get(member.guild.text_channels, name="general")
    await channel.send(f"{member} has arrived!\n Have a pleasant stay {member}")

#announcing member reaction
@client.event
async def on_raw_reaction_add(reaction):
    channel=client.get_channel(reaction.channel_id)
    message=await channel.fetch_message(reaction.message_id)
    if(reaction.emoji.id==None):
        emoji=reaction.emoji.name
    else:
        emoji=f"<:{reaction.emoji.name}:{reaction.emoji.id}>"
    await channel.send(f"{reaction.member.name} reacted with {emoji} to {message.author.name}'s message")

#assign roles to member
@client.command()
async def role(ctx,*args):
    if(len(args)>0):
        member=ctx.author
        role = get(ctx.guild.roles,name=args[0])
        if(role==None):
            role=await ctx.guild.create_role(name=args[0])
        print(member,role)
        await member.add_roles(role)

#register name to database
@client.command()
async def register(ctx,*args):
  if(len(args)<0):
    await ctx.send('Enter valid name')
  else:
    nuMember = args[0]
    update_gMembers(nuMember)
    await ctx.send("Registered successfully to database")

#retrieve all names in database
@client.command()
@commands.has_role('superman')
async def names(ctx):
  for i in db['gMembers']:
    await ctx.send(i)
      

client.run(os.getenv('TOKEN'))