import discord, os, random, requests, io, time, sqlite3, traceback, datetime, neko
from discord.ext import commands
from discord.utils import get
from PIL import Image, ImageFont, ImageDraw
from vars import words, strPeep
from bs4 import BeautifulSoup 

intents = discord.Intents.all()
bot = commands.Bot(command_prefix = '$', intents = intents)
bot.remove_command('help')

con = sqlite3.connect(os.path.dirname(os.path.realpath(__file__))+'/lod.db')
cur = con.cursor()

# Приветствие Пользователя
@bot.event
async def on_member_join(member: discord.Member):
    channel = bot.get_channel(985680070800728114)
    emb = discord.Embed(title = 'Welcome to The Club!',description = f'{member.mention} Мы Тебе Очень Рады Здесь!', color = 0x641212)
    emb.set_thumbnail(url ='https://cdn.discordapp.com/attachments/985680070800728114/992026355824861244/zerotwohappy.gif')
    await channel.send(embed = emb)
    for guild in bot.guilds:
        for member in guild.members:           
            if cur.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
                cur.execute(f"INSERT INTO users VALUES ('{member.name}', {member.id}, {guild.id}, 0, 0, 0, 0, 1, 0, 0)")
            else:
                pass
            
# Прощание С Пользователем
@bot.event
async def on_member_remove(member: discord.Member):
    channel = bot.get_channel(985680070800728114)
    emb = discord.Embed(title ='Bye Bye!', description = f'{member.mention} Очень Грусно,\nЧто Ты Покинул Нас(((', color = 0x641212)
    emb.set_thumbnail(url ='https://cdn.discordapp.com/attachments/985680070800728114/992027899861413978/animetears.gif')
    await channel.send(embed = emb)
 
 # помощь
@bot.command()
async def help(ctx):
    emb=discord.Embed(title='Вся инфа:', color=0x641212)
    emb.add_field(name=f"``{'$'}join``", value='*Присоединение К Голосовому Каналу*')
    emb.add_field(name=f"``{'$'}leave``", value='*Покинуть Голосовой Канал*')
    emb.add_field(name=f"``{'$'}card``", value='*Карточка Сос Мыслом*')
    emb.add_field(name=f"``{'$'}list``", value='*Команды Хентыча*')
    emb.add_field(name=f"``{'$'}question``", value='*Внимание, Вопрос*')
    emb.add_field(name=f"``{'$'}moneyboard(mb)``", value='*Таблица Лидеров По Валюте*')
    emb.add_field(name=f"``{'$'}repboard(rb)``", value='*Таблица Лидеров По Уважению*')
    emb.add_field(name=f"``{'$'}shameboard(sb)``", value='*Таблица Лидеров По -Уважению*')
    emb.add_field(name=f"``{'$'}cube(ставка)(число)``", value='*Игра С Угадыванием Числа*')
    emb.add_field(name=f"``{'$'}casino(10💎)``", value='*Казино*')
    emb.add_field(name=f"``{'$'}lvl(@...)``", value='*Узнать Уровень И Опыт Участникка*')
    emb.add_field(name=f"``{'$'}money(balance, cash)``", value='*Узнать Свой Баланс*')
    emb.add_field(name=f"``{'$'}info``", value='*Полная Информация О Себе*')
    emb.add_field(name=f"``{'$'}parse``", value='*Парс Хента*')
    emb.add_field(name=f"``{'$'}help_admin``", value='*Помощь Админам*')
    await ctx.send(embed=emb)
    
# помощь админам
@bot.command()
@commands.has_permissions(administrator = True)
async def help_admin(ctx):
    emb = discord.Embed(title = 'Инфа Для Админа:', color = 0x641212)
    emb.add_field(name = f"{'$'}clear (@...)", value = '*Очистка Чата*')
    emb.add_field(name = f"{'$'}kick (@...)", value = '*Легкий Пинок С Сервера*')
    emb.add_field(name = f"{'$'}ban (@...)", value = '*Запретить Доступ Пользователю К Серверу*')
    emb.add_field(name = f"{'$'}unban (@...)", value = '*Вернуть Доступ Пользователю К Серверу*')
    await ctx.send(embed = emb)
  
