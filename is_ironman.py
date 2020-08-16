from asyncio import sleep
from configparser import ConfigParser
import requests
from bs4 import BeautifulSoup
from discord.ext import commands, tasks

def config(section, filename='conf.ini'):
    parser = ConfigParser()
    parser.read(filename)
    conf = {}
    if parser.has_section(section):
        parameters = parser.items(section)
        for param in parameters:
            conf[param[0]] = param[1]
    else:
        raise Exception("config not found!")
    return conf

bot = commands.Bot("!")
conf = config('group_ironman')


def get_daily_msg():
    daily_update = "ironman status: \n"
    if is_group_ironman():
        daily_update += "is out!!"
    else:
        daily_update += "is not out yet. Checking again in 12 hours!"
    return daily_update
        

def is_group_ironman():
    res = requests.get("https://secure.runescape.com/m=hiscore_oldschool/overall")
    soup = BeautifulSoup(res.text, 'html.parser')
    search_res = soup.find_all('div', class_='ironman-nav')
    if "group" in search_res[0].get_text().lower():
        return True

class DailyChecker(commands.Cog):
    def __init__(self, bot, channel):
        self.bot = bot
        self.check_daily_ironman.start()
        self.channel = channel

    @tasks.loop(hours=12)
    async def check_daily_ironman(self):
        channel = self.bot.get_channel(int(self.channel))
        msg = get_daily_msg()
        await channel.send(msg)



@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    bot.add_cog(DailyChecker(bot, conf['channel']))


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if "ironman" in message.content.lower():
        if is_group_ironman():
            await message.channel.send('group ironman is out!')
        else:
            await message.channel.send('group ironman is not out yet :(')
    await bot.process_commands(message)


if __name__ == "__main__":
    bot.run(conf['token'])