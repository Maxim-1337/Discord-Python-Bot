import discord
import datetime
import config
from discord.commands import Option
from discord.ext.commands import has_permissions, MissingPermissions

intents = discord.Intents.default()
intents.members = True
intents = intents.all()

activity = discord.Activity(type=config.activity, name=config.status)

bot = discord.Bot(
    intents=intents, 
    debug_guilds=[config.guilds],
    activity=activity,
    status=discord.Status.idle
)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    CYELLOW = '\33[33m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

########################################################################## - On Event
@bot.event
async def on_ready():
    print()
    print('------------------------------------------------------------------------------------')
    print('Maxim1337 Der Profi Dev!')
    print(f'Der Bot [{bot.user}] wurde {bcolors.OKGREEN}erfoglreich{bcolors.ENDC} hochgefahren!')
    print('------------------------------------------------------------------------------------')
########################################################################## - User Info Command
@bot.slash_command(description='User Infos', name='userinfo')
async def userinfo(ctx, *, user: discord.Member = None):
    if user is None:
        user = ctx.author      
    date_format = "%a, %d %b %Y %H:%M:%S"
    embed = discord.Embed(color=0xdfa3ff, description=user.mention)
    embed.set_author(name=str(user), icon_url=user.display_avatar.url)
    embed.set_thumbnail(url=user.display_avatar.url)
    embed.add_field(name="Joined", value=user.joined_at.strftime(date_format))
    members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
    embed.add_field(name="Join position", value=str(members.index(user)+1))
    embed.add_field(name="Registered", value=user.created_at.strftime(date_format))
    embed.set_footer(text='ID: ' + str(user.id))
    return await ctx.send(embed=embed,ephemeral=True)
########################################################################## - Embed Creator
@bot.slash_command(description='Embed Creator', name=config.createembed)
@has_permissions(manage_messages=True)
async def buttonembed(ctx, title: str, description : str, author : str):

  embed = discord.Embed(title=title, description=description, color=0xb700ff)
  embed.set_thumbnail(url=config.embedthumbnail)
  embed.set_author(name=author, icon_url=config.embedauthorimg)
  embed.set_footer(text=author, icon_url=config.embedfooterimg)
  
  await ctx.send(embed=embed)
  await ctx.respond('Dein embed wurde gesendet!',ephemeral=True)
########################################################################## - Embed Creator with Button
@bot.slash_command(description='Embed Creator with Button', name=config.buttonembed)
@has_permissions(manage_messages=True)
async def buttonembed(ctx, title: str, description : str, author : str, buttonlabel : str, buttonurl : Option(str, 'Es muss eine URL sein')):

  embed = discord.Embed(title=title, description=description, color=0xb700ff)
  embed.set_thumbnail(url=config.embedthumbnail)
  embed.set_author(name=author, icon_url=config.embedauthorimg)
  embed.set_footer(text=author, icon_url=config.embedfooterimg)
  
  button = discord.ui.Button(label=buttonlabel, url=buttonurl)
  view = discord.ui.View()
  view.add_item(button)
  
  await ctx.send(embed=embed,view=view)
  await ctx.respond('Dein embed wurde gesendet!',ephemeral=True)
########################################################################## - Clear Command
@bot.slash_command(description='Nachrichten Löschen', name=config.clear)
@has_permissions(manage_messages=True)
async def clear(
    ctx,
    count: Option(int, 'Anzahl der Nachrichten die gelöscht werden sollen', min_value=1, max_value=133769)
):
        embed = discord.Embed(
            title=f'<:yes:1003748583788523560> Es wurden Erfolgreich ```{count}``` Nachrichten gelöscht.',
            color=0xb700ff
        )
        messages = await ctx.channel.purge(limit=count)
        await ctx.respond(embed=embed,delete_after=10,ephemeral=True)
        
@clear.error
async def clear(ctx, error):
    if isinstance(error, MissingPermissions):
            embed = discord.Embed(
            title=f'<:no:1003748584992288889> Du hast keine Rechte!',
            color=0xb700ff,
        )
    await ctx.respond(embed=embed,delete_after=10,ephemeral=True)
########################################################################## - Bann Command
@bot.slash_command(description='User Bannen', name=config.ban)
@has_permissions(administrator = True)
async def ban(
            ctx,
            member : discord.Member, 
            reason = None
):

    embed = discord.Embed(
    title=f'<:yes:1003748584992288889> Du hast den User ```{member}``` Gebannt! Grund ```{reason}```',
    color=0xb700ff,

)
    await member.ban(reason = reason)
    await ctx.respond(embed=embed,delete_after=10)