# Выдать Варн
@bot.command()
@commands.has_permissions(administrator = True)
async def warn(ctx, member: discord.Member = None):
    if member is None:
        await ctx.send(f"{ctx.author.mention}, Укажи ``Участника`` Которому Хочешь Выдать ``Warn``!")
    else:
        if member.id == ctx.author.id:
            await ctx.send(embed = discord.Embed(description = f"**{ctx.author.mention}, Ты Не Можешь Сам Себя Указать!**",color = 0x641212)) 
        else:
            cur.execute(f"UPDATE users SET warn = warn + {1} WHERE id = {member.id}")
            con.commit()
            for row in cur.execute(f"SELECT warn FROM users WHERE id = {member.id}"):
                if row[0] != 3:
                    await ctx.send(embed = discord.Embed(description = f"*{member.mention} У Тебя* ``{row[0]}/3 Warn``!",color = 0x641212))
                else:
                    if row[0] == 3:
                        await ctx.send(embed = discord.Embed(description = f"*{member.mention} У Тебя* ``{row[0]}/3 Warn``!",color = 0x641212))
                        cur.execute(f"DELETE FROM users WHERE id = {member.id}")
                        con.commit()
                        await ctx.send(embed = discord.Embed(description = f'*{member.mention} Успешно Выгнан За Варны\nПользователем: {ctx.author.mention}*!',color = 0x641212))
                        await member.kick(reason = None)                        

# Убрать Варны Пользователя
@bot.command()
@commands.has_permissions(administrator = True)
async def remove_warn(ctx, member: discord.Member = None):
    for row in cur.execute(f"SELECT warn FROM users WHERE id = {member.id}"):
        if member is None:
            await ctx.send(f"*{ctx.author.mention}, Укажи Челика Кому Хочешь Выдать Warn*")
        else:
            if member.id == ctx.author.id:
                await ctx.send(f"**{ctx.author.mention}, Ты Не Можешь Сам Себя Указать!**")
            else:
                if row[0] == 0:
                    await ctx.send(embed = discord.Embed(description = f'*{ctx.author.mention} У Пользователя* ``0 Warn`ов``!',color = 0x641212))
                else:
                    cur.execute(f"UPDATE users SET warn = 0 WHERE id = {member.id}")
                    con.commit()
                    await ctx.send(embed = discord.Embed(description = f"*{member.mention} Были Сняты* ``Все Warn`ы``!",color = 0x641212))
   
# чистка сообщений
@bot.command()
@commands.has_permissions(administrator = True)
async def clear(ctx, amount: int): 
    if ctx.author.id == 682178950331629569:
        await ctx.message.delete()
        deleted = await ctx.channel.purge(limit = amount)
        emb = discord.Embed(description=f' Было Удалено: **{len(deleted)}** Сообщений В Канале ``#{ctx.channel}``', color=0x641212)
        await ctx.channel.send(embed = emb, delete_after=3.5)
    else:
        ctx.send(embed = discord.Embed(description = f'{ctx.author.mention} У Тебя Нет Прав!',color = 0x641212))
        
# кик
@bot.command()
@commands.has_permissions(administrator = True)
async def kick(ctx, member: discord.Member, *, reason = None):
    emb = discord.Embed( title = '*Выгнали За Шиворот:*', color = 0x641212)
    await member.send(f'*{member.mention}, Подумаешь О Своём Поведении!*')
    await member.kick(reason = reason)
    emb.add_field(name = '*Под Зад Дали Пинка*', value = f'*Кикнули: {member.mention}!*')
    emb.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/985680070800728114/986868281262632960/AnimEmoteTreeThrow.gif')
    await ctx.send(embed = emb)
    
# бан
@bot.command()
@commands.has_permissions(administrator = True)
async def ban(ctx, member: discord.Member, *, reason = None):
    emb = discord.Embed( title = '*От Влада Галакаса:*', color = 0x641212)
    await member.ban(reason = reason)
    await member.send(f'*{member.mention}, Надо Было Слушаться!*')
    emb.add_field(name = '*А Вот И Нежданчик)*', value = f'*Забанен : {member.mention}!*')
    emb.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/985680070800728114/985909989396848740/zerotwodead.gif')
    await ctx.send(embed = emb)
    
# разбан
@bot.command()
@commands.has_permissions(administrator = True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    for ban_entry in banned_users:
        user = ban_entry.user 
        await ctx.guild.unban(user)
        await member.send(f'*{member.mention}, Разбанили, Не будь Токсиком:*)')
        emb = discord.Embed(title = '*Разбан:*', colour = 0x621212)
        emb.add_field(name = '*Слава Админам!', value = f'*Все Для Людей) {member.mention}*')
        emb.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/985680070800728114/985891100747247656/TT_elonHighOwO.gif')
        await ctx.send(embed = emb)
                                                                                                                         
# отправить сообщение в ЛС
@bot.command()
async def ls(ctx, member: discord.Member,* ,arg):
    if ctx.author.id == 682178950331629569:
        await ctx.message.delete()
        await member.send(arg)
        
# Войс Присоединиться
@bot.command()
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild = ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        
# Войс Покинуть
@bot.command()
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild = ctx.guild)
    if voice and voice.is_connected():
        await voice.disconnect()
    else:
        voice = await channel.connect()

