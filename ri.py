import discord
from discord.ext import commands
import json
import os
import random
import asyncio
from datetime import datetime
import math
from typing import Optional, Dict, List

# Configuration
CONFIG = {
    "owner_ids": [1078878279433469983],  # Replace with your 2 Discord IDs
    "bot_token": "MTM4NDg3ODM4NDE5ODE5MzI2NQ.GhFPuw.NoA_2b-GmneevAR78xE65w-0iNyO_jbAZr2wQc",  # Replace with your bot token
    "data_files": {
        "players": "data/players.json",
        "realms": "data/realms.json",
        "weapons": "data/weapons.json",
        "sects": "data/sects.json"
    },
    "gacha_cost": 150,
    "work_cooldown": 3600,  # 1 hour in seconds
    "gacha_cooldown": 300,  # 5 minutes in seconds
    "breakthrough_cooldown": 86400,  # 24 hours in seconds
    "colors": {
        "primary": 0x5865F2,
        "success": 0x57F287,
        "warning": 0xFEE75C,
        "danger": 0xED4245,
        "cultivation": 0x9B59B6,
        "gacha": 0xE91E63
    },
    "default_files": {
        "players.json": {},
        "realms.json": {
            "step1": [
                {"mandarin": "凝气", "pinyin": "Níng qì", "english": "Qi Condensation", "xp_required": 100, "power": 1.0},
                {"mandarin": "筑基", "pinyin": "Zhù jī", "english": "Foundation Establishment", "xp_required": 300, "power": 1.5},
                {"mandarin": "结丹", "pinyin": "Jié dān", "english": "Core Formation", "xp_required": 900, "power": 2.2},
                {"mandarin": "化神", "pinyin": "Huà shén", "english": "Nascent Soul", "xp_required": 2700, "power": 3.3},
                {"mandarin": "化神", "pinyin": "Huà shén", "english": "Soul Formation", "xp_required": 8100, "power": 5.0},
                {"mandarin": "婴变", "pinyin": "Yīng biàn", "english": "Soul Transformation", "xp_required": 24300, "power": 7.5},
                {"mandarin": "问鼎", "pinyin": "Wèn dǐng", "english": "Ascendant", "xp_required": 72900, "power": 11.2}
            ],
            "step2": [
                {"mandarin": "阴虚", "pinyin": "Yīn xū", "english": "Illusory Yin", "xp_required": 100000, "power": 16.8},
                {"mandarin": "阳实", "pinyin": "Yáng shí", "english": "Corporeal Yang", "xp_required": 300000, "power": 25.2},
                {"mandarin": "窥涅", "pinyin": "Kuī niè", "english": "Nirvana Scryer", "xp_required": 900000, "power": 37.8},
                {"mandarin": "净涅", "pinyin": "Jìng niè", "english": "Nirvana Cleanser", "xp_required": 2700000, "power": 56.7},
                {"mandarin": "碎涅", "pinyin": "Suì niè", "english": "Nirvana Shatterer", "xp_required": 8100000, "power": 85.0},
                {"mandarin": "破空五指", "pinyin": "Pò kōng wǔ zhǐ", "english": "Heaven's Blight", "xp_required": 24300000, "power": 127.5}
            ],
            "step3": [
                {"english": "Nirvana Void", "xp_required": 50000000, "power": 191.2},
                {"english": "Spirit Void", "xp_required": 100000000, "power": 286.8},
                {"english": "Arcane Void", "xp_required": 200000000, "power": 430.2},
                {"english": "Void Tribulant", "xp_required": 400000000, "power": 645.3},
                {"english": "Great Exalt", "xp_required": 800000000, "power": 968.0},
                {"english": "Golden Exalt", "xp_required": 1600000000, "power": 1452.0},
                {"english": "Empyrean Exalt", "xp_required": 3200000000, "power": 2178.0},
                {"english": "Ascendant Empyrean", "xp_required": 6400000000, "power": 3267.0},
                {"english": "Grand Empyrean", "xp_required": 12800000000, "power": 4900.5},
                {"english": "Half-Step Heaven Trampling", "xp_required": 25600000000, "power": 7350.8},
                {"english": "Heaven Trampling", "xp_required": 51200000000, "power": 11026.2}
            ],
            "ancient_god": [
                {"stars": 1, "equivalent": "Qi Condensation - Core Formation", "xp_required": 100000, "power": 15.0},
                {"stars": 2, "equivalent": "Nascent Soul - Soul Formation", "xp_required": 300000, "power": 22.5},
                {"stars": 3, "equivalent": "Soul Transformation - Yin/Yang", "xp_required": 900000, "power": 33.8},
                {"stars": 4, "equivalent": "Nirvana Scryer", "xp_required": 2700000, "power": 50.6},
                {"stars": 5, "equivalent": "Nirvana Cleanser - Shatterer", "xp_required": 8100000, "power": 75.9},
                {"stars": 6, "equivalent": "Heaven's Blight", "xp_required": 24300000, "power": 113.9},
                {"stars": 7, "equivalent": "Nirvana Void", "xp_required": 50000000, "power": 170.8},
                {"stars": 8, "equivalent": "Spirit Void", "xp_required": 100000000, "power": 256.2},
                {"stars": 9, "equivalent": "Arcane Void", "xp_required": 200000000, "power": 384.3},
                {"stars": 10, "equivalent": "Void Tribulant", "xp_required": 400000000, "power": 576.5},
                {"stars": 11, "xp_required": 600000000, "power": 864.7},
                {"stars": 12, "xp_required": 800000000, "power": 1297.1},
                {"stars": 13, "xp_required": 1000000000, "power": 1945.6},
                {"stars": 14, "xp_required": 1200000000, "power": 2918.4},
                {"stars": 15, "xp_required": 1400000000, "power": 4377.6},
                {"stars": 16, "xp_required": 1600000000, "power": 6566.4},
                {"stars": 17, "xp_required": 1800000000, "power": 9849.6},
                {"stars": 18, "xp_required": 2000000000, "power": 14774.4},
                {"stars": 19, "xp_required": 2200000000, "power": 22161.6},
                {"stars": 20, "xp_required": 2400000000, "power": 33242.4},
                {"stars": 21, "xp_required": 2600000000, "power": 49863.6},
                {"stars": 22, "xp_required": 2800000000, "power": 74795.4},
                {"stars": 23, "xp_required": 3000000000, "power": 112193.1},
                {"stars": 24, "xp_required": 3200000000, "power": 168289.7},
                {"stars": 25, "xp_required": 3400000000, "power": 252434.5},
                {"stars": 26, "xp_required": 3600000000, "power": 378651.8},
                {"stars": 27, "xp_required": 3800000000, "power": 567977.7},
                {"stars": "Grand Empyrean", "xp_required": 5000000000, "power": 800000.0},
                {"stars": "Half-Step Heaven Trampling", "xp_required": 7500000000, "power": 1200000.0},
                {"stars": "Heaven Trampling", "xp_required": 10000000000, "power": 1800000.0}
            ]
        },
        "weapons.json": {
            "basic": [
                {"name": "Iron Sword", "power": 1.1, "description": "A basic iron sword used by novice cultivators."},
                {"name": "Wooden Staff", "power": 1.0, "description": "A simple wooden staff for channeling qi."},
                {"name": "Bronze Dagger", "power": 1.2, "description": "A short bronze dagger with modest power."}
            ],
            "rare": [
                {"name": "Frost Blade", "power": 1.8, "description": "A blade imbued with frost energy."},
                {"name": "Flame Whip", "power": 1.7, "description": "A whip that burns with spiritual flames."},
                {"name": "Jade Fan", "power": 1.6, "description": "An elegant fan that channels wind energy."}
            ],
            "epic": [
                {"name": "Wealth Sword", "power": 2.5, "description": "Wang Lin's first sword, carries mysterious power."},
                {"name": "Core-Treasure Sword", "power": 2.7, "description": "A sword with teleportation effects."},
                {"name": "Half-Moon Blade", "power": 2.6, "description": "A curved blade that glows like the moon."}
            ],
            "legend": [
                {"name": "God Slaying Spear (Illusory)", "power": 4.0, "description": "A spear capable of slaying gods (illusory version)."},
                {"name": "Blood Slaughter Sword", "power": 4.2, "description": "One of the 7 Ancient Dao Swords."},
                {"name": "Yin Blade", "power": 3.9, "description": "A sword of essential yin energy."}
            ],
            "step": [
                {"name": "Karma Whip", "power": 6.0, "description": "A whip connected to the domain of karma."},
                {"name": "18 Hell Celestial Sealing Stamp", "power": 6.5, "description": "A stamp that can seal spiritual realms."},
                {"name": "Rain Celestial Sword", "power": 5.8, "description": "Xu Liguo's sword of moderate quality."}
            ],
            "ancient": [
                {"name": "Ancient God Trident (Destroyed)", "power": 10.0, "description": "A remnant of an Ancient God's weapon."},
                {"name": "Axe of Giant Demon Clan (Destroyed)", "power": 9.5, "description": "A destroyed axe from the Giant Demon Clan."},
                {"name": "Seven-Colored Nail", "power": 11.0, "description": "An ancient Void artifact of immense power."}
            ],
            "mythical": [
                {"name": "Pearl of Defiance", "power": 50.0, "description": "Grants 10,000 XP instantly and unlocks secret paths."}
            ]
        },
        "sects.json": [
            {
                "name": "Soul Refining Sect",
                "buff": "+20% Spiritual XP and +10% drop rate for spiritual/rare weapons"
            },
            {
                "name": "Heavenly Fate Sect",
                "buff": "+10% chance to get rare characters in gacha"
            },
            {
                "name": "Heng Yue Sect",
                "buff": "+15% general loot and +10% XP from domain quests"
            },
            {
                "name": "Fighting Evil Sect",
                "buff": "+10% damage vs undead & +15% battle quest drops"
            },
            {
                "name": "Corpse Sect",
                "buff": "+8% HP regen & +12% resistance to necrotic damage"
            },
            {
                "name": "Xuan Dao Sect",
                "buff": "-20% quest cooldown & +10% void XP absorption"
            },
            {
                "name": "Cloud Sky Sect",
                "buff": "+10% crafting success & +10% jade/stones yield"
            },
            {
                "name": "Da Lou Sword Sect",
                "buff": "-10% weapon ability cooldown & +15% sword damage"
            },
            {
                "name": "Vermilion Bird Divine Sect",
                "buff": "Unlocks Vermilion Mark skill (+10% all XP after threshold)"
            },
            {
                "name": "Origin Sect",
                "buff": "+10% world exploration XP & +5% secret loot"
            },
            {
                "name": "Great Soul Sect",
                "buff": "+15% Soul-based skill power & +10% soul XP"
            },
            {
                "name": "War God Shrine Sect",
                "buff": "+20% war quest rewards & +5% power in global events"
            },
            {
                "name": "Scarlet Soul Sect",
                "buff": "+15% blood-slaughter synergy & +10% vampiric healing"
            },
            {
                "name": "Purple Dao Sect",
                "buff": "Unlocks Purple Dao passive (+15% cooldown reduction)"
            },
            {
                "name": "Celestial Dragon Sect",
                "buff": "+10% ranged/parry & +5% elemental resistance"
            },
            {
                "name": "Blue Dragon Sect",
                "buff": "+15% water/ice aura power"
            },
            {
                "name": "Thunder Celestial Temple",
                "buff": "+15% thunder damage & +10% lightning XP absorption"
            },
            {
                "name": "Tian Dao Sect",
                "buff": "+10% divine jurisprudence XP & +5% law resistance"
            },
            {
                "name": "Treasure Jade Sect",
                "buff": "+15% shard drop rate & +10% jade gem quality"
            },
            {
                "name": "Slaughter Realm",
                "buff": "+20% burst damage on critical health targets"
            },
            {
                "name": "School of Heaven",
                "buff": "+10% Heavenly realm XP & unlocks divine buff"
            }
        ]
    }
}

