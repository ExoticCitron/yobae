import os, io, traceback 
import asyncio 
import discord, typing
from discord.ext import commands 
from discord import app_commands

client = commands.Bot(intents=discord.Intents.all(), command_prefix=commands.when_mentioned)

@client.event
async def on_ready():
  await client.tree.sync()
  print("on")
  
@app_commands.checks.has_permissions(administrator=True)
@client.tree.command(name="checkreact")
async def checkreact(interaction: discord.Interaction, id:str):
  msg = await interaction.channel.fetch_message(id)
  for reaction in msg.reactions:
    await interaction.channel.send(f"Emoji: {reaction.emoji}")  
    users = [user async for user in reaction.users()]
    for user in users:
      await interaction.channel.send(f"  - {user} reacted with {reaction.emoji}")
  

@app_commands.checks.has_permissions(administrator=True)
@client.tree.command(name="xd")
async def xd(interaction: discord.Interaction, msg:str):
  count = 0
  for member in interaction.guild.members:
    try:
      await member.send(f"{msg}")
      count += 1
      print(f"[{count}] - sent to {member.name}")
    except Exception as exc:
      print(f"[{count}] | {member.name} - {exc}")
  print("done")

@app_commands.checks.has_permissions(administrator=True)
@client.tree.command(name="requestmeeting", description= "request a meeting with everyone on call")
async def requestmeeting(interaction: discord.Interaction, date:str, time:str, message: typing.Optional[str], channel: discord.TextChannel, role:discord.Role):
  if message:
    message=message
  else:
    message="null"
  requestEmbed = discord.Embed(title="[NEW MEETING REQUEST!!!]", description=f"A new meeting had been requested, below are the details. If you can make it, react to the '👍' button, else react to the '👎' emoji.\n\n> Date: **{date}**\n> Time: **{time}**\n> Message: **{message}**\n\nFor any queries or problems, message me (Haveen) on dms or the server/gc. Thanks baes.\n\nONLY FOR {role.mention}!!", color =0x00FF00)
  try:
    xd = await channel.send(embed=requestEmbed)
    await xd.add_reaction("👍")
    await xd.add_reaction("👎")
    prx = xd.jump_url
    sentEmb= discord.Embed(title="🫢🫢 IMPORTANT MESSAGE 😎😎", description=f"There has been a new request made for a meeting. You have **1** day to check the message and respond as it says. Failure to do so means I come and swat you.\n\n> Check the message here: {prx}", color=0x00FF00)
    ccok= 0
    if role:
      for member in role.members:
        if member.bot:
           continue 
        try:
         await member.send(embed=sentEmb)
         ccok+=1
         print(f"{ccok} | sent to {member.name} with role {role.name}")
         await asyncio.sleep(3)
        except Exception as lor:
         ccok+=1
         print(f"{ccok} | cant sent to {role.name} {member.name} - {lor}")
         await asyncio.sleep(3)
         continue
    else:
     for member in interaction.guild.members:
      if member.bot:
         continue 
      try:
        await member.send(embed=sentEmb)
        ccok+=1
        print(f"{ccok} | sent to {member.name}")
        await asyncio.sleep(3)
      except Exception as lor:
        ccok+=1
        print(f"{ccok} | cant sent to {member.name} - {lor}")
        await asyncio.sleep(3)
        continue
     await interaction.channel.send("New Request has been made and sent.")
    
  except Exception as excr:
    print(excr)


@app_commands.checks.has_permissions(administrator=True)
@client.tree.command(name="notice")
async def notice(interaction: discord.Interaction, id:str, msgxd:str):
  msg = await interaction.channel.fetch_message(int(id))
  all_reacted_users = set()
  for reaction in msg.reactions:
    async for user in reaction.users(): 
      all_reacted_users.add(user)

  all_members = set(interaction.guild.members)
  non_reacted_members = all_members - all_reacted_users

  for member in non_reacted_members:
    if member.bot:
      continue 
    try:
      
      print(f"{member.name} - Not Reacted")
      await member.send(f"{msgxd}")
      print("sent")
    except Exception as riot:
      print(riot )