# Проигрывание Музыки ( ДОДЕЛАТЬ! )________________________________________________________________________________________
#@bot.command()
#async def play(ctx, url: str):

# Карточка Пользователя
@bot.command()
async def card(ctx):
    img = Image.new('RGBA', (400, 200), '#232529')
    url = str(ctx.author.avatar.url)[:-10]
    
    response = requests.get(url, stream = True)
    response = Image.open(io.BytesIO(response.content))
    response = response.convert('RGBA')
    response = response.resize((100, 100), Image.ANTIALIAS)
    
    img.paste(response, (15, 15, 115, 115))
    draw = ImageDraw.Draw(img)
    name = ctx.author.name
    tag = ctx.author.discriminator
    
    headline = ImageFont.truetype('/Users/lodthehou/Desktop/code/code/Bot/arial.ttf', 18)
    undertext = ImageFont.truetype('/Users/lodthehou/Desktop/code/code/Bot/arial.ttf', 12)
    quote = ImageFont.truetype('/Users/lodthehou/Desktop/code/code/Bot/arial.ttf', 12)
    
    Words = random.choice(words)
    peep = random.choice(strPeep)
    Peep = random.choice(strPeep)
    
    draw.text((130, 15), f'{name}#{tag}', font=headline)
    draw.text((130, 50), f'ID: {ctx.author.id}', font=undertext)
    draw.text((130, 75), str(peep), font=undertext)
    draw.text((130, 100), str(Peep), font=undertext)
    draw.text((15, 125), str(Words), font=quote)
    
    img.save('Preview.png')
    
    await ctx.send(file = discord.File(fp = 'preview.png'))
    
# Ошибка Команды
@bot.event
async def on_command_error(ctx, exception): 
    channel = bot.get_channel(1003390015470047353)
    emb = discord.Embed(title=':x: Ошибка Команды',description = f"```py{traceback.format_exception(type(exception), exception, exception.__traceback__)}```",color = 0x641212)
    emb.add_field(name = 'Команда:', value = ctx.command)
    emb.timestamp = datetime.datetime.utcnow()
    await channel.send(embed=emb)
    
# Ошибка События    
@bot.event
async def on_error(ctx, event, *args, **kwargs):
    channel = bot.get_channel(1003390015470047353)
    emb = discord.Embed(title=':x: Ошибка События',description = f"```py{traceback.format_exc()}```",color = 0x641212)
    emb.add_field(name = 'Событие:', value = event)
    emb.timestamp = datetime.datetime.utcnow()
    await channel.send(embed=emb)
    
# Список Команд Хентая
@bot.command()
async def list(ctx):
    await ctx.message.delete()
    emb=discord.Embed(title='Команды Хентыча', description='$end ``команда`` ниже:', color=0x641212)
    emb.add_field(name='wallpaper', value='Обои')
    emb.add_field(name='ngif', value='Гиф')
    emb.add_field(name='feed', value='Еда')
    emb.add_field(name='gecg', value='Пикча С Текстом')
    emb.add_field(name='gasm', value='Ахегао')
    emb.add_field(name='slap', value='Сочные Лещи')
    emb.add_field(name='avatar', value='Аватар')
    emb.add_field(name='waifu', value='Вайфа')
    emb.add_field(name='pat', value='Погладь)')
    emb.add_field(name='kiss', value='Лизуны')
    emb.add_field(name='neko', value='Неко-Тян')
    emb.add_field(name='spank', value='Отшлепать!')
    emb.add_field(name='cuddle', value='ОбнимашкиV2')
    emb.add_field(name='hug', value='Обнимашки')
    emb.add_field(name='smug', value='Че То...')
    await ctx.send(embed=emb)
    
# Команды Хентая
@bot.command()
async def end(ctx, act: str):
    if act:
        if act in ['wallpaper', 'ngif', 'feed', 'gecg', 'gasm', 'slap', 'avatar', 'waifu', 'pat', 'kiss', 'neko', 'spank', 'cuddle', 'hug', 'smug']:
            if ctx.message.guild.id == 985543845741723678:
                channel = bot.get_channel(987427214683422770)
                await channel.send(neko.img(act))
                if ctx.message.channel.id == 987427214683422770:
                    pass
                else:
                    emb = discord.Embed(title = 'Отправлено!',description = '$end '+act, color = 0x641212)
                    emb.add_field(name = 'В Канал:', value = '\n{}'.format(channel.mention))
                    emb.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/953708861238427648/994296293482569838/PepestanGachimuchi.gif')    
                    await ctx.send(embed = emb)
                await ctx.message.delete()
            else:
                pass
    else:
        pass

