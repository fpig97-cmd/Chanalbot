import discord
import os
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

TOCKEN = os.getenv("BOT_TOCKEN")

bot = commands.Bot(command_prefix="!", intents=intents)

structure = [
    {"type": "category", "name": "✅ 인증 ▬▬▬"},
    {"type": "text", "name": "✅ 닉네임-양식", "parent": "✅ 인증 ▬▬▬"},

    {"type": "category", "name": "📌 중요 ▬▬▬"},
    {"type": "text", "name": "📢 공지사항", "parent": "📌 중요 ▬▬▬"},
    {"type": "text", "name": "📢 서버-공지사항", "parent": "📌 중요 ▬▬▬"},
    {"type": "text", "name": "📢 시험공지", "parent": "📌 중요 ▬▬▬"},
    {"type": "text", "name": "📢 판매공지", "parent": "📌 중요 ▬▬▬"},
    {"type": "text", "name": "📢 개발공지", "parent": "📌 중요 ▬▬▬"},
    {"type": "text", "name": "📢 업데이트-유출", "parent": "📌 중요 ▬▬▬"},
    {"type": "text", "name": "📢 패치노트", "parent": "📌 중요 ▬▬▬"},
    {"type": "text", "name": "📢 동맹국", "parent": "📌 중요 ▬▬▬"},
    {"type": "text", "name": "📢 투표", "parent": "📌 중요 ▬▬▬"},
    {"type": "text", "name": "📢 서버부스트", "parent": "📌 중요 ▬▬▬"},
    {"type": "text", "name": "📢 이벤트", "parent": "📌 중요 ▬▬▬"},
    {"type": "text", "name": "📢 블랙리스트", "parent": "📌 중요 ▬▬▬"},

    {"type": "category", "name": "🌐 커뮤니티 ▬▬▬"},
    {"type": "text", "name": "💬 자유채팅", "parent": "🌐 커뮤니티 ▬▬▬"},
    {"type": "text", "name": "🤖 봇명령어", "parent": "🌐 커뮤니티 ▬▬▬"},
    {"type": "text", "name": "📷 사진공유", "parent": "🌐 커뮤니티 ▬▬▬"},
    {"type": "text", "name": "🚨 신고채널", "parent": "🌐 커뮤니티 ▬▬▬"},
    {"type": "text", "name": "❓ 질문포럼", "parent": "🌐 커뮤니티 ▬▬▬"},
    {"type": "text", "name": "💡 아이디어", "parent": "🌐 커뮤니티 ▬▬▬"},
    {"type": "text", "name": "📝 자유게시판", "parent": "🌐 커뮤니티 ▬▬▬"},

    {"type": "category", "name": "📑 보고서 ▬▬▬"},
    {"type": "text", "name": "📄 진급-보고서", "parent": "📑 보고서 ▬▬▬"},
    {"type": "text", "name": "📄 강등-보고서", "parent": "📑 보고서 ▬▬▬"},
    {"type": "text", "name": "📄 처벌-보고서", "parent": "📑 보고서 ▬▬▬"},
    {"type": "text", "name": "📄 밴-보고서", "parent": "📑 보고서 ▬▬▬"},
    {"type": "text", "name": "📄 타임아웃-보고서", "parent": "📑 보고서 ▬▬▬"},

    {"type": "category", "name": "🧾 행정업무 ▬▬▬"},
    {"type": "text", "name": "📄 그룹랭크-요청", "parent": "🧾 행정업무 ▬▬▬"},
    {"type": "text", "name": "📄 역할-요청", "parent": "🧾 행정업무 ▬▬▬"},

    {"type": "category", "name": "🔊 보이스 ▬▬▬"},
    {"type": "voice", "name": "🎤 스테이지", "parent": "🔊 보이스 ▬▬▬"},
    {"type": "voice", "name": "🔊 음성 1", "parent": "🔊 보이스 ▬▬▬"},
    {"type": "voice", "name": "🔊 음성 2", "parent": "🔊 보이스 ▬▬▬"},
    {"type": "voice", "name": "🔊 음성 3", "parent": "🔊 보이스 ▬▬▬"},
    {"type": "voice", "name": "🎵 노래방 1", "parent": "🔊 보이스 ▬▬▬"},
]

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def 서버셋업(ctx):
    guild = ctx.guild
    categories = {}

    await ctx.send("채널 구조를 생성하는 중입니다...")

    for item in structure:
        if item["type"] == "category":
            cat = await guild.create_category(item["name"])
            categories[item["name"]] = cat
        else:
            parent = categories.get(item["parent"])
            if item["type"] == "text":
                await guild.create_text_channel(item["name"], category=parent)
            elif item["type"] == "voice":
                await guild.create_voice_channel(item["name"], category=parent)

    await ctx.send("채널 구조 생성 완료!")

bot.run(TOCKEN)