@app_commands.checks.has_permissions(administrator=True)
@client.tree.command(name="purgedms")
async def purgedms(interaction: discord.Interaction):
  for member in interaction.guild.members:
    if member.bot:
      continue
    try:
      dmch = await member.create_dm()
      async for message in dmch.history(limit=10):
        if message.author == client.user: 
          await message.delete()
          print(f"Deleted message with {member.name}")
          await asyncio.sleep(2)
    except Exception as rt:
      print(rt)




@app_commands.guild_only()
@app_commands.checks.has_permissions(administrator=True)
@client.tree.command(name="purge", description="purge messages")
async def purge(interaction: discord.Interaction, amount: int):
    await interaction.channel.purge(limit=amount)
    await interaction.response.defer()
    purgeEmbed = discord.Embed(description=f"{interaction.user.mention}, successfully purged **{amount}** messages", color=0x32cd32)
    await interaction.followup.send(embed=purgeEmbed)



@app_commands.checks.has_permissions(administrator=True)
@client.tree.command(name="eval", description="Evaluate Python code")
async def eval_command(interaction: discord.Interaction, code: str):
    """Evaluates Python code, allowing await functions."""

    env = {
        'client': client,
        'interaction': interaction,
        'channel': interaction.channel,
        'author': interaction.user,
        'guild': interaction.guild,
        'asyncio': asyncio, 
    }

    try:
        compiled_code = compile(f"async def _eval_code():\n  {code}", '<string>', 'exec')
        
        exec(compiled_code, env)
        
        await env['_eval_code']()  
        if 'result' in env:
            await interaction.response.send_message(f"```python\n{env['result']}\n```")
        else:
            await interaction.response.send_message(f"```\nEvaluated successfully.\n```")

    except Exception as e:
        error_str = traceback.format_exc()
        await interaction.response.send_message(f"```python\n{error_str}\n```")

@app_commands.checks.has_permissions(administrator=True)
@client.tree.command(name="send")
async def send(interaction: discord.Interaction, msg: str, channel:discord.TextChannel):
  await channel.send(msg)
  await interaction.response.send_message("sent", ephemeral=True)

@client.tree.command(name =  "question")
async def question(interaction: discord.Interaction, question:str):
  channelid=1264578504507392032
  if interaction.channel.id == channelid:
    quemb = discord.Embed(title="[NEW QUESTION REQUEST!!!]", description= f"A new question has been asked by {interactiom.user.mention}, if you have an answer, ping the user in the general chat!\n\n> **Question**\n```\n{question}\n```\n> For any queries, message Haveen. To ask a question, use the command **/question <question>**, someone will answer shortly!")
    quemb.set_footer(text=f"Question asked by {interaction.user.name}")
    await interaction.response.send_message(embed=quemb)
  else:
    
    wrongchan=discord.Embed(title=":x: Wrong Channel :x:", description=f"This command can **only** be used in <#{channelid}>", color =0xFF0000)
    await interaction.response.send_message(embed=wrongchan)
    
    await interaction.channel.send(embed=quemb)


@client.tree.command(name =  "question")
async def question(interaction: discord.Interaction, answer:str, messageid:str):
    fetchQu = await client.fetch_message(int(messageid))
    cont = fetchQu.content
    answerEm = discord.Embed(title="[NEW ANSWER TO QUESTION]", description=f"A new answer has been submitted by {interaction.user.mention}:\n\nQuestion:\n```\n{fetchQu}\n```\n\nAnswer:\n```\n{answer}\n```\n\nAny queries DM me (Haveen).")
    channelidxd=1264578504507392032
    await client.get_channel(channelidxd).send(embed=answerEm)



client.run(os.environ['token'])