# Парсинг
@bot.command()    
async def parse(ctx):
    if ctx.message.guild.id == 985543845741723678:
        channel = bot.get_channel(987427214683422770) 
        emb = discord.Embed(title = 'Отправлено!',description = '$parse', color = 0x641212)
        emb.add_field(name = 'В Канал:', value = '{}'.format(channel.mention))
        emb.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/953708861238427648/994296293482569838/PepestanGachimuchi.gif')
        headers = { "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.160 YaBrowser/22.5.2.615 Yowser/2.5 Safari/537.36"}
        responce = requests.get("https://nekos.life/#", headers=headers)
        soup = BeautifulSoup(responce.content,"html.parser")
        divs = soup.find_all("div", class_="w3-container w3-card-4 w3-center w3-purple")
        for div in divs:
            url_img = div.find("img", class_="w3-image w3-card-4").get("src")
        await channel.send(url_img)
        if ctx.message.channel.id == 987427214683422770:
            pass
        else:
            emb = discord.Embed(title = 'Отправлено!',description = 'parse', color = 0x641212)
            emb.add_field(name = 'В Канал:', value = f'{channel.mention}')
            emb.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/953708861238427648/994296293482569838/PepestanGachimuchi.gif')
            await ctx.send(embed = emb)
        await ctx.message.delete()
    else:
        pass

# Парс Хентая
@bot.command()
async def hentai(ctx):
    if ctx.message.guild.id == 985543845741723678:
        channel = bot.get_channel(987427214683422770) 
        emb = discord.Embed(title = 'Отправлено!',description = '$parse', color = 0x641212)
        emb.add_field(name = 'В Канал:', value = '{}'.format(channel.mention))
        emb.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/953708861238427648/994296293482569838/PepestanGachimuchi.gif')
        for x in range(0, 7158):
            url = f"https://anime-pictures.net/pictures/view_posts/{x}?lang=rut"
            headers = { "Accept": "*/*","User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.134 YaBrowser/22.7.1.806 Yowser/2.5 Safari/537.36"}
            req = requests.get(url, headers = headers)
            soup = BeautifulSoup(req.text, "lxml")
            img = soup.find_all("img", class_ = "img_cp")
            for item in img:
                url = item.get("src")
                await channel.send("https:" + url)
                time.sleep(2)
        if ctx.message.channel.id == 987427214683422770:
            pass
        else:
            emb = discord.Embed(title = 'Отправлено!',description = 'parse', color = 0x641212)
            emb.add_field(name = 'В Канал:', value = f'{channel.mention}')
            emb.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/953708861238427648/994296293482569838/PepestanGachimuchi.gif')
            await ctx.send(embed = emb)
        await ctx.message.delete()
    else:
        pass

# Баланс
@bot.command(aliases = ['balance', 'cash'])
async def money(ctx, member: discord.Member = None):
    if member is None:
        for row in cur.execute(f"SELECT cash FROM users WHERE id = {ctx.author.id}"):
            await ctx.send(embed = discord.Embed(description = f'В Копилке У {ctx.author.mention} Лежит: ``{row[0]} Алмазов 💎``',color = 0x641212))
    else:
        for row in cur.execute(f"SELECT cash FROM users WHERE id = {member.id}"):
            await ctx.send(embed = discord.Embed(description = f'В Копилке У {member.mention} Лежит: ``{row[0]} Алмазов 💎``',color = 0x641212))

# Выдать Валюту 
@bot.command()
@commands.has_permissions(administrator = True)
async def award(ctx, member: discord.Member = None, cash: int = None):
    if ctx.author.id == 682178950331629569:
        if member is None:
            await ctx.send(embed = discord.Embed(description = f"{ctx.author.mention}, А Кому?",color = 0x641212))
        else:
            if cash is None:
                await ctx.send(embed = discord.Embed(description = f"{ctx.author.mention}, А Сколько Скинуть Выдать ``💎``?",color = 0x641212))
            elif cash < 10:
                await ctx.send(embed = discord.Embed(description = f"{ctx.author.mention}, Можно Только Больше ``10 💎``",color = 0x641212))
            else:
                cur.execute(f"UPDATE users SET cash = cash + {cash} WHERE id = {member.id}")
                con.commit()

                for row in cur.execute(f"SELECT cash FROM users WHERE id = {member.id}"):
                    await ctx.send(embed = discord.Embed(description = f"``{member.mention} Баланс Обновлен:`` ``{row[0]} 💎``",color = 0x641212))
    else:
        await ctx.send(embed = discord.Embed(description = "Вы Не Разработчик!",color = 0x641212))

