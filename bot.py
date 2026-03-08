import os
import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

structure = [
    {"type": "category", "name": "▬▬▬ 📌 중요 ▬▬▬"},
    {"type": "text", "name": "╭📢ㅣ공지사항", "parent": "▬▬▬ 📌 중요 ▬▬▬"},
    {"type": "text", "name": "ㅣ📢ㅣ서브-공지사항", "parent": "▬▬▬ 📌 중요 ▬▬▬"},
    {"type": "text", "name": "╰📋ㅣ시험공지", "parent": "▬▬▬ 📌 중요 ▬▬▬"},
    {"type": "text", "name": "╭🛠️ㅣ개발공지", "parent": "▬▬▬ 📌 중요 ▬▬▬"},
    {"type": "text", "name": "ㅣ👀ㅣ업데이트-유출", "parent": "▬▬▬ 📌 중요 ▬▬▬"},
    {"type": "text", "name": "╰📝ㅣ패치노트", "parent": "▬▬▬ 📌 중요 ▬▬▬"},
    {"type": "text", "name": "╭🤝ㅣ동맹국", "parent": "▬▬▬ 📌 중요 ▬▬▬"},
    {"type": "text", "name": "ㅣ🗳️ㅣ투표", "parent": "▬▬▬ 📌 중요 ▬▬▬"},
    {"type": "text", "name": "ㅣ💎ㅣ서버부스트", "parent": "▬▬▬ 📌 중요 ▬▬▬"},
    {"type": "text", "name": "ㅣ❗ㅣ이벤트", "parent": "▬▬▬ 📌 중요 ▬▬▬"},
    {"type": "text", "name": "╰❌ㅣ블랙리스트", "parent": "▬▬▬ 📌 중요 ▬▬▬"},

    {"type": "category", "name": "▬▬▬ 🌐 커뮤니티 ▬▬▬"},
    {"type": "text", "name": "╭💬ㅣ자유채팅", "parent": "▬▬▬ 🌐 커뮤니티 ▬▬▬"},
    {"type": "text", "name": "ㅣ🤖ㅣ봇명령어", "parent": "▬▬▬ 🌐 커뮤니티 ▬▬▬"},
    {"type": "text", "name": "ㅣ📷ㅣ사진공유", "parent": "▬▬▬ 🌐 커뮤니티 ▬▬▬"},
    {"type": "text", "name": "ㅣ🚨ㅣ신고채널", "parent": "▬▬▬ 🌐 커뮤니티 ▬▬▬"},
    {"type": "text", "name": "ㅣ❓ㅣ질문포럼", "parent": "▬▬▬ 🌐 커뮤니티 ▬▬▬"},
    {"type": "text", "name": "ㅣ💡ㅣ아이디어", "parent": "▬▬▬ 🌐 커뮤니티 ▬▬▬"},
    {"type": "text", "name": "╰📝ㅣ자유게시판", "parent": "▬▬▬ 🌐 커뮤니티 ▬▬▬"},
    
    {"type": "category", "name": "▬▬▬ 🔊 보이스 ▬▬▬"},
    {"type": "voice", "name": "╭🎤ㅣ 스테이지", "parent": "▬▬▬ 🔊 보이스 ▬▬▬"},
    {"type": "voice", "name": "ㅣ🔊 음성 1", "parent": "▬▬▬ 🔊 보이스 ▬▬▬"},
    {"type": "voice", "name": "ㅣ🔊ㅣ음성 2", "parent": "▬▬▬ 🔊 보이스 ▬▬▬"},
    {"type": "voice", "name": "ㅣ🔊ㅣ음성 3", "parent": "▬▬▬ 🔊 보이스 ▬▬▬"},
    {"type": "voice", "name": "╰🎵ㅣ노래방 1", "parent": "▬▬▬ 🔊 보이스 ▬▬▬"},
]

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} slash command(s)")
    except Exception as e:
        print(f"❌ Failed to sync commands: {e}")

@bot.tree.command(name="서버셋업", description="서버 채널 구조 완전 초기화 후 재생성")
async def 서버셋업(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.manage_channels:
        await interaction.response.send_message("❌ **채널 관리 권한**이 필요합니다.", ephemeral=True)
        return
    
    guild = interaction.guild
    keep_channel = interaction.channel  # 이 채널은 살려둠

    await interaction.response.send_message(
        "⚠️ **서버 모든 채널을 삭제하고 새로 생성합니다.**\n"
        "정말 실행하시겠습니까? `확인` 또는 `취소` 입력 (30초)",
        ephemeral=True
    )
    
    def check(m: discord.Message):
        return (
            m.author == interaction.user and
            m.channel == keep_channel and
            m.content in ["확인", "취소"]
        )
    
    try:
        response = await bot.wait_for("message", check=check, timeout=30.0)
        if response.content == "취소":
            await interaction.followup.send("❌ 서버셋업이 취소되었습니다.", ephemeral=True)
            return
    except asyncio.TimeoutError:
        await interaction.followup.send("⏰ 30초가 지나 명령어가 자동 취소되었습니다.", ephemeral=True)
        return

    await interaction.followup.send("🧹 기존 채널 삭제 중...", ephemeral=True)

    # 🔹 현재 채널은 제외하고 삭제
    for channel in list(guild.channels):
        if channel.id == keep_channel.id:
            continue
        try:
            await channel.delete()
            await asyncio.sleep(0.1)
        except discord.HTTPException:
            pass

    await interaction.followup.send("✅ 기존 채널 삭제 완료!\n🔨 새 채널 구조 생성 중...", ephemeral=True)

    # 🔹 구조 생성 (기존 코드 그대로 사용)
    categories: dict[str, discord.CategoryChannel] = {}
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

    embed = discord.Embed(
        title="🎉 서버셋업 완료!",
        description=f"총 **{len(structure)}개** 채널이 생성되었습니다.\n"
                    f"현재 채널은 유지된 상태입니다.",
        color=0x00ff00
    )
    await interaction.followup.send(embed=embed, ephemeral=True)

bot.run(os.getenv("BOT_TOCKEN"))