@ban.error
async def ban(ctx, error):
    if isinstance(error, MissingPermissions):
            embed = discord.Embed(
            title=f'<:no:1003748584992288889> Du hast keine Rechte!',
            color=0xb700ff,
        )
    await ctx.respond(embed=embed,delete_after=10,ephemeral=True)
########################################################################## - Kick Command
@bot.slash_command(description='User Kicken', name=config.kick)
@has_permissions(administrator = True)
async def kick(ctx, member : discord.Member, reason = None):
    
    embed = discord.Embed(
    title=f'<:yes:1003748584992288889> Du hast den User ```{member}``` Gekickt! Grund ```{reason}```',
    color=0xb700ff,

)
    await member.kick(reason = reason)
    await ctx.respond(embed=embed,delete_after=10)

@kick.error
async def kick(ctx, error):
    if isinstance(error, MissingPermissions):
            embed = discord.Embed(
            title=f'<:no:1003748584992288889> Du hast keine Rechte!',
            color=0xb700ff,
        )
    await ctx.respond(embed=embed,delete_after=10,ephemeral=True)
########################################################################## - Help Command
@bot.slash_command(description='Liste aller Commands', name=config.helpcmd)
async def help(
            ctx
):

    embed = discord.Embed(
    title=f'Eine Liste aller Commands',
    description='**/userinfo** - Zeigt alle infos über den ausgewehlten user\n**/carlist** - Zeigt die Spawnliste aller Autos auf Spongebob Crimelife\n**/andrewtate** - Adrew Tate',
    color=0xb700ff,

)
    embed.set_thumbnail(url=config.embedthumbnail)
    embed.set_author(name=config.author, icon_url=config.embedauthorimg)
    embed.set_footer(text=config.footer, icon_url=config.embedfooterimg)

    await ctx.respond(embed=embed,delete_after=120,ephemeral=True)
########################################################################## - Car list Command
@bot.slash_command(description='Car List', name=config.carlist)
async def carlist(ctx,):   

        embed = discord.Embed(
        title='Spongebob Car List',
        color=0xb700ff,
        description= 'bmw8mm - **BMW**\nclssb - **Mercedes**\ndawnonyx - **Rolls Royce**\ns500 - **Mercedes**\nrocket - **Mercedes**\nevs850 - **Mercedes**\nKillerRs7 - **Audi**\nrrf8wide **Ferrari**\nUrus - **Lamborghini**\nserv_electricscooter - **Scooter**\ns63mansorycabrio - **Mercede**\nRocket900_Royal_FINAL7 -** Mercedes**\nhyclambo - **Lamborghini**\ngemera - **Könnigsegg**',
    )
        embed.set_thumbnail(url=config.embedthumbnail)
        embed.set_image(url=config.image)
        embed.set_author(name=config.author, icon_url=config.embedauthorimg)
        embed.set_footer(text=config.footer, icon_url=config.embedfooterimg)
        button = discord.ui.Button(label="FiveM", url="https://stake.com/casino/home")
        view = discord.ui.View()
        view.add_item(button)

        await ctx.respond(embed=embed,view=view,ephemeral=True)
########################################################################## - FiveM Command
@bot.slash_command(description='FiveM', name=config.fivem)
async def fivem(ctx,):   

        embed = discord.Embed(
        title='Spongebob Crimelife',
        color=0xb700ff,
        description='Hier sind Alle informationen über Spongebob Crimlife \n\n**<:fivem:1025059414497034312> FiveM ➙ ** \n\n**<:voice:1025059998717444277> Voice ➙  ** Ingame Voice\n'
 
        )
        embed.set_thumbnail(url=config.embedthumbnail)
        embed.set_author(name=config.author, icon_url=config.embedauthorimg)
        ##embed3.set_footer(text="Spongebob Crimelife", icon_url=config.embedfooterimg)
        button = discord.ui.Button(label="FiveM", url="https://stake.com/casino/home")
        view = discord.ui.View()
        view.add_item(button)

        await ctx.respond(embed=embed,view=view,ephemeral=True)