# Скинуть Свою Валюту
@bot.command()
async def take(ctx, member: discord.Member = None, cash = None):
    if member is None:
        await ctx.send(embed = discord.Embed(description = f"{ctx.author.mention}, А Кому?",color = 0x641212))
    else:
        if cash is None:
            await ctx.send(embed = discord.Embed(description = f"{ctx.author.mention}, А Сколько Скинуть ``💎``?",color = 0x641212))
        elif str(cash) == 'all':
            await ctx.send(embed = discord.Embed(description = f"Теперь Ты {member.mention} Ноль По Жизни!",color = 0x641212))
            cur.execute(f"UPDATE users SET cash = {0} WHERE id = {member.id}")
            con.commit()
        elif int(cash) < 0:
            await ctx.send(embed = discord.Embed(description = f"{ctx.author.mention}, Укажи Больше ``1 💎``",color = 0x641212))
        else:
            cur.execute(f"UPDATE users SET cash = cash - {cash} WHERE id = {member.id}")
            con.commit()
            await ctx.send(embed = discord.Embed(description = f"{member.mention}, У Тебя Отняли: ``{cash} 💎``",color = 0x641212))

# Повысить Репутацию
@bot.command()
async def rep(ctx, member: discord.Member = None):
    if member is None:
        await ctx.send(embed = discord.Embed(description = f"{ctx.author.mention}, Кому Хочешь Повысить Фактор Rep",color = 0x641212))
    else:
        if member.id == ctx.author.id:
            await ctx.send(embed = discord.Embed(description = f"{ctx.author.mention}, Ты Не Можешь Сам Себя Указать!",color = 0x641212))
        else:
            cur.execute(f"UPDATE users SET rep = rep + {1} WHERE id = {member.id}")
            con.commit()
            await ctx.message.add_reaction('🎩')

# Понизить Репутацию
@bot.command()
async def shame(ctx, member: discord.Member = None):
    if member is None:
        await ctx.send(f"{ctx.author.mention}, Укажи Челика Которому Хочешь Понизить Фактор Rep")
    else:
        if member.id == ctx.author.id:
            await ctx.send(f"{ctx.author.mention}, Ты Не Можешь Сам Себя Указать!")
        else:
            cur.execute(f"UPDATE users SET rep = rep - {1} WHERE id = {member.id}")
            con.commit()
            await ctx.message.add_reaction('🤡')

# Таблица Лидеров По Валюте
@bot.command(aliases = ['moneyboard', 'mb'])
async def __moneyboard(ctx):
    emb = discord.Embed(title = 'Топчик:', color = 0x641212)
    emb.add_field(name ='По Количеству', value = 'Алмазов')
    counter = 0
    for row in cur.execute("SELECT name, cash FROM users WHERE server_id = {} ORDER BY cash DESC LIMIT 5".format(ctx.guild.id)):
        counter += 1
        emb.add_field(name = f'# {counter} | `{row[0]}`',value = f'Сундук: {row[1]} 💎',inline = False)
        emb.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/953708861238427648/995577677908017162/995386503993766050.webp')
    await ctx.send(embed = emb)

# Таблица Лидеров По Репутации
@bot.command(aliases =['repboard', 'rb'])
async def __repboard(ctx):
    emb = discord.Embed(title = 'Топчик:', color = 0x483D8B)
    emb.add_field(name ='По количеству', value = 'Репутации')
    counter = 0
    for row in cur.execute("SELECT name, rep FROM users WHERE server_id = {} ORDER BY rep DESC LIMIT 5".format(ctx.guild.id)):
        counter += 1
        emb.add_field(name = f'# {counter} | `{row[0]}`',value = f'Репутация: {row[1]} 🎩',inline = False)
        emb.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/985680070800728114/992104978472771674/PU_PepeCigarSmoke.gif')
    await ctx.send(embed = emb)

# Доска Позора
@bot.command(aliases = ['shameboard', 'sb'])
async def __shameboard(ctx):
    emb = discord.Embed(title = 'Топ Буйных:', color = 0x641212)
    emb.add_field(name ='По количеству', value = '-Репутация')
    counter = 0
    for row in cur.execute("SELECT name, rep FROM users WHERE server_id = {} ORDER BY rep LIMIT 5".format(ctx.guild.id)):
        counter += 1
        emb.add_field(name = f'# {counter} | `{row[0]}`',value = f'Репутация: {row[1]} 🤡',inline = False)
        emb.set_thumbnail(url = '')
    await ctx.send(embed = emb)

