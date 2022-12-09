import os
import discord
import requests
import json
from discord.commands import Option

activity = discord.Activity(name='Literally on fire | /help', type=discord.ActivityType.playing)
bot = discord.Bot(activity=activity)
token = os.environ['TOKEN']
gids = [954871789224329357,586582883641065481]


#Database setup
apikey = os.environ['apikey']
urlfind = "https://data.mongodb-api.com/app/data-lvmlg/endpoint/data/v1/action/findOne"
urlinsert = "https://data.mongodb-api.com/app/data-lvmlg/endpoint/data/v1/action/insertOne"
urldel = "https://data.mongodb-api.com/app/data-lvmlg/endpoint/data/v1/action/deleteOne"
urlupdate = "https://data.mongodb-api.com/app/data-lvmlg/endpoint/data/v1/action/updateOne"

headers = {
  'Content-Type': 'application/json',
  'Access-Control-Request-Headers': '*',
  'api-key': apikey, 

}
async def findDB(coll,dtb,dts,fnd):
  global urlfind
  global headers
  payload = json.dumps({
    "collection": coll,
    "database": dtb,
    "dataSource": dts,
    "filter":fnd
  })
  response = requests.request("POST", urlfind, headers=headers, data=payload)
  return response.text
  
async def insertDB(coll,dtb,dts,inst):
  global urlinsert
  global headers
  payload = json.dumps({
    "collection": coll,
    "database": dtb,
    "dataSource": dts,
    "document":inst
  })
  response = requests.request("POST", urlinsert, headers=headers, data=payload)
  return response.text

async def delDB(coll,dtb,dts,fnd):
  global urldel
  global headers
  payload = json.dumps({
    "collection": coll,
    "database": dtb,
    "dataSource": dts,
    "filter":fnd
  })
  response = requests.request("POST", urldel, headers=headers, data=payload)
  return response.text
  
async def updateDB(coll,dtb,dts,fnd,upt):
  global urlupdate
  global headers
  payload = json.dumps({
    "collection": coll,
    "database": dtb,
    "dataSource": dts,
    "filter":fnd,
    "update": {"$set":upt}
  })
  response = requests.request("POST", urlupdate, headers=headers, data=payload)
  return response.text

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

#commands

#hello
@bot.slash_command(guild_ids=gids)
async def hello(ctx):
    await ctx.respond("Hello, "+str(ctx.author)+"!")

#help
@bot.slash_command(guild_ids=gids)
async def help(ctx):
  embed=discord.Embed(title="Help", description="Help page for LitBot!", color=0x509ef2)
  embed.add_field(name="/help", value="Shows this page.", inline=False)
  embed.add_field(name="/hello", value="Says hello back!", inline=False)
  embed.add_field(name="/createprofile", value="Creates a profile that other users can see by using the /showprofile command.", inline=False)
  embed.add_field(name="/showprofile", value="Shows the profile of a specific user.", inline=False)
  embed.add_field(name="/deleteprofile", value="Deletes your profile.", inline=False)
  embed.add_field(name="/dadjoke", value="Says a random dad joke.", inline=False)
  embed.add_field(name="/cat", value="Displays a random picture of a cat.", inline=False)
  
  await ctx.respond(embed=embed)

  
#profile system (i hope this works) (yay it works) 

  #create profile
@bot.slash_command(guild_ids=gids)
async def createprofile(ctx, name, age, birthday: Option(str, "Enter your birthday", required = False, default = '')):
  if 1==0:
    await ctx.respond("You already have a profile!")
  else:
    await ctx.respond("Creating profile...")
    await insertDB("Level", "Userdata", "TheBestDB", {"name":name,"age":age,"bday":birthday,"id":str(ctx.author.id)})
    await ctx.respond("Profile created!")

  #show profile
@bot.slash_command(guild_ids=gids)
async def showprofile(ctx,user):
  try:
    await ctx.respond("Loading profile...")
    x = user.replace('<','')
    y = x.replace('>', '')
    g = y.replace('@','')
  
    a = await findDB("Level", "Userdata", "TheBestDB", {"id":str(g)})
    b = json.loads(a)
    c = b["document"]
    embed=discord.Embed(title="Profile of "+c["name"],color=0x509ef2)
    #embed.add_field(name="Name: ", value="undefined", inline=False)
    embed.add_field(name="Age:", value=c["age"], inline=False)
    embed.add_field(name="Birthday:", value=c["bday"], inline=False)
    embed.add_field(name="Id:", value=c["id"], inline=False)
    await ctx.respond(embed = embed)
  except:
    await ctx.respond("Profile not found! :(")

  #delete profile
@bot.slash_command(guild_ids=gids)
async def deleteprofile(ctx):
  await ctx.respond("Deleting profile...")
  await delDB("Level", "Userdata", "TheBestDB",{"id":str(ctx.author.id)})
  await ctx.respond("Profile Deleted!")


#Fun

  #Dad jokes
@bot.slash_command(guild_ids=gids)
async def dadjoke(ctx):
  embed=discord.Embed(title=requests.request("GET", "https://icanhazdadjoke.com/", headers={'Accept':'text/plain'}).text,color=0x509ef2)
  embed.set_footer(text="Powered by icanhazdadjoke.com")
  await ctx.respond(embed=embed)

  #Cat Pictures
@bot.slash_command(guild_ids=gids)
async def cat(ctx):
  cat = requests.request("GET","https://api.thecatapi.com/v1/images/search").text
  a = json.loads(cat)
  #Example response: [{'id': 'b6r', 'url': 'https://cdn2.thecatapi.com/images/b6r.jpg', 'width': 500, 'height': 335}]
  aaa = a[0]
  id = aaa['id']
  url = aaa['url']

  
  

  embed=discord.Embed(title="Look at this cute cat:",color=0x509ef2)
  embed.set_image(url=url)
  embed.set_footer(text=f"Powered by thecatapi.com | ID: {id}")
  await ctx.respond(embed=embed)

bot.run(token)