# Ensure data directory exists
os.makedirs("data", exist_ok=True)

# Initialize data files if they don't exist
for filename, content in CONFIG["default_files"].items():
    filepath = os.path.join("data", filename)
    if not os.path.exists(filepath):
        with open(filepath, "w", encoding='utf-8') as f:
            json.dump(content, f, indent=2, ensure_ascii=False)

# Load data files
def load_data(filename: str) -> Dict:
    filepath = os.path.join("data", filename)
    try:
        with open(filepath, "r", encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return CONFIG["default_files"].get(filename, {})

def save_data(filename: str, data: Dict):
    filepath = os.path.join("data", filename)
    with open(filepath, "w", encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# Bot setup
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

# Custom Help Command
class CultivationHelp(commands.HelpCommand):
    def __init__(self):
        super().__init__(
            command_attrs={
                "help": "Menampilkan menu bantuan sistem kultivasi",
                "hidden": True
            }
        )

    async def send_bot_help(self, mapping):
        embed = discord.Embed(
            title="📜 **Buku Manual Kultivasi** 📜",
            description="Gunakan `!help <command>` untuk detail lebih lanjut\n",
            color=CONFIG["colors"]["primary"]
        )
        
        # Add thumbnail
        embed.set_thumbnail(url="https://i.imgur.com/taq9p8k.png")
        
        # Command categories
        categories = {
            "🌱 **Dasar**": [
                ("!register", "Memulai perjalanan kultivasi"),
                ("!profile", "Lihat progres kultivasi"),
                ("!inventory", "Lihat inventory")
            ],
            "⚔️ **Kultivasi**": [
                ("!work", "Latih kultivasi (1h cooldown)"),
                ("!breakthrough", "Naik realm (24h cooldown)"),
                ("!suicide", "Reinkarnasi (reset dengan bonus)")
            ],
            "🎰 **Gacha**": [
                ("!gacha", "Gacha senjata (150 gold)")
            ]
        }

        for category, cmds in categories.items():
            embed.add_field(
                name=category,
                value="\n".join(f"`{cmd[0]}` - {cmd[1]}" for cmd in cmds),
                inline=False
            )

        embed.set_footer(text=f"Requested by {self.context.author.display_name}")
        await self.context.send(embed=embed)

    async def send_command_help(self, command):
        # Skip hidden commands
        if command.hidden:
            return
            
        embed = discord.Embed(
            title=f"📖 **Help: {command.name}**",
            color=CONFIG["colors"]["primary"]
        )
        
        if command.help:
            embed.description = command.help
        
        if hasattr(command, 'usage'):
            embed.add_field(
                name="Cara Pakai",
                value=f"```\n!{command.name} {command.usage if command.usage else ''}\n```",
                inline=False
            )
        
        await self.context.send(embed=embed)

bot.help_command = CultivationHelp()

# Player management
def get_player(user_id: int) -> Optional[Dict]:
    players = load_data("players.json")
    return players.get(str(user_id))

def create_player(user_id: int) -> Dict:
    players = load_data("players.json")
    if str(user_id) not in players:
        players[str(user_id)] = {
            "step": 1,
            "realm": 0,
            "spiritual_xp": 0,
            "comprehension_xp": 0,
            "essence_xp": 0,
            "ancient_xp": 0,
            "gold": 100,
            "inventory": [],
            "sect": None,
            "reincarnations": 0,
            "xp_bonus": 0,
            "last_work": None,
            "last_gacha": None,
            "last_breakthrough": None,
            "ancient_god": False,
            "ancient_stars": 0,
            "legacy_fragments": 0,
            "has_true_legacy": False
        }
        save_data("players.json", players)
    return players[str(user_id)]

def update_player(user_id: int, data: Dict):
    players = load_data("players.json")
    players[str(user_id)] = data
    save_data("players.json", players)

# Helper functions
def get_current_realm(player: Dict) -> Dict:
    realms = load_data("realms.json")
    if player["ancient_god"]:
        return realms["ancient_god"][player["ancient_stars"]]
    
    step = f"step{player['step']}"
    return realms[step][player["realm"]]

def can_breakthrough(player: Dict) -> bool:
    realms = load_data("realms.json")
    
    if player["ancient_god"]:
        if player["ancient_stars"] + 1 >= len(realms["ancient_god"]):
            return False
        next_realm = realms["ancient_god"][player["ancient_stars"] + 1]
        return player["ancient_xp"] >= next_realm["xp_required"]
    
    step = f"step{player['step']}"
    if player["realm"] + 1 >= len(realms[step]):
        if player["step"] == 3:
            return False
        return True
    
    next_realm = realms[step][player["realm"] + 1]
    if player["step"] == 1:
        return player["spiritual_xp"] >= next_realm["xp_required"]
    elif player["step"] == 2:
        return player["comprehension_xp"] >= next_realm["xp_required"]
    else:
        return player["essence_xp"] >= next_realm["xp_required"]

def calculate_power(player: Dict) -> float:
    realms = load_data("realms.json")
    weapons = load_data("weapons.json")
    
    # Base power from realm
    realm = get_current_realm(player)
    power = realm["power"]
    
    # Power from weapons
    weapon_power = 1.0
    for item in player["inventory"]:
        for rarity in weapons:
            for weapon in weapons[rarity]:
                if weapon["name"] == item:
                    weapon_power *= weapon["power"]
                    break
    
    # Reincarnation bonus
    power *= (1 + player["reincarnations"] * 0.1)
    
    return power * weapon_power

def format_realm_info(player: Dict, current_realm: Dict) -> str:
    if player["ancient_god"]:
        return (
            f"⭐ **{player['ancient_stars']}-Star Ancient God** ⭐\n"
            f"Equivalent: {current_realm.get('equivalent', 'Cosmic level')}"
        )
    
    realm_name = current_realm.get('english', 'Unknown Realm')
    mandarin = current_realm.get('mandarin', '')
    pinyin = current_realm.get('pinyin', '')
    
    info = f"**{realm_name}**"
    if mandarin:
        info += f" ({mandarin}"
        if pinyin:
            info += f", {pinyin}"
        info += ")"
    
    step = player['step']
    realm_num = player['realm'] + 1
    total_realms = len(load_data("realms.json")[f"step{step}"])
    
    info += f"\nStep {step}, Realm {realm_num}/{total_realms}"
    return info

# Commands
@bot.command(
    name="register",
    help="Memulai perjalanan kultivasi dengan memilih sekte",
    usage=""
)
async def register(ctx):
    player = get_player(ctx.author.id)
    if player:
        embed = discord.Embed(
            title="❌ Sudah Terdaftar",
            description="Anda sudah terdaftar sebagai kultivator!",
            color=CONFIG["colors"]["danger"]
        )
        await ctx.send(embed=embed)
        return
    
    sects = load_data("sects.json")
    
    embed = discord.Embed(
        title="🏛️ Pilih Sekte Kultivasi",
        description="Pilih sekte dengan mengirim nomor yang sesuai:\n",
        color=CONFIG["colors"]["primary"]
    )
    
    for i, sect in enumerate(sects, 1):
        embed.add_field(
            name=f"{i}. {sect['name']}",
            value=sect['buff'],
            inline=False
        )
    
    embed.set_footer(text="Anda memiliki 1 menit untuk memilih")
    await ctx.send(embed=embed)
    
    def check(m):
        return (
            m.author == ctx.author and 
            m.channel == ctx.channel and 
            m.content.isdigit() and 
            1 <= int(m.content) <= len(sects)
        )
    
    try:
        msg = await bot.wait_for("message", check=check, timeout=60)
        sect_index = int(msg.content) - 1
        sect = sects[sect_index]
        
        create_player(ctx.author.id)
        player = get_player(ctx.author.id)
        player["sect"] = sect["name"]
        update_player(ctx.author.id, player)
        
        embed = discord.Embed(
            title=f"🎉 Selamat Bergabung dengan {sect['name']}!",
            description=sect['buff'],
            color=CONFIG["colors"]["success"]
        )
        await ctx.send(embed=embed)
    except asyncio.TimeoutError:
        embed = discord.Embed(
            title="⏰ Waktu Habis",
            description="Pendaftaran dibatalkan karena waktu habis",
            color=CONFIG["colors"]["danger"]
        )
        await ctx.send(embed=embed)

@bot.command(
    name="work",
    help="Melatih kultivasi untuk mendapatkan XP spiritual dan pemahaman",
    usage=""
)
async def work(ctx):
    player = get_player(ctx.author.id)
    if not player:
        embed = discord.Embed(
            title="❌ Belum Terdaftar",
            description="Silakan registrasi dulu dengan !register",
            color=CONFIG["colors"]["danger"]
        )
        await ctx.send(embed=embed)
        return
    
    current_time = datetime.now().timestamp()
    if player["last_work"] and (current_time - player["last_work"]) < CONFIG["work_cooldown"]:
        remaining = CONFIG["work_cooldown"] - (current_time - player["last_work"])
        hours, remainder = divmod(remaining, 3600)
        minutes = remainder // 60
        
        embed = discord.Embed(
            title="⏳ Cooldown",
            description=f"Anda perlu menunggu {int(hours)} jam {int(minutes)} menit sebelum bekerja lagi",
            color=CONFIG["colors"]["warning"]
        )
        await ctx.send(embed=embed)
        return
    
    base_spiritual = random.randint(10, 30)
    base_comprehension = random.randint(5, 20)
    
    # Apply sect bonuses
    if "Spiritual XP" in player["sect"]:
        base_spiritual = int(base_spiritual * 1.2)
    if "XP from domain quests" in player["sect"]:
        base_comprehension = int(base_comprehension * 1.1)
    
    # Apply reincarnation bonus
    if player["xp_bonus"] > 0:
        base_spiritual += player["xp_bonus"]
        base_comprehension += player["xp_bonus"]
    
    player["spiritual_xp"] += base_spiritual
    player["comprehension_xp"] += base_comprehension
    player["last_work"] = current_time
    update_player(ctx.author.id, player)
    
    embed = discord.Embed(
        title="🧘 Latihan Kultivasi Berhasil",
        description=f"Anda mendapatkan:\n"
                   f"✨ **{base_spiritual} Spiritual XP**\n"
                   f"📚 **{base_comprehension} Comprehension XP**",
        color=CONFIG["colors"]["success"]
    )
    await ctx.send(embed=embed)

@bot.command(
    name="gacha",
    help="Menggacha senjata dengan biaya 150 gold",
    usage=""
)
async def gacha(ctx):
    player = get_player(ctx.author.id)
    if not player:
        embed = discord.Embed(
            title="❌ Belum Terdaftar",
            description="Silakan registrasi dulu dengan !register",
            color=CONFIG["colors"]["danger"]
        )
        await ctx.send(embed=embed)
        return
    
    current_time = datetime.now().timestamp()
    if player["last_gacha"] and (current_time - player["last_gacha"]) < CONFIG["gacha_cooldown"]:
        remaining = CONFIG["gacha_cooldown"] - (current_time - player["last_gacha"])
        minutes = remaining // 60
        
        embed = discord.Embed(
            title="⏳ Cooldown",
            description=f"Anda perlu menunggu {int(minutes)} menit sebelum gacha lagi",
            color=CONFIG["colors"]["warning"]
        )
        await ctx.send(embed=embed)
        return
    
    if player["gold"] < CONFIG["gacha_cost"]:
        embed = discord.Embed(
            title="❌ Gold Tidak Cukup",
            description=f"Anda butuh {CONFIG['gacha_cost']} gold untuk gacha. Gold anda: {player['gold']}",
            color=CONFIG["colors"]["danger"]
        )
        await ctx.send(embed=embed)
        return
    
    player["gold"] -= CONFIG["gacha_cost"]
    player["last_gacha"] = current_time
    
    roll = random.random() * 100
    weapons = load_data("weapons.json")
    item = None
    rarity = ""
    color = CONFIG["colors"]["primary"]
    
    if roll < 0.0000001:  # Pearl of Defiance
        item = weapons["mythical"][0]
        rarity = "MYTHICAL"
        color = 0xFFD700  # Gold
        player["spiritual_xp"] += 10000
        player["comprehension_xp"] += 10000
        player["essence_xp"] += 10000
    elif roll < 0.1:  # Ancient weapon
        item = random.choice(weapons["ancient"])
        rarity = "ANCIENT"
        color = 0x800080  # Purple
        player["legacy_fragments"] += 1
    elif roll < 1.1:  # Step weapon
        item = random.choice(weapons["step"])
        rarity = "STEP"
        color = 0x00FF00  # Green
    elif roll < 3.1:  # Legend weapon
        item = random.choice(weapons["legend"])
        rarity = "LEGEND"
        color = 0xFF4500  # OrangeRed
    elif roll < 9.1:  # Epic weapon
        item = random.choice(weapons["epic"])
        rarity = "EPIC"
        color = 0x9932CC  # DarkOrchid
    elif roll < 21.1:  # Rare weapon
        item = random.choice(weapons["rare"])
        rarity = "RARE"
        color = 0x1E90FF  # DodgerBlue
        if "rare weapons" in player["sect"] and random.random() < 0.1:
            bonus_item = random.choice(weapons["rare"])
            player["inventory"].append(bonus_item["name"])
    else:  # Basic weapon
        item = random.choice(weapons["basic"])
        rarity = "BASIC"
        color = 0xC0C0C0  # Silver
    
    player["inventory"].append(item["name"])
    
    if roll < 2.1:  # 1-2% chance
        frags = random.randint(1, 2)
        player["legacy_fragments"] += frags
    
    if roll < 2.0:  # 2% chance
        player["has_true_legacy"] = True
    
    if roll < 5.0:  # 5% chance
        xp_type = random.choice(["spiritual", "comprehension"])
        amount = random.randint(10, 50)
        if xp_type == "spiritual":
            player["spiritual_xp"] += amount
        else:
            player["comprehension_xp"] += amount
    
    update_player(ctx.author.id, player)
    
    embed = discord.Embed(
        title=f"🎁 Anda Mendapatkan: {rarity}",
        description=f"**{item['name']}**\n{item['description']}",
        color=color
    )
    embed.set_footer(text=f"Gold tersisa: {player['gold']}")
    
    if rarity == "MYTHICAL":
        embed.add_field(
            name="✨ Bonus XP",
            value="+10,000 semua jenis XP!",
            inline=False
        )
    
    await ctx.send(embed=embed)

@bot.command(
    name="breakthrough",
    help="Mencapai realm berikutnya dalam kultivasi",
    usage=""
)
async def breakthrough(ctx):
    player = get_player(ctx.author.id)
    if not player:
        embed = discord.Embed(
            title="❌ Belum Terdaftar",
            description="Silakan registrasi dulu dengan !register",
            color=CONFIG["colors"]["danger"]
        )
        await ctx.send(embed=embed)
        return
    
    current_time = datetime.now().timestamp()
    if player["last_breakthrough"] and (current_time - player["last_breakthrough"]) < CONFIG["breakthrough_cooldown"]:
        remaining = CONFIG["breakthrough_cooldown"] - (current_time - player["last_breakthrough"])
        hours = remaining // 3600
        minutes = (remaining % 3600) // 60
        
        embed = discord.Embed(
            title="⏳ Cooldown",
            description=f"Anda perlu menunggu {int(hours)} jam {int(minutes)} menit sebelum breakthrough lagi",
            color=CONFIG["colors"]["warning"]
        )
        await ctx.send(embed=embed)
        return
    
    realms = load_data("realms.json")
    
    if not can_breakthrough(player):
        embed = discord.Embed(
            title="❌ Belum Memenuhi Syarat",
            description="Anda belum memenuhi syarat untuk breakthrough",
            color=CONFIG["colors"]["danger"]
        )
        await ctx.send(embed=embed)
        return
    
    if player["ancient_god"]:
        player["ancient_stars"] += 1
        next_realm = realms["ancient_god"][player["ancient_stars"]]
        player["last_breakthrough"] = current_time
        update_player(ctx.author.id, player)
        
        embed = discord.Embed(
            title="🌟 Ancient God Ascension 🌟",
            description=f"Anda sekarang menjadi **{player['ancient_stars']}-Star Ancient God**!\n"
                       f"Equivalent: {next_realm.get('equivalent', 'Cosmic level')}",
            color=0x800080
        )
        await ctx.send(embed=embed)
        return
    
    step = f"step{player['step']}"
    if player["realm"] + 1 < len(realms[step]):  # Next realm in current step
        player["realm"] += 1
        next_realm = realms[step][player["realm"]]
        player["last_breakthrough"] = current_time
        update_player(ctx.author.id, player)
        
        embed = discord.Embed(
            title="✨ Breakthrough Berhasil ✨",
            description=f"Anda sekarang mencapai realm **{next_realm['english']}**!",
            color=CONFIG["colors"]["success"]
        )
        
        if 'mandarin' in next_realm:
            embed.add_field(
                name="Mandarin",
                value=f"{next_realm['mandarin']} ({next_realm['pinyin']})",
                inline=False
            )
        
        await ctx.send(embed=embed)
    else:  # Next step
        if player["step"] == 3:
            embed = discord.Embed(
                title="🏆 Puncak Kultivasi",
                description="Anda telah mencapai puncak kultivasi!",
                color=0xFFD700
            )
            await ctx.send(embed=embed)
            return
        
        if (player["step"] == 2 and 
            (player["realm"] == len(realms["step2"]) - 1 or
             player["legacy_fragments"] >= 10 or 
             player["has_true_legacy"])):
            
            embed = discord.Embed(
                title="⚡ Ancient God Path Unlocked!",
                description="Anda telah membuka jalan Ancient God! Apakah anda ingin:\n"
                           "1. Lanjut ke Step 3 biasa\n"
                           "2. Memulai sebagai 1-Star Ancient God\n\n"
                           "Balas dengan angka pilihan anda",
                color=0x800080
            )
            await ctx.send(embed=embed)
            
            def check(m):
                return (
                    m.author == ctx.author and 
                    m.channel == ctx.channel and 
                    m.content in ["1", "2"])
            
            try:
                msg = await bot.wait_for("message", check=check, timeout=30)
                if msg.content == "2":
                    player["ancient_god"] = True
                    player["ancient_stars"] = 1
                    player["step"] = 3
                    player["last_breakthrough"] = current_time
                    update_player(ctx.author.id, player)
                    
                    embed = discord.Embed(
                        title="🌟 Memulai Jalan Ancient God 🌟",
                        description="Anda sekarang menjadi **1-Star Ancient God**!",
                        color=0x800080
                    )
                    await ctx.send(embed=embed)
                    return
            except asyncio.TimeoutError:
                pass
        
        player["step"] += 1
        player["realm"] = 0
        player["last_breakthrough"] = current_time
        update_player(ctx.author.id, player)
        
        next_step = f"step{player['step']}"
        next_realm = realms[next_step][0]
        
        embed = discord.Embed(
            title="🌀 Naik Step Kultivasi 🌀",
            description=f"Selamat! Anda mencapai **Step {player['step']}** dan realm **{next_realm['english']}**!",
            color=CONFIG["colors"]["success"]
        )
        await ctx.send(embed=embed)

@bot.command(
    name="suicide",
    help="Reinkarnasi untuk memulai ulang dengan bonus XP",
    usage=""
)
async def suicide(ctx):
    player = get_player(ctx.author.id)
    if not player:
        embed = discord.Embed(
            title="❌ Belum Terdaftar",
            description="Silakan registrasi dulu dengan !register",
            color=CONFIG["colors"]["danger"]
        )
        await ctx.send(embed=embed)
        return
    
    embed = discord.Embed(
        title="☯️ Konfirmasi Reinkarnasi",
        description="Apakah anda yakin ingin reinkarnasi?\n"
                   "Ini akan mereset semua progres kecuali inventory dan status Ancient God.\n"
                   "Balas dengan `confirm` untuk melanjutkan atau `cancel` untuk membatalkan.",
        color=CONFIG["colors"]["warning"]
    )
    await ctx.send(embed=embed)
    
    def check(m):
        return (
            m.author == ctx.author and 
            m.channel == ctx.channel and 
            m.content.lower() in ["confirm", "cancel"])
    
    try:
        msg = await bot.wait_for("message", check=check, timeout=30)
        if msg.content.lower() != "confirm":
            embed = discord.Embed(
                title="❌ Reinkarnasi Dibatalkan",
                color=CONFIG["colors"]["danger"]
            )
            await ctx.send(embed=embed)
            return
    except asyncio.TimeoutError:
        embed = discord.Embed(
            title="⏳ Waktu Habis",
            description="Reinkarnasi dibatalkan karena waktu habis",
            color=CONFIG["colors"]["danger"]
        )
        await ctx.send(embed=embed)
        return
    
    xp_bonus = 0
    if player["step"] >= 2 or player["ancient_god"]:
        xp_bonus = random.randint(1, 15)
    
    player["step"] = 1
    player["realm"] = 0
    player["spiritual_xp"] = 0
    player["comprehension_xp"] = 0
    player["essence_xp"] = 0
    player["ancient_xp"] = 0
    player["reincarnations"] += 1
    player["xp_bonus"] = xp_bonus
    player["last_work"] = None
    player["last_gacha"] = None
    player["last_breakthrough"] = None
    
    if player["ancient_god"]:
        player["ancient_stars"] = 0
    
    update_player(ctx.author.id, player)
    
    embed = discord.Embed(
        title="🌀 Reinkarnasi Berhasil 🌀",
        description=f"Anda telah bereinkarnasi!\n"
                   f"Total reinkarnasi: {player['reincarnations']}\n"
                   f"{f'Bonus XP: +{xp_bonus} untuk semua aksi' if xp_bonus > 0 else ''}",
        color=CONFIG["colors"]["success"]
    )
    await ctx.send(embed=embed)

@bot.command(
    name="profile",
    help="Menampilkan profil kultivasi anda",
    usage=""
)
async def profile(ctx):
    player = get_player(ctx.author.id)
    if not player:
        embed = discord.Embed(
            title="❌ Belum Terdaftar",
            description="Silakan registrasi dulu dengan !register",
            color=CONFIG["colors"]["danger"]
        )
        await ctx.send(embed=embed)
        return
    
    realms = load_data("realms.json")
    current_realm = get_current_realm(player)
    power = calculate_power(player)
    
    # Format realm info
    realm_info = format_realm_info(player, current_realm)
    
    # Format XP progress
    xp_info = ""
    if player["step"] == 1:
        next_realm = realms["step1"][player["realm"] + 1] if player["realm"] + 1 < len(realms["step1"]) else None
        if next_realm:
            xp_info = f"**Spiritual XP**: {player['spiritual_xp']}/{next_realm['xp_required']}"
    elif player["step"] == 2:
        next_realm = realms["step2"][player["realm"] + 1] if player["realm"] + 1 < len(realms["step2"]) else None
        if next_realm:
            xp_info = f"**Comprehension XP**: {player['comprehension_xp']}/{next_realm['xp_required']}"
    else:
        next_realm = realms["step3"][player["realm"] + 1] if player["realm"] + 1 < len(realms["step3"]) else None
        if next_realm:
            xp_info = f"**Essence XP**: {player['essence_xp']}/{next_realm['xp_required']}"
    
    # Format inventory
    inventory = player["inventory"][:10]
    inventory_info = "\n".join(f"• {item}" for item in inventory) if inventory else "Kosong"
    if len(player["inventory"]) > 10:
        inventory_info += f"\n...dan {len(player['inventory']) - 10} item lainnya"
    
    # Create embed
    embed = discord.Embed(
        title=f"📊 Profil {ctx.author.display_name}",
        description=f"**Sekte**: {player['sect']}",
        color=CONFIG["colors"]["primary"]
    )
    
    embed.add_field(
        name="⚡ Realm Saat Ini",
        value=realm_info,
        inline=False
    )
    
    embed.add_field(
        name="💪 Power",
        value=f"{power:.2f}",
        inline=True
    )
    
    embed.add_field(
        name="💰 Gold",
        value=player["gold"],
        inline=True
    )
    
    if xp_info:
        embed.add_field(
            name="📈 Progres ke Realm Berikutnya",
            value=xp_info,
            inline=False
        )
    
    embed.add_field(
        name=f"🎒 Inventory ({len(player['inventory'])})",
        value=inventory_info,
        inline=False
    )
    
    embed.add_field(
        name="🌀 Reinkarnasi",
        value=player["reincarnations"],
        inline=True
    )
    
    if player["xp_bonus"] > 0:
        embed.add_field(
            name="✨ Bonus XP",
            value=f"+{player['xp_bonus']}",
            inline=True
        )
    
    if player["ancient_god"]:
        embed.add_field(
            name="⭐ Fragmen Warisan Ancient God",
            value=player["legacy_fragments"],
            inline=True
        )
    
    embed.set_thumbnail(url=ctx.author.display_avatar.url)
    await ctx.send(embed=embed)

@bot.command(
    name="inventory",
    help="Menampilkan inventory anda dengan detail",
    usage=""
)
async def inventory(ctx):
    player = get_player(ctx.author.id)
    if not player:
        embed = discord.Embed(
            title="❌ Belum Terdaftar",
            description="Silakan registrasi dulu dengan !register",
            color=CONFIG["colors"]["danger"]
        )
        await ctx.send(embed=embed)
        return
    
    weapons = load_data("weapons.json")
    
    if not player["inventory"]:
        embed = discord.Embed(
            title="🎒 Inventory Kosong",
            description="Anda belum memiliki item apapun",
            color=CONFIG["colors"]["warning"]
        )
        await ctx.send(embed=embed)
        return
    
    items_by_rarity = {
        "MYTHICAL": [],
        "ANCIENT": [],
        "STEP": [],
        "LEGEND": [],
        "EPIC": [],
        "RARE": [],
        "BASIC": []
    }
    
    for item_name in player["inventory"]:
        found = False
        for rarity in weapons:
            for weapon in weapons[rarity]:
                if weapon["name"] == item_name:
                    items_by_rarity[rarity].append(weapon)
                    found = True
                    break
            if found:
                break
    
    embed = discord.Embed(
        title=f"🎒 Inventory {ctx.author.display_name}",
        description=f"Total item: {len(player['inventory'])}",
        color=CONFIG["colors"]["primary"]
    )
    
    for rarity, items in items_by_rarity.items():
        if items:
            value = "\n".join(
                f"**{item['name']}** - {item['description']}\n"
                f"Power: {item['power']}x"
                for item in items
            )
            embed.add_field(
                name=f"{rarity} ({len(items)})",
                value=value,
                inline=False
            )
    
    await ctx.send(embed=embed)

# Owner commands
def is_owner():
    async def predicate(ctx):
        return ctx.author.id in CONFIG["owner_ids"]
    return commands.check(predicate)

@bot.command(
    name="addgold",
    help="[OWNER] Menambahkan gold ke player",
    usage="@user <amount>",
    hidden=True
)
@is_owner()
async def add_gold(ctx, member: discord.Member, amount: int):
    player = get_player(member.id)
    if not player:
        await ctx.send("Player not found.")
        return
    
    player["gold"] += amount
    update_player(member.id, player)
    
    embed = discord.Embed(
        title="💰 Gold Ditambahkan",
        description=f"Ditambahkan {amount} gold ke {member.display_name}",
        color=CONFIG["colors"]["success"]
    )
    embed.add_field(
        name="Gold Sekarang",
        value=player["gold"],
        inline=False
    )
    await ctx.send(embed=embed)

@bot.command(
    name="setxp",
    help="[OWNER] Set XP player",
    usage="@user <type> <amount>",
    hidden=True
)
@is_owner()
async def set_xp(ctx, member: discord.Member, xp_type: str, amount: int):
    player = get_player(member.id)
    if not player:
        await ctx.send("Player not found.")
        return
    
    xp_type = xp_type.lower()
    if xp_type == "spiritual":
        player["spiritual_xp"] = amount
    elif xp_type == "comprehension":
        player["comprehension_xp"] = amount
    elif xp_type == "essence":
        player["essence_xp"] = amount
    elif xp_type == "ancient":
        player["ancient_xp"] = amount
    else:
        await ctx.send("Invalid XP type. Use: spiritual, comprehension, essence, or ancient")
        return
    
    update_player(member.id, player)
    
    embed = discord.Embed(
        title="📈 XP Diupdate",
        description=f"Set {xp_type} XP ke {amount} untuk {member.display_name}",
        color=CONFIG["colors"]["success"]
    )
    await ctx.send(embed=embed)

@bot.command(
    name="setrealm",
    help="[OWNER] Set realm player",
    usage="@user <step> <realm>",
    hidden=True
)
@is_owner()
async def set_realm(ctx, member: discord.Member, step: int, realm: int):
    player = get_player(member.id)
    if not player:
        await ctx.send("Player not found.")
        return
    
    realms = load_data("realms.json")
    step_key = f"step{step}"
    
    if step_key not in realms or realm < 0 or realm >= len(realms[step_key]):
        await ctx.send("Invalid step or realm number.")
        return
    
    player["step"] = step
    player["realm"] = realm
    update_player(member.id, player)
    
    realm_data = realms[step_key][realm]
    
    embed = discord.Embed(
        title="⚡ Realm Diupdate",
        description=f"Set {member.display_name} ke {realm_data['english']} (Step {step})",
        color=CONFIG["colors"]["success"]
    )
    await ctx.send(embed=embed)

@bot.command(
    name="setancient",
    help="[OWNER] Set status Ancient God player",
    usage="@user <stars>",
    hidden=True
)
@is_owner()
async def set_ancient(ctx, member: discord.Member, stars: int):
    player = get_player(member.id)
    if not player:
        await ctx.send("Player not found.")
        return
    
    realms = load_data("realms.json")
    if stars < 1 or stars > 27:
        await ctx.send("Stars must be between 1 and 27 for Ancient Gods.")
        return
    
    player["ancient_god"] = True
    player["ancient_stars"] = stars
    player["step"] = 3
    update_player(member.id, player)
    
    embed = discord.Embed(
        title="⭐ Ancient God Diupdate",
        description=f"Set {member.display_name} sebagai {stars}-Star Ancient God",
        color=0x800080
    )
    await ctx.send(embed=embed)

@bot.command(
    name="resetplayer",
    help="[OWNER] Reset progress player",
    usage="@user",
    hidden=True
)
@is_owner()
async def reset_player(ctx, member: discord.Member):
    create_player(member.id)
    
    embed = discord.Embed(
        title="🔄 Player Direset",
        description=f"Progress {member.display_name} telah direset ke awal",
        color=CONFIG["colors"]["success"]
    )
    await ctx.send(embed=embed)

# Run bot
bot.run(CONFIG["bot_token"])