# Добавить Предмет/Ссылку/Картинку В Магазин
@bot.command()
async def add_shop(ctx, url: str = None, item_name: str = None, price: int = None):
    if url is None:
        await ctx.send(embed = discord.Embed(description = f"{ctx.author.mention}, Укажи ``Предмет/Ссылку/Картинку``!",color = 0x641212))
    elif item_name is None:
        await ctx.send(embed = discord.Embed(description = f"{ctx.author.mention}, Укажи ``Имя`` Предмета!",color = 0x641212))
    else:
        if price is None:
            await ctx.send(embed = discord.Embed(description = f"{ctx.author.mention}, Укажи ``Стоимость 💎``!",color = 0x641212))
        elif price < 1:
            await ctx.send(embed = discord.Embed(description = f"{ctx.author.mention}, Слишком ``Мало 💎``!",color = 0x641212))
        else:
            cur.execute(f"INSERT INTO shop VALUES ('{url}', '{item_name}', {price}, '{ctx.author.name}', {ctx.author.id}, {ctx.guild.id})")
            con.commit()
            await ctx.message.delete()
            await ctx.send(embed = discord.Embed(description = f"Предмет ``{item_name}`` Был Выставлен На Продажу, {ctx.author.mention}!",color = 0x641212))

# Удалить Товар С Магазина
@bot.command()
async def dlt_shop(ctx, item_name: str = None):
    if item_name is None:
        await ctx.send(embed = discord.Embed(description = f'{ctx.author.mention}, Укажи ``Имя`` Предмета Который Хочешь Удалить!',color = 0x641212))
    else:
        for row in cur.execute(f"SELECT user_id FROM shop WHERE user_id = {ctx.author.id}"):
            if ctx.author.id != row[0]:           
                await ctx.send(embed = discord.Embed(description = f"**{ctx.author.mention}, У Тебя Нет Прав!**",color = 0x641212))
            else:
                cur.execute(f"DELETE FROM shop WHERE item_name = '{item_name}'")
                con.commit()
                await ctx.send(embed = discord.Embed(description = f"Предмет ``{item_name}`` Был Удален {ctx.author.mention}!",color = 0x641212))

# Магазин
@bot.command()
async def shop(ctx):
    emb = discord.Embed(title ='``Магазин:``', color = 0x641212)
    for row in cur.execute(f"SELECT item_name, price FROM shop WHERE server_id = {ctx.guild.id}"):
        emb.add_field(name = f'**{row[0]}**',value = f'``{row[1]} 💎``',inline = False)
        if row is None:
            await ctx.send('*Магазин пуст*')
    await ctx.send(embed = emb)

# Купить Предмет В Магазине
@bot.command()
async def buy(ctx, item_name: str = None):
    for row in cur.execute(f"SELECT url, price, cash FROM shop, users WHERE item_name = '{item_name}' AND id = {ctx.author.id}"):    
        if item_name is None:
            await ctx.send(f'{ctx.author.mention}, Укажи ``Имя`` Предмета Который Хочешь Купить!')
        elif row[2] < row[1]:
            await ctx.send(embed = discord.Embed(description = f'{ctx.author.mention} У Тебя Нет ``{row[1]} 💎``!',color = 0x641212))
        else:
            item = cur.execute(f"SELECT item_name FROM shop WHERE item_name = '{item_name}'")
            url = cur.execute(f"SELECT url FROM shop WHERE item_name = '{item_name}'")
            cur.execute(f"UPDATE users SET cash = cash - {row[1]} WHERE id = {ctx.author.id}")
            await ctx.send(embed = discord.Embed(description = f"Предмет ``{item_name}`` Был Куплен За ``{row[1]} Алмазов 💎``, {ctx.author.mention}!",color = 0x641212))
            time.sleep(1)
            await ctx.author.send(f'Вы Купили: {row[0]}')
            cur.execute(f"DELETE FROM shop WHERE item_name = '{item_name}'")
            con.commit()

# Информация
@bot.command()
async def info(ctx, member: discord.Member = None):
    if member is None:
        information = cur.execute(f"SELECT cash, rep, warn, lvl, exp, msg FROM users WHERE id = {ctx.author.id}")
        for row in information:
            emb = discord.Embed(title = f'*Информация О:* ``{ctx.author.name}``',color = 0x641212)
            emb.add_field(name = '``Карман:``',value = f'``{row[0]} 💎``'),
            emb.add_field(name = '``Rep:``',value = f'``{row[1]} 🎩``'),
            emb.add_field(name = '``Warns:``',value = f'``{row[2]}/3 📣``'),
            emb.add_field(name = '``level:``',value = f'``{row[3]} 🔋``'),
            emb.add_field(name = '``exp:``',value = f'``{row[4]} 🍀``'),
            emb.add_field(name = '``Сообщений:``',value = f'``{row[5]} 📄``')            
            await ctx.send(embed = emb)
    else:
        information = cur.execute(f"SELECT cash, rep, warn, lvl, exp, msg FROM users WHERE id = {member.id}")
        for row in information:
            emb = discord.Embed(title = f'*Информация О:* ``{member.name}``',color = 0x641212)
            emb.add_field(name = '``Карман:``',value = f'``{row[0]} 💎``'),
            emb.add_field(name = '``Rep:``',value = f'``{row[1]} 🎩``'),
            emb.add_field(name = '``Warns:``',value = f'``{row[2]}/3 📣``'),
            emb.add_field(name = '``level``:',value = f'``{row[3]} 🔋``'),
            emb.add_field(name = '``exp:``',value = f'``{row[4]} 🍀``'),
            emb.add_field(name = '``Сообщений:``',value = f'``{row[5]} 📄``')            
            await ctx.send(embed = emb)

