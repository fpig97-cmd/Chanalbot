import os
import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

structure = [
    {"type": "category", "name": "✅ 인증 ▬▬▬"},
    {"type": "text", "name": "✅ 닉네임-양식", "parent": "✅ 인증 ▬▬▬"},

    {"type": "category", "name": "📌 중요 ▬▬▬"},
    {"type": "text", "name": "📢 공지사항", "parent": "📌 중요 ▬▬▬"},
    {"type": "text", "name": "📢 서브-공지사항", "parent": "📌 중요 ▬▬▬"},
    {"type": "text", "name": "📋 시험공지", "parent": "📌 중요 ▬▬▬"},
    {"type": "text", "name": "💵 판매공지", "parent": "📌 중요 ▬▬▬"},
    {"type": "text", "name": "🛠️ 개발공지", "parent": "📌 중요 ▬▬▬"},
    {"type": "text", "name": "👀 업데이트-유출", "parent": "📌 중요 ▬▬▬"},
    {"type": "text", "name": "📝 패치노트", "parent": "📌 중요 ▬▬▬"},
    {"type": "text", "name": "🤝 동맹국", "parent": "📌 중요 ▬▬▬"},
    {"type": "text", "name": "🗳️ 투표", "parent": "📌 중요 ▬▬▬"},
    {"type": "text", "name": "💎 서버부스트", "parent": "📌 중요 ▬▬▬"},
    {"type": "text", "name": "❗ 이벤트", "parent": "📌 중요 ▬▬▬"},
    {"type": "text", "name": "❌ 블랙리스트", "parent": "📌 중요 ▬▬▬"},

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

@bot.tree.command(name="서버셋업", description="서버 채널 구조 완전 초기화 후 재생성")
@commands.has_permissions(manage_channels=True)
async def 서버셋업(ctx):
    guild = ctx.guild  # 이 줄 먼저 선언
    
    # 확인 메시지
    confirm = await ctx.send("⚠️ **서버 모든 채널을 삭제하고 새로 생성합니다.**\n"
                           "정말 실행하시겠습니까? `확인` 또는 `취소` 입력 (30초)")
    
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel and m.content in ["확인", "취소"]
    
    try:
        response = await bot.wait_for("message", check=check, timeout=30.0)
        
        if response.content == "취소":
            await confirm.edit(content="❌ 서버셋업이 취소되었습니다.", embed=None)
            return
            
    except asyncio.TimeoutError:
        await confirm.edit(content="⏰ 30초가 지나 명령어가 자동 취소되었습니다.")
        return
    
    await confirm.edit(content="🧹 기존 채널 삭제 중...")
    
    # 모든 채널 삭제 (guild 변수 사용)
    for channel in reversed(guild.channels):
        try:
            await channel.delete()
            await asyncio.sleep(0.1)
        except discord.HTTPException:
            pass
    
    await confirm.edit(content="✅ 기존 채널 삭제 완료!\n🔨 새 채널 구조 생성 중...")
    
    categories = {}
    
    # 새 채널 생성
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
    
    embed = discord.Embed(title="🎉 서버셋업 완료!", 
                         description=f"총 **{len(structure)}개** 채널이 생성되었습니다.",
                         color=0x00ff00)
    await confirm.edit(content=None, embed=embed)

# 별도 채널 삭제 명령어
@bot.tree.command(name="채널삭제", description="서버 모든 채널 삭제")
@commands.has_permissions(manage_channels=True)
async def 채널삭제(ctx):
    guild = ctx.guild  # 여기도 추가
    
    confirm = await ctx.send("⚠️ **서버 모든 채널을 삭제합니다.**\n"
                           "`확인` 또는 `취소` 입력 (10초)")
    
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel and m.content in ["확인", "취소"]
    
    try:
        response = await bot.wait_for("message", check=check, timeout=10.0)
        
        if response.content == "취소":
            await confirm.delete()
            await ctx.send("❌ 채널 삭제가 취소되었습니다.")
            return
            
    except asyncio.TimeoutError:
        await confirm.delete()
        return
    
    await ctx.send("🧹 기존 채널 삭제 중...")
    
    # guild 변수 사용
    for channel in reversed(guild.channels):
        try:
            await channel.delete()
            await asyncio.sleep(0.1)
        except:
            pass
    
    await ctx.send("✅ 모든 채널 삭제 완료!")

bot.run(os.getenv("BOT_TOCKEN"))
