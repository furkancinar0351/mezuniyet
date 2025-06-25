import discord
from discord.ext import commands
from config import TOKEN, DATABASE
from sss import sss_cevap_bul  
from logic import create_tables, mesaj_kaydet  

intents = discord.Intents.default()
intents.message_content = True


bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    create_tables()  
    print(f"{bot.user} başarıyla çalışıyor.")
    await bot.change_presence(activity=discord.Game(name="!sss | destek için hazırım"))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    cevap = sss_cevap_bul(message.content)
    if cevap:
        await message.channel.send(cevap)

    await bot.process_commands(message) 

@bot.command(name="komutlar")
async def yonetici_dokumantasyonu(ctx):
    mesaj = (
        "**📘 Mağaza Yöneticisi Bot Kullanım Rehberi**\n\n"
        "**1. SSS Yanıtı:** `!sss <mesaj>` komutuyla sık sorulan sorulara yanıt alınabilir.\n"
        "**2. Veritabanı Kaydı:** Kullanıcı sorguları backend'de saklanır (bu özellik ayrıca uygulanmıştır).\n"
        "**3. Destek:** Sorun yaşarsanız sistem yöneticinizle iletişime geçebilirsiniz.\n"
    )
    await ctx.send(mesaj)


@bot.command()
async def merhaba(ctx):
    await ctx.send(f"Merhaba {ctx.author.name}, nasıl yardımcı olabilirim?")


@bot.command()
async def yardım(ctx):
    embed = discord.Embed(
        title="Destek Botu Komutları",
        description="İşte kullanabileceğin komutlar:",
        color=discord.Color.blue()
    )
    embed.add_field(name="!merhaba", value="Bot seni selamlar.", inline=False)
    embed.add_field(name="!yardım", value="Tüm komutları listeler.", inline=False)
    embed.add_field(name="!sss", value="SSS listesini gösterir.", inline=False)
    await ctx.send(embed=embed)


@bot.command()
async def sss(ctx):
    try:
        import json
        with open("sss.json", "r", encoding="utf-8") as f:
            veriler = json.load(f)

        embed = discord.Embed(
            title="Sıkça Sorulan Sorular",
            description="Sorunu aşağıdaki örneklerdeki gibi yazarsan otomatik cevap alırsın:",
            color=discord.Color.green()
        )

        for s in veriler:
            embed.add_field(name="🔹 " + s["soru"].capitalize(), value="—", inline=False)

        await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send("SSS verileri yüklenemedi.")
        print(f"[HATA - !sss]: {e}")


if __name__ == "__main__":
    bot.run(TOKEN)