#Система Опыта
@bot.event
async def on_message(message):
    content = len(message.content)
    if message.author.bot:
        pass
    elif content > 2:
        for y in cur.execute(f"SELECT lvl, exp FROM users WHERE id = {message.author.id}"):
            x = content*10/2
            cur.execute(f"UPDATE users SET exp = exp + {x} WHERE id = {message.author.id}")
            con.commit()
            exp = int(y[1])
            lvl_start = y[0]
            lvl_end = int(lvl_start * (1000))
            if exp > lvl_end:
                money = 1000                
                cur.execute(f"UPDATE users SET lvl = lvl + {1},exp = 0, cash = cash + {money} WHERE id = {message.author.id}")
                con.commit()
                for next_lvl in cur.execute(f"SELECT lvl FROM users WHERE id = {message.author.id}"):
                    await message.channel.send(embed = discord.Embed(description = f'*{message.author.mention} Повышен До* ``{next_lvl[0]} Уровня``!',color = 0x641212))
            else:
                if cur.execute(f"UPDATE users SET msg = msg + {1} WHERE id = {message.author.id}"):
                    con.commit()              
    else:
        pass
    await bot.process_commands(message)

# Уровень Участника
@bot.command()
async def lvl(ctx, member: discord.Member = None):
    if member is None:
        level = cur.execute(f"SELECT lvl, exp FROM users WHERE id = {ctx.author.id}")
        for row in level:
            exp = row[1]
            lvl_start = row[0]
            lvl_end = int(lvl_start * (100))
            results = int(lvl_end - exp)
            await ctx.send(embed = discord.Embed(description = f'*{ctx.author.mention} У Тебя* ``{row[0]} 🔋`` И ``{row[1]} 🍀``!\n*До Следуещего Уровня:* ``{results} 🍀``',color = 0x641212))
    else:    
        lvl = cur.execute(f"SELECT lvl, exp FROM users WHERE id = {member.id}")
        for row in lvl:
            exp = row[1]
            lvl_start = row[0]
            lvl_end = int(lvl_start * (100))
            results = int(lvl_end - exp)
            await ctx.send(embed = discord.Embed(description = f'У ``{member.name}`` ``{row[0]} 🔋`` И ``{row[1]} 🍀``!\n*До Следуещего Уровня:* ``{results} 🍀``',color = 0x641212))

# Игра Куб
@bot.command()
async def cube(ctx, bet: int = None, answer: int = None):
    for row in cur.execute(f"SELECT cash FROM users WHERE id = {ctx.author.id}"):
        if bet is None:
            await ctx.send(embed = discord.Embed(description = f'**{ctx.author.mention} Укажи Ставку!**',color = 0x641212))
        elif answer is None:
            await ctx.send(embed = discord.Embed(description = f'**{ctx.author.mention} Укажи Число!**',color = 0x641212))
        elif bet > row[0]:
            await ctx.send(embed = discord.Embed(description = f'**{ctx.author.mention} У Тебя Нет** ``{bet} 💎``!',color = 0x641212))
        elif answer > 10:
            await ctx.send(embed = discord.Embed(description = f"*Нельзя Указать Больше* ``10``!",color = 0x641212))
        else:
            await ctx.send(embed = discord.Embed(description = f'*{ctx.author.mention} Бросаю Кубик...*\n*Ваша Ставка:* ``{bet} 💎``\n*Ваше Число:* ``{answer} 🎲``',color = 0x641212))
            time.sleep(1)
            number = random.randint(1, 10)
            x = random.randint(5, 25)
            if answer == number:
                winning = int(bet*x)
                await ctx.send(embed = discord.Embed(description = f'*Верно!*\n*{ctx.author.mention} Вы Выиграли:* ``{winning} 💎``',color = 0x641212))
                cur.execute(f"UPDATE users SET cash = cash + {winning} WHERE id = {ctx.author.id}")
                con.commit()
            else:
                if answer != number:
                    lose = int(bet)
                    await ctx.send(embed = discord.Embed(description = f'{ctx.author.mention} *Неверно!*\n*Правильный Ответ Был:* ``{number} 🎲``',color = 0x641212))
                    cur.execute(f"UPDATE users SET cash = cash - {lose} WHERE id = {ctx.author.id}")
                    con.commit()