########################################################################## - Adrew Tate Command
@bot.slash_command(description='Adrew Abi', name=config.andrewtate)
async def andrewtate(ctx,):   

        embed = discord.Embed(
        title='Andrew Tate',
        color=0xb700ff,

        )
        embed.set_thumbnail(url="https://technisch24.com/wp-content/uploads/2022/08/wer-ist-andrew-tate-wie-alt-ist-andrew-tate-XLh4WRvN.jpg")
        embed.set_author(name="Andrew Tate", icon_url="https://technisch24.com/wp-content/uploads/2022/08/wer-ist-andrew-tate-wie-alt-ist-andrew-tate-XLh4WRvN.jpg")
        embed.set_footer(text="Andrew Tate", icon_url="https://technisch24.com/wp-content/uploads/2022/08/wer-ist-andrew-tate-wie-alt-ist-andrew-tate-XLh4WRvN.jpg")
        embed.set_image(url="https://technisch24.com/wp-content/uploads/2022/08/wer-ist-andrew-tate-wie-alt-ist-andrew-tate-XLh4WRvN.jpg")
        await ctx.respond(embed=embed,ephemeral=True)
########################################################################## - Suggestion Command
@bot.slash_command(description='Suggestion', name=config.suggestion)
async def suggestion(ctx, *, description: str):
    ##member = ctx.author
    embed = discord.Embed(title=f'Suggestion', description=description, color=0xb700ff)
    embed.set_thumbnail(url=config.embedthumbnail)
    embed.set_author(name=config.author, icon_url=config.embedauthorimg)
    embed.set_footer(text=config.footer, icon_url=config.embedfooterimg)
    vote = await ctx.send(embed=embed)
    await vote.add_reaction("✅")
    await vote.add_reaction("❌")
########################################################################## - Verify
@bot.slash_command(name=config.verifycmd)
async def verifyembed(ctx):

    embed = discord.Embed(
    timestamp=datetime.datetime.utcnow(),
    ##title='Spongebob Crimelife',
    color=0xb700ff,
    description=f'Bitte Verify dich untem am Button!'
 
)
    embed.set_thumbnail(url=config.embedthumbnail)
    embed.set_author(name=config.author, icon_url=config.embedauthorimg)
    embed.set_footer(text=config.footer, icon_url=config.embedfooterimg)
    button = discord.ui.Button(label="Regelwerk", url="https://stake.com/casino/home")
    view2 = discord.ui.View()
    view2.add_item(button)

    await ctx.respond(embed=embed,view=Verify())

class Verify(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Verify", style=discord.ButtonStyle.success, emoji="<:yes:1003748583788523560>", custom_id="verify", row=3)
    async def verify(self, interaction: discord.Interaction, button: discord.ui.Button):
        if type(config.verifybotrole) is not discord.Role: bot.role = interaction.guild.get_role(config.verifyrole)
        if bot.role not in interaction.user.roles:
            await interaction.user.add_roles(bot.role)
            await interaction.response.send_message(f"I have given you {bot.role.mention}!", ephemeral = True)
        else: await interaction.response.send_message(f"You already have {bot.role.mention}!", ephemeral = True)

########################################################################## - Welcome Embed
@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.channels, name=config.joinchannel)
    await member.add_roles(member.guild.get_role(config.joinrole))
    ##await channel.send(f"{member.mention} has just joined the server!")
    
    embed = discord.Embed(
    timestamp=datetime.datetime.utcnow(),
    ##title='Spongebob Crimelife',
    color=0xb700ff,
    description=f'Willkommen auf Spongebob Crimelife **{member.mention}**'
 
)
    time = datetime.datetime.utcnow()
    embed.set_thumbnail(url=str(member.display_avatar.url))
    embed.set_author(name=config.author, icon_url=config.embedauthorimg)
    embed.set_footer(text=config.footer, icon_url=config.embedfooterimg)
    button = discord.ui.Button(label="FiveM", url=config.buttonurl)
    view = discord.ui.View()
    view.add_item(button)

    await channel.send(embed=embed,view=view)
########################################################################## - Leave Embed
@bot.event
async def on_member_remove(member):
    channel = discord.utils.get(member.guild.channels, name=config.leavechannel)
        
    embed = discord.Embed(
    timestamp=datetime.datetime.utcnow(),
    ##title='Spongebob Crimelife',
    color=0xb700ff,
    description=f'Schade das du Spongebob Crimelife verlässt!**{member.mention}**'
 
)
    
    embed.set_thumbnail(url=str(member.display_avatar.url))
    embed.set_author(name=config.author, icon_url=config.embedauthorimg)
    embed.set_footer(text="Spongebob Crimelife\u200b", icon_url=config.embedfooterimg)
    await channel.send(embed=embed)
########################################################################## - Run
bot.run(config.token)
########################################################################## - End