# Казино
@bot.command()
async def casino(ctx):
    for row in cur.execute(f"SELECT cash FROM users WHERE id = {ctx.author.id}"):
        if row[0] < 10:
            await ctx.send(embed = discord.Embed(description = f'**{ctx.author.mention} У Тебя Нет** ``10 💎``!',color = 0x641212))
        else:
            signs = ['🔔', '🍋', '💲', '🍀', '🍒', '🍇']
            z = random.choice(signs)
            x = random.choice(signs)
            c = random.choice(signs)
            await ctx.send(embed = discord.Embed(description = f"*Кручу Джекпот...*",color = 0x641212))
            time.sleep(2)
            await ctx.send(embed = discord.Embed(description = f"*Выпадают Знаки:*\n----------------------\n|``{z}``|- -|``{x}``|- -|``{c}``|\n----------------------",color = 0x641212))
            if z == x == c:
                winning = int(10*1000)
                cur.execute(f"UPDATE users SET cash = cash + {winning} WHERE id = {ctx.author.id}")
                await ctx.send(embed = discord.Embed(description = f"**Джекпот!**\n``Вы Выиграли! ✔️``\n*Ваш Выигрышь:*\n``{winning} 💎``",color = 0x641212))
            elif z == x != c:
                cur.execute(f"UPDATE users SET cash = cash - {10} WHERE id = {ctx.author.id}")
                await ctx.send(embed = discord.Embed(description = f"``Вы Проиграли! ❌``\n*Удача Улыбнется В Следующий Раз!*",color = 0x641212))
            elif z != x == c:
                cur.execute(f"UPDATE users SET cash = cash - {10} WHERE id = {ctx.author.id}")
                await ctx.send(embed = discord.Embed(description = f"``Вы Проиграли! ❌``\n*Удача Улыбнется В Следующий Раз!*",color = 0x641212))
            elif z != x != c:
                cur.execute(f"UPDATE users SET cash = cash - {10} WHERE id = {ctx.author.id}")
                await ctx.send(embed = discord.Embed(description = f"``Вы Проиграли! ❌``\n*Удача Улыбнется В Следующий Раз!*",color = 0x641212))
            else:
                pass

#
@bot.command()
async def test(ctx):
    await ctx.send('test command')


#
@bot.command()
async def cmd(ctx):
    await ctx.send('создать новую комманду?')


# любой текст
@bot.command()
async def ex(ctx, *, arg):
    await ctx.message.delete()
    emb = discord.Embed(description = arg,color = 0x641212)
    await ctx.message.delete()
    await ctx.send(embed = emb)
    
# загрузка когов
@bot.command()
async def load(ctx, extension):
    if ctx.author.id == 682178950331629569:
        bot.load_extension(f"cogs.{extension}")
        await ctx.send(embed = discord.Embed(description = "Коги Были Успешно Загружены!",color = 0x641212))
    else:
        await ctx.send(embed = discord.Embed(description = "Вы Не Разработчик!",color = 0x641212))

# выгрузка когов
@bot.command()
async def unload(ctx, extension):
    if ctx.author.id == 682178950331629569:
        bot.unload_extension(f"cogs.{extension}")
        await ctx.send(embed = discord.Embed(description = "Коги Были Успешно Выгружены!",color = 0x641212))
    else:
        await ctx.send(embed = discord.Embed(description = "Вы Не Разработчик!",color = 0x641212))

# перезагрузка когов
@bot.command()
async def reload(ctx, extension):
    if ctx.author.id == 682178950331629569:
        bot.unload_extension(f"cogs.{extension}")
        time.sleep(1)
        bot.load_extension(f"cogs.{extension}")
        await ctx.send(embed = discord.Embed(description = "Коги Были Успешно Перезагружены!",color = 0x641212))
    else:
        await ctx.send(embed = discord.Embed(description = "Вы Не Разработчик!",color = 0x641212))

# Запуск
@bot.event
async def on_ready():
    await bot.change_presence(status = discord.Status.dnd,activity = discord.Game('Visual Studio Code'))
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
        name TEXT,
        id INT,
        server_id INT,
        cash BIGINT,
        rep INT,
        warn INT,
        exp INT,
        lvl INT,
        msg INT,
    )""")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS shop (
        url TEXT,
        item_name TEXT,
        price BIGINT,
        nickname TEXT,
        user_id INT,
        server_id INT
    )""")
    con.commit()
    for guild in bot.guilds:
        for member in guild.members:           
            if cur.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
                cur.execute(f"INSERT INTO users VALUES ('{member.name}', {member.id}, {guild.id}, 0, 0, 0, 0, 1, 0, 0)")
            else:
                pass
    con.commit()
    print('Bot started')

token = os.path.expanduser('/Users/lodthehou/Desktop/code/code/Bot/tkn.txt')
f = open(token)
bot.run(f.read())