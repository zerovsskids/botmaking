import os
import random
import json
import threading
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext
from flask import Flask

async def cancel_action(update: Update, context: CallbackContext):
    await update.callback_query.answer("Action cancelled!")         

async def show_access_users(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    try:
        with open('user_access.json', 'r') as file:
            access_data = json.load(file)

        if not access_data:
            await query.message.edit_text("❌ No users with access found.", parse_mode="Markdown")
            return

        message = "🏷️ *Access Granted Users:*\n\n"
        count = 0

        for user_id in access_data.keys():
            try:
                user_obj = await context.bot.get_chat(int(user_id))
                first_name = user_obj.first_name or ""
                last_name = user_obj.last_name or ""
                full_name = (first_name + " " + last_name).strip()
                username = f"@{user_obj.username}" if user_obj.username else "NoUsername"

                message += (
                    f"🔰 *Name:* `{full_name}`\n"
                    f"🆔 *ID:* `{user_id}`\n"
                    f"💬 *Username:* `{username}`\n\n"
                )
                count += 1

            except Exception:
                message += (
                    f"🔰 *Name:* `Unknown`\n"
                    f"🆔 *ID:* `{user_id}`\n"
                    f"💬 *Username:* `Unknown`\n\n"
                )
                count += 1

        message += f"✅ *Total Users:* `{count}`"

        await query.message.edit_text(message, parse_mode="Markdown")

    except FileNotFoundError:
        await query.message.edit_text("❌ user_access.json not found.", parse_mode="Markdown")
from telegram import Update
from telegram.ext import CallbackContext

async def start_command(update: Update, context: CallbackContext):
    user = update.effective_user

    gif_url = "https://media4.giphy.com/media/7pRgHlyv887Rq2UGF5/giphy.gif?cid=6c09b952k4j27k6ik7lxc3ewpytv38ikqt5hacb8j30zdb4x&ep=v1_internal_gif_by_id&rid=giphy.gif&ct=g"

    # Send GIF
    await update.message.reply_animation(
        animation=gif_url,
        caption=(
            f"🎉 *Welcome {user.first_name}!* 🎉\n\n"
            "🚀 *Ready to use Kazii VIP Bot?*\n\n"
            "🔑 `/key <your_key>` — *Enter your access pass!*\n"
            "🎲 `/generate` — *Open the generator panel!*\n\n"
            "✨ / search — *Get ready unlimited txt files!* ✨\n\n"
            "⚡Created by @kazikamiii⚡"
        ),
        parse_mode="Markdown"
    )
async def show_proxy_options(update: Update, context: CallbackContext):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("100 Proxies", callback_data="proxy_select:100")],
        [InlineKeyboardButton("200 Proxies", callback_data="proxy_select:200")],
        [InlineKeyboardButton("300 Proxies", callback_data="proxy_select:300")],
    ]
    await query.message.edit_text(
        "🌐 *Welcome to Proxy Generator!*\n\n"
        "Choose how many proxies you want to generate:",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )         
    
async def confirm_proxy_choice(update: Update, context: CallbackContext, count: int):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("✅ Yes", callback_data=f"confirm_proxy:{count}"),
         InlineKeyboardButton("❌ No", callback_data="cancel_proxy")]
    ]
    await query.message.edit_text(
        f"⚙️ You chose *{count} proxies*.\n\nProceed?",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
        
async def cancel_proxy_generation(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.message.edit_text("❌ Cancelled proxy generation.", parse_mode="Markdown")        
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

import random


import asyncio
import os
import random
from telegram import InputFile

async def generate_proxies(update: Update, context: CallbackContext, count: int):
    query = update.callback_query

    if not os.path.exists("Proxies.txt"):
        await query.message.edit_text("❌ Proxy database `Proxies.txt` not found.", parse_mode="Markdown")
        return

    with open("Proxies.txt", "r", encoding="utf-8") as f:
        proxies_list = [line.strip() for line in f if line.strip()]

    if not proxies_list:
        await query.message.edit_text("❌ Proxy database is empty.", parse_mode="Markdown")
        return

    selected_proxies = random.sample(proxies_list, min(count, len(proxies_list)))

    filename = f"proxy_{count}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("✅ File Generated via Kazii VIP Bot\n")
        f.write("📄 File: proxy\n")
        f.write("🔥 Type: Mix\n")
        f.write(f"📈 Total: {len(selected_proxies)}\n")
        f.write("----------------------------------\n\n")
        f.write("\n".join(selected_proxies))

    # Step 1: Fast Progress animation
    await query.message.edit_text("⏳ *Generating your proxies...*", parse_mode="Markdown")
    await asyncio.sleep(0.7)
    await query.message.edit_text("⚙️ *Working...*", parse_mode="Markdown")
    await asyncio.sleep(0.7)
    await query.message.edit_text("✅ *Finishing up...*", parse_mode="Markdown")
    await asyncio.sleep(0.5)

    # Step 2: Send file
    with open(filename, "rb") as f:
        await query.message.reply_document(
            document=InputFile(f),
            caption=f"✅ *File Generated via Kazii VIP Bot*\n📄 *File:* proxy\n🔥 *Type:* Mix\n📈 *Lines:* {len(selected_proxies)}",
            parse_mode="Markdown"
        )

    # Step 3: Fast fade effect then delete
    try:
        for fade_text in ["", ".", "..", "...", ""]:
            await query.message.edit_text(f"*{fade_text}*", parse_mode="Markdown")
            await asyncio.sleep(0.2)  # mas mabilis fade
        await query.message.delete()
    except:
        pass  # kung na-delete na

    
        
            
     #other
     
import os
import re
import time
from telegram import Update, InputFile
from telegram.ext import CallbackContext

async def handle_file(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id

    document = update.message.document
    if not document or document.mime_type != "text/plain":
        await update.message.reply_text("❌ Please send a .txt file only.", parse_mode="Markdown")
        return

    # Check if there is an active operation
    active_url_remover = context.user_data.get("url_remover_active")
    active_password_filter = context.user_data.get("ml_password_filter_active")
    operation_expire_at = context.user_data.get("operation_expire_at")

    current_time = time.time()

    # If no active operation or expired, reject
    if (not active_url_remover and not active_password_filter) or (operation_expire_at and current_time > operation_expire_at):
        # Clear modes if expired
        context.user_data.pop("url_remover_active", None)
        context.user_data.pop("ml_password_filter_active", None)
        context.user_data.pop("operation_expire_at", None)

        await update.message.reply_text(
            "❌ No active operation or operation expired.\nPlease click the correct button first.",
            parse_mode="Markdown"
        )
        return

    await update.message.chat.send_action(action="upload_document")

    file_path = await document.get_file()
    downloaded = await file_path.download_to_drive()

    # ========== URL REMOVER ==========
    if active_url_remover:
        cleaned_lines = []
        with open(downloaded, "r", encoding="utf-8") as infile:
            lines = infile.readlines()

        for line in lines:
            match = re.search(r'([^:/\s]+):([^:/\s]+)\)?$', line.strip())
            if match:
                cleaned_lines.append(f"{match.group(1)}:{match.group(2)}")

        cleaned_filename = "Kenshiruu_Remove_Url.txt"
        with open(cleaned_filename, "w", encoding="utf-8") as outfile:
            outfile.write("\n".join(cleaned_lines))

        with open(cleaned_filename, "rb") as f:
            await update.message.reply_document(
                document=InputFile(f),
                caption="✅ *File cleaned successfully!*\n\n_Powered by Kazii VIP Bot_",
                parse_mode="Markdown"
            )

        os.remove(cleaned_filename)

    # ========== ML PASSWORD FILTER ==========
    elif active_password_filter:
        invalid_chars = set('@#$_&-+()/?!;:\'"*~`|¥•√π÷×§∆£\\¢}€]¥[®✓©™%^°=')

        def is_valid_password(pw):
            has_capital = any(c.isupper() for c in pw)
            has_invalid = any(c in invalid_chars for c in pw)
            return has_capital and not has_invalid

        valid_lines = []
        with open(downloaded, "r", encoding="utf-8") as infile:
            for line in infile:
                line = line.strip()
                if ':' in line:
                    user, pw = line.split(':', 1)
                    if is_valid_password(pw):
                        valid_lines.append(f"{user}:{pw}")

        filtered_filename = "Kenshiruu_Filter_Pw.txt"
        with open(filtered_filename, "w", encoding="utf-8") as outfile:
            outfile.write("\n".join(valid_lines))

        with open(filtered_filename, "rb") as f:
            await update.message.reply_document(
                document=InputFile(f),
                caption="✅ Passwords filtered successfully!\n\nGenerated via *Kazii VIP Bot*",
                parse_mode="Markdown"
            )

        os.remove(filtered_filename)

    # After processing, always clear active modes
    context.user_data.pop("url_remover_active", None)
    context.user_data.pop("ml_password_filter_active", None)
    context.user_data.pop("operation_expire_at", None)

    os.remove(downloaded)
VIP_DATABASE_FILES = {
    "bilibili": "vbilibili.txt",
    "codashop": "vcodashop.txt",
    "discord": "vdiscord.txt",
    "vivamax": "viv.txt",
    "garena": "vgarena.txt",
    "instagram": "vinstagram.txt",
    "ml": "vml.txt",
    "mtacc": "vmtacc.txt",
    "facebook": "vfb.txt",
    "amazon": "vamazon.txt",
    "github": "vgithub.txt",
    "gaslite": "vgaslite.txt",
    "100054": "vip_100054.txt",
    "100055": "vip_100055.txt",
    "100072": "vip_100072.txt",
    "100080": "vip_100080.txt",
    "100082": "vip_100082.txt"
}

# === VIP Button Handler ===
async def handle_vip_database(update, context):
    query = update.callback_query
    await query.message.delete()

    def format_name(name, width=12):
        return name.ljust(width)

    buttons = [
        InlineKeyboardButton(f"📁 {format_name(name)}", callback_data=f"vip_select:{name}")
        for name in VIP_DATABASE_FILES.keys()
    ]

    # Group buttons 4 per row
    grouped = [buttons[i:i + 4] for i in range(0, len(buttons), 4)]

    await query.message.chat.send_message(
        "🌟 *VIP DATABASE MENU*\n\nSelect a file to generate from:",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(grouped)
    )


# === Handle Specific VIP Selection ===
async def handle_vip_selection(update, context):
    query = update.callback_query
    await query.message.delete()
    
    _, name = query.data.split(":")
    context.user_data["vip_source"] = name

    buttons = [
        InlineKeyboardButton("🔹 25", callback_data=f"vip_lines:{name}:25"),
        InlineKeyboardButton("🔹 50", callback_data=f"vip_lines:{name}:50"),
        InlineKeyboardButton("🔹 100", callback_data=f"vip_lines:{name}:100"),
    ]

    await query.message.chat.send_message(
        f"📁 *{name}* selected!\n\nHow many lines do you want to generate?",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([buttons])
    )


# === Confirmation Before Generation ===
async def handle_vip_line_selection(update, context):
    query = update.callback_query
    await query.message.delete()

    _, name, lines = query.data.split(":")
    context.user_data["vip_lines"] = int(lines)
    context.user_data["vip_source"] = name

    buttons = [
        InlineKeyboardButton("✅ Yes", callback_data="vip_confirm"),
        InlineKeyboardButton("❌ Cancel", callback_data="cancel_generation")
    ]

    await query.message.chat.send_message(
        f"🧾 You chose to generate *{lines} lines* from *{name}*.\n\nProceed?",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([buttons])
    )


import random
import datetime
import os
import asyncio
from telegram import InputFile

async def confirm_vip_generate(update, context):
    query = update.callback_query
    name = context.user_data.get("vip_source")
    lines = context.user_data.get("vip_lines")
    file_path = VIP_DATABASE_FILES.get(name)
    used_path = f"used_{file_path}"

    if not file_path or not os.path.exists(file_path):
        await query.message.edit_text("⚠️ *File not found.*", parse_mode="Markdown")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        all_lines = set(line.strip() for line in f if line.strip())

    used_lines = set()
    if os.path.exists(used_path):
        with open(used_path, "r", encoding="utf-8") as f:
            used_lines = set(line.strip() for line in f if line.strip())

    available = list(all_lines - used_lines)
    total_lines = len(all_lines)
    used_count = len(used_lines)
    remaining = len(available)

    if remaining == 0:
        await query.message.edit_text("⚠️ *All lines used.*", parse_mode="Markdown")
        return

    selected = random.sample(available, min(lines, remaining))
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_id = f"#VGB-{random.randint(1000, 9999)}"

    with open(used_path, "a", encoding="utf-8") as f:
        for line in selected:
            f.write(line + "\n")

    out_file = f"{name.replace(' ', '_')}_VIP_{lines}.txt"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
        f.write("      ★ VIP DROP — Kazii VIP Bot ★\n")
        f.write("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
        f.write(f"📁 Source : {name}\n")
        f.write(f"📦 Total  : {len(selected)} lines\n")
        f.write(f"🕒 Date   : {timestamp}\n")
        f.write(f"🆔 File ID: {file_id}\n")
        f.write("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n")

        for idx, line in enumerate(selected, 1):
            f.write(f"★ DROP {idx:02}\n{line}\n")
            f.write("──────────────────────────────\n")

        f.write("\nGenerated by Kazii VIP Bot\n")

    await query.message.edit_text("✨ *Preparing your VIP DROP...*", parse_mode="Markdown")
    await asyncio.sleep(1.2)

    with open(out_file, "rb") as f:
        await query.message.reply_document(
            document=InputFile(f),
            caption=(
                f"✅ *VIP DROP COMPLETE!*\n"
                f"📁 Source: *{name}*\n"
                f"📦 Lines: *{len(selected)}*\n"
                f"🕒 Date: *{timestamp}*\n"
                f"🆔 File ID: `{file_id}`\n\n"
                f"🔐 _Generated by Kazii VIP Bot_"
            ),
            parse_mode="Markdown"
        )

    await query.message.reply_text(
        f"📊 *VIP FILE STATS*\n"
        f"• Source: *{name}*\n"
        f"• Pulled: *{lines}* lines\n"
        f"• Used: *{used_count + len(selected)}* / *{total_lines}*\n"
        f"• Remaining: *{remaining - len(selected)}*\n"
        f"• Timestamp: *{timestamp}*",
        parse_mode="Markdown"
    )
# === V2L / Bypass Tutorial Menu ===
async def show_v2l_menu(update, context):
    query = update.callback_query
    await query.message.delete()

    keyboard = [
        [InlineKeyboardButton("🧩 Bypass Tutorial", callback_data="bypass_tutorial")],
        [InlineKeyboardButton("⚙️ V2L Tutorial", callback_data="v2l_info")],
        [InlineKeyboardButton("⬅️ Back to Menu", callback_data="main_menu")]
    ]

    await query.message.reply_text(
        "📘 *Choose a tutorial below:*\nHelpful guides to bypass and use V2L systems!",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    
# === Show Bypass Tutorial ===
# === Function: Show Bypass Tutorial ===
async def show_bypass_tutorial(update, context):
    query = update.callback_query
    await query.answer()
    await query.message.edit_text(
        "**V2L BYPASS TUTS**\n\n"
        "**What to download:**\n"
        "1. DL & Install *Mobile Legends: Bang Bang FT* — search in Chrome: `apkcombo mlbb ft`\n"
        "2. DL any virtual/dual app (e.g., Amy Virtual, Parallel Space)\n"
        "3. DL Express VPN (use 1-week trial) or modded version from Chrome\n\n"
        "**What to do:**\n"
        "1. Connect VPN to *Indonesia*\n"
        "2. Open Virtual App, clone MLBB FT\n"
        "3. Switch your account to a V2L account\n\n"
        "📽️ Eto Tutorial  [Watch here](https://t.me/MLACCOUN/10)",
        parse_mode="Markdown",
        disable_web_page_preview=True
    )

# === Function: Show V2L Tutorial ===
async def show_v2l_tutorial(update, context):
    query = update.callback_query
    await query.answer()
    await query.message.edit_text(
        "**V2L TUTORIAL**\n\n"
        "1. I-download mo ang app dito: [Moba 5v5](https://moba-legends-5v5.en.uptodown.com/android/download)\n"
        "2. Login ang account na i-V2L\n"
        "3. I-enable ang *New Devices Verification* sa settings\n"
        "4. Tapos! Pwede na gamitin.",
        parse_mode="Markdown",
        disable_web_page_preview=True
    )
import os
import random
import asyncio
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, InputFile
from telegram.ext import CallbackContext
import os
import random
import asyncio
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext


async def fetch_lines(update: Update, context: CallbackContext):
    query = update.callback_query
    chat_id = query.message.chat_id
    num_lines = int(query.data.replace("fetch_", ""))

    # Step 1: Delete the previous options message
    try:
        await query.message.delete()
    except Exception as e:
        print(f"Error deleting message: {e}")

    # Step 2: Show "Generating file..." message
    loading_msg = await query.message.reply_text("⚡ Generating file...")

    # Step 3: Get random lines (Optimized)
    random_lines = get_random_lines("Ovi.txt", num_lines)
    
    # Step 4: Create & save the file
    filename = f"Ovi_{num_lines}.txt"
    with open(filename, "w", encoding="utf-8") as file:
        file.writelines(random_lines)

    # Step 5: Delete "Generating file..." message
    try:
        await loading_msg.delete()
    except Exception as e:
        print(f"Error deleting loading message: {e}")

    # Step 6: Send the file
    sent_message = await query.message.reply_document(
        document=open(filename, "rb"), 
        filename=filename, 
        caption=f"📜 *Here is your {num_lines} lines file:*", 
        parse_mode="Markdown"
    )

    # Cleanup
    os.remove(filename)
    await query.answer()

async def show_options(update: Update, context: CallbackContext):
    query = update.callback_query
    chat_id = query.message.chat_id

    # Step 1: Delete the previous message (Ovi File button)
    try:
        await query.message.delete()
    except Exception as e:
        print(f"Error deleting message: {e}")

    # Step 2: Show options
    keyboard = [
        [InlineKeyboardButton("📄 5K Lines", callback_data="fetch_5000"), InlineKeyboardButton("📄 10K Lines", callback_data="fetch_10000")],
        [InlineKeyboardButton("📜 15K Lines", callback_data="fetch_15000"), InlineKeyboardButton("📜 20K Lines", callback_data="fetch_20000")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    options_msg = await query.message.reply_text("📊 *Choose the number of lines to generate:*", parse_mode="Markdown", reply_markup=reply_markup)
    context.user_data["last_message_id"] = options_msg.message_id
    await query.answer()

def get_random_lines(filename, num_lines):
    """Fetch random lines from a large file efficiently."""
    with open(filename, "r", encoding="utf-8") as file:
        lines = file.readlines()
    return random.sample(lines, min(num_lines, len(lines)))  # Random selection
#ACCEST LIST
ADMIN_IDS = {7472543084, 7472543084}  # Palitan ng totoong admin user IDs

async def show_access_list(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    if query.from_user.id not in ADMIN_IDS:
        await query.message.edit_text("🚫 *Admin access only!*")
        return

    if not USER_ACCESS:
        await query.message.edit_text("ℹ️ *No users have access.*")
        return

    keyboard = []
    text = "🔑 *Users with Access:*\n\n"

    for user_id, expiry in USER_ACCESS.items():
        user_id = int(user_id)
        try:
            user = await context.bot.get_chat(user_id)
            username = f"@{user.username}" if user.username else user.full_name
        except:
            username = "Unknown User"

        expiry_text = "Lifetime" if expiry is None else datetime.datetime.fromtimestamp(expiry).strftime('%Y-%m-%d %H:%M:%S')
        text += f"🆔 *{username}* (`{user_id}`) - {expiry_text}\n"
        keyboard.append([InlineKeyboardButton(f"❌ Revoke {username}", callback_data=f"revoke_{user_id}")])

    keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="generated_menu")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.edit_text(text, parse_mode="Markdown", reply_markup=reply_markup)

async def revoke_access(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    if query.from_user.id not in ADMIN_IDS:
        await query.message.edit_text("🚫 *Admin access only!*")
        return

    user_id = query.data.split("_")[1]
    try:
        user = await context.bot.get_chat(int(user_id))
        username = f"@{user.username}" if user.username else user.full_name
    except:
        username = f"User {user_id}"

    if user_id in USER_ACCESS:
        del USER_ACCESS[user_id]
        save_data()
        await query.message.edit_text(f"✅ *Access revoked for {username} (`{user_id}`)*")
    else:
        await query.message.edit_text(f"❌ *User {user_id} does not have access.*")

import random

def get_random_lines(filename, num_lines):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            lines = file.readlines()
        
        if len(lines) < num_lines:
            return lines  # Kung kulang ang laman ng file, ibabalik lahat
        return random.sample(lines, num_lines)  # Random na pipili ng eksaktong dami ng lines
    except FileNotFoundError:
        return ["⚠️ File not found!"]
    except Exception as e:
        return [f"❌ Error: {str(e)}"]       
        

        # === CONFIGURATION ===
TOKEN = "8417427932:AAEQHCxOoCOXafpgZqygluRY8mtzcLqYapE"  # Palitan ng iyong bot token
ADMIN_ID = 6086248885 # Palitan ng iyong Telegram ID
DATABASE_FILES ={
  "100082": "100082.txt",
  "8BALL": "8BALL.txt",
  "Amazon": "Amazon.txt",
  "MTACC": "MTACC.txt",
  "apex": "apex.txt",
  "authgop": "authgop.txt",
  "brawlstar": "brawlstar.txt",
  "clashofclan": "clashofclan.txt",
  "discord": "discord.txt",
  "roblox": "vroblox.txt",
  "facebook": "facebook.txt",
  "fifa": "fifa.txt",
  "fortnite": "fortnite.txt",
  "freefire": "freefire.txt",
  "garena": "garena.txt",
  "genshin": "genshin.txt",  
  "gmail": "gmail.txt",
  "hotmail": "hotmail.txt",
  "instagram": "instagram.txt",
  "minecraft": "minecraft.txt",
  "mobilelegends": "mobilelegends.txt",
  "netflix": "netflix.txt",
  "paypal": "paypal.txt",
  "pubg": "pubg.txt",
  "riotgames": "riotgames.txt",
  "spotify": "spotify.txt",
  "steam": "steam.txt",
  "tiktok": "tiktok.txt",
  "twitch": "twitch.txt",
  "twitter": "twitter.txt",
  "valorant": "valorant.txt",
  "yahoo": "yahoo.txt",
  "youtube": "youtube.txt"
} 
import os
import json
import random
import datetime
import re
from telegram import Update, InputFile
from telegram.ext import CallbackContext

ACCESS_KEYS_FILE = "access_keys.json"
USER_ACCESS_FILE = "user_access.json"

ACCESS_KEYS = {}  # {key: {"expires_at": timestamp}}
USER_ACCESS = {}  # {user_id: expiry_time or None}

# === LOAD DATA FROM FILES ON BOT STARTUP ===
def load_data():
    global ACCESS_KEYS, USER_ACCESS
    if os.path.exists(ACCESS_KEYS_FILE):
        with open(ACCESS_KEYS_FILE, "r", encoding="utf-8") as f:
            ACCESS_KEYS = json.load(f)
    
    if os.path.exists(USER_ACCESS_FILE):
        with open(USER_ACCESS_FILE, "r", encoding="utf-8") as f:
            USER_ACCESS = json.load(f)

    # Convert timestamps back to integers (JSON stores as strings)
    for key in ACCESS_KEYS:
        if ACCESS_KEYS[key]["expires_at"]:
            ACCESS_KEYS[key]["expires_at"] = float(ACCESS_KEYS[key]["expires_at"])

    for user in USER_ACCESS:
        if USER_ACCESS[user]:
            USER_ACCESS[user] = float(USER_ACCESS[user])

# === SAVE DATA TO FILES ===
def save_data():
    with open(ACCESS_KEYS_FILE, "w", encoding="utf-8") as f:
        json.dump(ACCESS_KEYS, f, indent=4)

    with open(USER_ACCESS_FILE, "w", encoding="utf-8") as f:
        json.dump(USER_ACCESS, f, indent=4)

# === REMOVE EXPIRED KEYS AUTOMATICALLY ===
def cleanup_expired_keys():
    current_time = datetime.datetime.now().timestamp()

    # Remove expired keys
    expired_keys = [key for key, data in ACCESS_KEYS.items() if data["expires_at"] and data["expires_at"] < current_time]
    for key in expired_keys:
        del ACCESS_KEYS[key]

    # Remove expired user access
    expired_users = [user for user, expiry in USER_ACCESS.items() if expiry and expiry < current_time]
    for user in expired_users:
        del USER_ACCESS[user]

    save_data()  # Save changes

# === GENERATE KEY (ADMIN ONLY) ===
import secrets
import string
import datetime
import re

async def generate_key(update: Update, context: CallbackContext):
    if update.message.from_user.id != ADMIN_ID:
        await update.message.reply_text("⛔ *Access Denied!* Only the Admin can generate keys.", parse_mode="MarkdownV2")
        return

    if len(context.args) == 0:
        await update.message.reply_text(
            "⚠️ *Usage:* `/genkey <time>`\n\n"
            "`10s`, `5m`, `2h`, `1d`, `lifetime`",
            parse_mode="MarkdownV2"
        )
        return

    duration_text = context.args[0]

    if duration_text.lower() == "lifetime":
        expires_at = None
        expiry_text = "∞ Lifetime Access"
    else:
        match = re.match(r"(\d+)([smhd])", duration_text)
        if not match:
            await update.message.reply_text(
                "❌ *Invalid Format!*\nTry: `/genkey 10s`, `/genkey 5m`, etc.",
                parse_mode="MarkdownV2"
            )
            return

        value, unit = int(match[1]), match[2]
        units = {"s": "Seconds", "m": "Minutes", "h": "Hours", "d": "Days"}
        multiplier = {"s": 1, "m": 60, "h": 3600, "d": 86400}
        expires_at = (datetime.datetime.now() + datetime.timedelta(seconds=value * multiplier[unit])).timestamp()
        expiry_text = f"{value} {units[unit]}"

    # Generate secure key
    part1 = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(4))
    part2 = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(4))
    key = f"KEN-{part1}-{part2}"

    ACCESS_KEYS[key] = {"expires_at": expires_at}
    save_data()

    # Techy animation + key message combined
    await update.message.reply_animation(
        animation="https://media4.giphy.com/media/qIE7nKYuG4jZK/giphy.gif?cid=6c09b9527wdkoh2ibjyfmy9yf1mfgnl0679ojaobdgtidi8a&ep=v1_internal_gif_by_id&rid=giphy.gif&ct=g",  # Techy lock animation
        caption=(
            "*╔════════════════════╗*\n"
            "*   🔐 ACCESS KEY GENERATED 🔐*\n"
            "*╚════════════════════╝*\n\n"
            "🚨 *One-Time Use Only!*\n\n"
            "*KEY:* ` {}`\n"
            "*VALIDITY:* `{}`\n\n"
            "🧠 Use this to access restricted areas.\n"
            "⚠️ Do not share this key.\n\n"
            "*Kazii VIP Bot — Code. Access. Conquer.*"
        ).format(key, expiry_text),
        parse_mode="Markdown"
    )

# === ENTER KEY ===
# === ENTER KEY ===
async def enter_key(update: Update, context: CallbackContext):
    if len(context.args) == 0:
        await update.message.reply_text("⚠️ *Usage: `/key <access_key>`*", parse_mode="Markdown")
        return

    key = context.args[0]
    user = update.message.from_user
    user_id = str(user.id)  # Store user_id as a string for JSON compatibility
    username = f"@{user.username}" if user.username else f"User {user.id}"

    if key in ACCESS_KEYS:
        key_data = ACCESS_KEYS[key]
        
        if key_data["expires_at"] and key_data["expires_at"] < datetime.datetime.now().timestamp():
            del ACCESS_KEYS[key]
            save_data()
            await update.message.reply_text("❌ *Key expired!*")
            return

        USER_ACCESS[user_id] = key_data["expires_at"]
        del ACCESS_KEYS[key]
        save_data()

        expiry_text = "Lifetime" if USER_ACCESS[user_id] is None else f"until {datetime.datetime.fromtimestamp(USER_ACCESS[user_id]).strftime('%Y-%m-%d %H:%M:%S')}"
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        await update.message.reply_text(f"✅ *Access granted! Expires {expiry_text}.*\nUse `/generate` to proceed.", parse_mode="Markdown")

        # === Notify the Admin ===
        admin_message = (
            f"🚨 *New Key Redemption Alert!*\n"
            f"👤 *User ID:* `{user_id}`\n"
            f"📛 *Username:* {username}\n"
            f"🔑 *Key Type:* {expiry_text}\n"
            f"📅 *Date & Time:* `{timestamp}`\n"
            f"ℹ️ *More Info:* [{user.full_name}](tg://user?id={user.id})"
        )

        try:
            await context.bot.send_message(chat_id=ADMIN_ID, text=admin_message, parse_mode="Markdown")
        except telegram.error.BadRequest:
            print(f"Admin notification failed for user {user_id}.")

        # === Notify All Users with Access ===
        public_message = f"🎉 *New user has redeemed access!* Let's welcome {username}! 🚀"

        expired_users = []
        for uid in USER_ACCESS.keys():
            try:
                await context.bot.send_message(chat_id=uid, text=public_message, parse_mode="Markdown")
            except telegram.error.BadRequest:
                expired_users.append(uid)

        # Clean up users who can no longer receive messages
        for uid in expired_users:
            del USER_ACCESS[uid]

        save_data()

    else:
        await update.message.reply_text("❌ *Invalid or used key!*")
# === CHECK ACCESS ===
def has_access(user_id):
    user_id = str(user_id)  # Convert to string for JSON compatibility
    cleanup_expired_keys()  # Remove expired access before checking

    if user_id not in USER_ACCESS:
        return False
    if USER_ACCESS[user_id] is None:
        return True
    return USER_ACCESS[user_id] > datetime.datetime.now().timestamp()

# === AUTO-LOAD KEYS ON STARTUP ===
load_data()
cleanup_expired_keys()

async def view_logs(update: Update, context: CallbackContext):
    user_id = update.callback_query.from_user.id
    await update.callback_query.answer()

    try:
        # Read the log file
        with open("generation_history.txt", "r", encoding="utf-8") as log_file:
            logs = log_file.readlines()

        if not logs:
            await update.callback_query.message.reply_text("❌ No history available.")
            return

        # Prepare logs for sending in chunks
        history_text = "📝 *Generation History:*\n\n"
        for log in logs:
            history_text += f"{log}\n"

        # If the history is too long, split it into smaller messages
        if len(history_text) > 4096:
            # Split into chunks of 4096 characters
            chunks = [history_text[i:i+4096] for i in range(0, len(history_text), 4096)]
            for chunk in chunks:
                await update.callback_query.message.reply_text(chunk, parse_mode="Markdown")
        else:
            await update.callback_query.message.reply_text(history_text, parse_mode="Markdown")

    except Exception as e:
        await update.callback_query.message.reply_text(f"❌ Error: {str(e)}")
        

# === SHOW GENERATE MENU ===
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

async def generate_menu(update: Update, context: CallbackContext):
    user = update.effective_user

    if not has_access(user.id):
        await update.message.reply_text("🚫 No access! Use `/key <access_key>` first.", parse_mode="Markdown")
        return

    # GIF + caption in one message
    gif_url = "https://media3.giphy.com/media/fB2IRTXd07IkcStfwU/giphy.gif?cid=6c09b952x7saekkjld3sozqsl4uctls3kksu7g5pae91omp7&ep=v1_internal_gif_by_id&rid=giphy.gif&ct=g"    
    await update.message.reply_animation(
        animation=gif_url,
        caption=(
            f"🎉 Welcome {user.mention_markdown()} to *Kazii VIP Bot!*\n\n"
            "I'm here to help you generate accounts and access tools efficiently.\n"
            "Choose a menu option below to get started:"
        ),
        parse_mode="Markdown"
    )

    # Menu buttons with Announcement
    keyboard = [
    [InlineKeyboardButton("📂 Database", callback_data="database_menu"),
     InlineKeyboardButton("🎲 Generate Account", callback_data="generate_account")],

    [InlineKeyboardButton("🚀 Ovi Gen.", callback_data="ovi_warning"),
     InlineKeyboardButton("🌀 EH Combo Gen", callback_data="combo_menu")],

    [InlineKeyboardButton("📜 View Logs", callback_data="view_logs"),
     InlineKeyboardButton("📊 Total Gen. Account", callback_data="total_generated"),
     InlineKeyboardButton("👤 My Stats", callback_data="my_stats")],

    [InlineKeyboardButton("🔑 Access List", callback_data="access_list"),
     InlineKeyboardButton("❓ Help", callback_data="help_menu"),
     InlineKeyboardButton("👥 Join Ken Community", callback_data="show_join_links")],

    [InlineKeyboardButton("🛠️ KGen Tools", callback_data="vgen_tools"),
     InlineKeyboardButton("🧪 Roblox Checker", callback_data="roblox_checker")],

    [InlineKeyboardButton("💎 VIP DATABASE", callback_data="vip_database")],

    [InlineKeyboardButton("📞 Contact Support", callback_data="contact_support"),
     InlineKeyboardButton("📢 Announcement", callback_data="make_announcement")],

    [InlineKeyboardButton("🟢 Bot Uptime", callback_data="bot_uptime")],

    [InlineKeyboardButton("🗑️ URL Remover", callback_data="url_remover"),
     InlineKeyboardButton("✏️ Your Name", callback_data="your_name"),
     InlineKeyboardButton("🔐 ML PwFilter", callback_data="ml_password_filter")],

    [InlineKeyboardButton("🌐 Proxy Generator", callback_data="proxy_generator"),
     InlineKeyboardButton("⚡ V2L/Bypass Tutorial", callback_data="v2l_tutorial")],

    [InlineKeyboardButton("🌍 IP Tracker", callback_data="ip_tracker"),
     InlineKeyboardButton("🏆 MLBB Validator", callback_data="mlbb_validator")],

    [InlineKeyboardButton("🔎 Search Logs", callback_data="search_logs")],

    [InlineKeyboardButton("🏅 MLBB Lvl Separator", callback_data="mlbb_separator"),
     InlineKeyboardButton("🔒 Encrypt File", callback_data="encrypt_file")]
]
    await update.message.reply_text(
        "Please choose an option:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
import base64
import os
import io
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, InputFile
from telegram.ext import CallbackQueryHandler, MessageHandler, ConversationHandler, filters, ContextTypes

ENCRYPT_WAIT_FILE = range(1)

async def encrypt_file_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("🔒 Please send the file you want to encrypt (Max 5MB).")
    return ENCRYPT_WAIT_FILE

async def encrypt_receive_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = update.message.document
    if not file:
        await update.message.reply_text("❌ Please send a valid file.")
        return ENCRYPT_WAIT_FILE
    if file.file_size > 5 * 1024 * 1024:
        await update.message.reply_text("❌ File too large. Max 5MB only.")
        return ENCRYPT_WAIT_FILE

    file_bytes = io.BytesIO()
    telegram_file = await file.get_file()
    await telegram_file.download_to_memory(out=file_bytes)
    file_bytes.seek(0)

    content = file_bytes.read().decode(errors="ignore")
    encoded = base64.b64encode(content.encode()).decode()
    encrypted = f"\nimport base64\nexec(base64.b64decode('{encoded}'))"

    encrypted_bytes = io.BytesIO(encrypted.encode())
    encrypted_bytes.name = "encrypted_file.py"

    await update.message.reply_document(
        document=InputFile(encrypted_bytes),
        caption="🔒 Your file has been encrypted!"
    )

    return ConversationHandler.END

encrypt_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(encrypt_file_start, pattern="^encrypt_file$")],
    states={
        ENCRYPT_WAIT_FILE: [MessageHandler(filters.Document.ALL, encrypt_receive_file)],
    },
    fallbacks=[]
)    
import os
import re
import zipfile
import io
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, InputFile
from telegram.ext import CallbackQueryHandler, MessageHandler, ConversationHandler, filters, ContextTypes

MLBB_START, WAIT_FOR_FILE, SEPARATE_FILE = range(3)


pattern = re.compile(r"(?:Level:\s*|level\s*=\s*)(\d+)", re.IGNORECASE)

level_ranges = {
    "Below 30": (0, 29),
    "31-50": (30, 50),
    "51-89": (51, 89),
    "90-99": (90, 99),
    "100 Above": (100, float("inf")),
}


async def mlbb_separator_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("📂 Please send me a .txt file (Max 5MB) to separate it by MLBB Level.")
    return WAIT_FOR_FILE


async def mlbb_receive_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = update.message.document
    if not file or not file.file_name.endswith(".txt"):
        await update.message.reply_text("❌ Please send a valid .txt file.")
        return WAIT_FOR_FILE

    if file.file_size > 5 * 1024 * 1024:
        await update.message.reply_text("❌ File too large. Max 5MB only.")
        return WAIT_FOR_FILE


    telegram_file = await file.get_file()
    file_bytes = io.BytesIO()
    await telegram_file.download_to_memory(file_bytes)
    file_bytes.seek(0)
    context.user_data["mlbb_file_bytes"] = file_bytes

    lines = file_bytes.getvalue().decode("utf-8", errors="ignore").splitlines()
    context.user_data["mlbb_lines"] = lines

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Yes", callback_data="mlbb_sep_yes"),
         InlineKeyboardButton("❌ No", callback_data="mlbb_sep_no")]
    ])
    await update.message.reply_text(
        f"✅ *File received!*\n\n📄 Size: {round(file.file_size/1024, 2)} KB\n📝 Lines: {len(lines)}\n\nProceed to separate by level?",
        parse_mode="Markdown",
        reply_markup=keyboard
    )
    return SEPARATE_FILE


async def mlbb_separate_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "mlbb_sep_no":
        await query.edit_message_text("❌ Operation cancelled.")
        return ConversationHandler.END

    await query.edit_message_text("⚙️ Separating file by MLBB Levels... Please wait...")

    lines = context.user_data["mlbb_lines"]
    level_counts = {key: 0 for key in level_ranges}
    file_buffers = {key: [] for key in level_ranges}


    for line in lines:
        match = pattern.search(line)
        if match:
            level = int(match.group(1))
            for range_name, (min_level, max_level) in level_ranges.items():
                if min_level <= level <= max_level:
                    file_buffers[range_name].append(line)
                    level_counts[range_name] += 1
                    break


    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', compression=zipfile.ZIP_DEFLATED) as zipf:
        for range_name, lines in file_buffers.items():
            if lines:
                content = '\n'.join(lines)
                filename = f"{range_name} [x{len(lines)}].txt"
                zipf.writestr(filename, content)
    zip_buffer.seek(0)


    await query.message.reply_document(
        document=InputFile(zip_buffer, filename="MLBB_Level_Separated.zip"),
        caption=(
            f"✅ *MLBB Level Separator Results:*\n\n" +
            "\n".join([f"✔️ {k}: {v} lines" for k, v in level_counts.items() if v > 0]) or "No valid entries found."
        ),
        parse_mode="Markdown"
    )


    context.user_data.pop("mlbb_lines", None)
    context.user_data.pop("mlbb_file_bytes", None)
    return ConversationHandler.END


mlbb_separator_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(mlbb_separator_start, pattern="^mlbb_separator$")],
    states={
        WAIT_FOR_FILE: [MessageHandler(filters.Document.ALL, mlbb_receive_file)],
        SEPARATE_FILE: [CallbackQueryHandler(mlbb_separate_file, pattern="^mlbb_sep_yes|mlbb_sep_no$")]
    },
    fallbacks=[]
)    
    
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackQueryHandler, MessageHandler, filters, ContextTypes


async def ip_tracker_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton("✅ Yes", callback_data="ip_yes"),
         InlineKeyboardButton("❌ No", callback_data="ip_no")]
    ]

    await query.edit_message_text(
        "⚠️ *Warning*: This is an IP Tracker feature. It can attempt to get the location of an IP address, but accuracy is not guaranteed and results may vary.\n\n"
        "Do you want to proceed using the IP Tracker?",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )


async def ip_yes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("🔄 Processing...\n\nPlease type the IP address you want to track (e.g., 8.8.8.8):")

    context.user_data['awaiting_ip'] = True


async def ip_no(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("❌ IP Tracker cancelled. Returning to main menu.")


import requests

async def ip_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('awaiting_ip'):
        ip = update.message.text
        await update.message.reply_text("⏳ IP received. Analyzing...")

        try:
            r = requests.get(f"http://ip-api.com/json/{ip}").json()
            if r['status'] == 'success':
                lat, lon = r.get('lat'), r.get('lon')
                google_maps_link = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"

                msg = (
                    f"🌍 IP Info:\n\n"
                    f"🌎 Country: {r.get('country', 'N/A')}\n"
                    f"🏙️ Region: {r.get('regionName', 'N/A')}\n"
                    f"🏠 City: {r.get('city', 'N/A')}\n"
                    f"🏢 Org: {r.get('org', 'N/A')}\n"
                    f"🌐 ISP: {r.get('isp', 'N/A')}\n"
                    f"📍 Lat/Long: {lat}, {lon}\n"
                    f"🔗 [Google Maps Location]({google_maps_link})"
                )
                await update.message.reply_text(msg, parse_mode="Markdown")
            else:
                await update.message.reply_text("❌ Unable to retrieve IP details.")
        except Exception as e:
            await update.message.reply_text(f"❌ Error occurred: {e}")

        context.user_data['awaiting_ip'] = False

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    CallbackQueryHandler, MessageHandler, filters,
    ConversationHandler, ContextTypes
)
import os
import re
import zipfile
import io
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, InputFile
from telegram.ext import CallbackQueryHandler, MessageHandler, ConversationHandler, filters, ContextTypes

MLBB_START, WAIT_FOR_FILE, CONFIRM_CHECK = range(3)


def is_valid_email_or_username(user):
    if '@' in user:
        return '.com' in user, "Email missing .com" if '.com' not in user else ""
    return bool(re.match(r'^[a-zA-Z0-9]{3,}$', user)), "Invalid username"

def is_valid_password(password):
    if len(password) < 8:
        return False, "Password too short"
    if not re.search(r'[A-Z]', password):
        return False, "Missing uppercase"
    if not re.search(r'[a-z]', password):
        return False, "Missing lowercase"
    if re.search(r'[^a-zA-Z0-9]', password):
        return False, "Invalid characters"
    return True, ""

def validate_line(line):
    parts = line.split(':', 1)
    if len(parts) < 2:
        return False
    user, pw = parts
    user_valid, _ = is_valid_email_or_username(user)
    pw_valid, _ = is_valid_password(pw)
    return user_valid and pw_valid


async def mlbb_validator_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Yes", callback_data="mlbb_yes"),
         InlineKeyboardButton("❌ No", callback_data="mlbb_no")]
    ])
    await query.edit_message_text(
        "⚠️ *Warning:* This ML Validator only checks format. There may be wrong passwords or unrecognized entries.\n\n"
        "Do you want to proceed?",
        parse_mode="Markdown",
        reply_markup=keyboard
    )
    return MLBB_START

async def mlbb_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "mlbb_yes":
        await query.edit_message_text("⏳ *Processing...*\n\nPlease send me your file (Max 2MB).", parse_mode="Markdown")
        return WAIT_FOR_FILE
    else:
        await query.edit_message_text("❌ Operation cancelled.")
        return ConversationHandler.END

async def mlbb_receive_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = update.message.document
    if not file:
        await update.message.reply_text("❌ Please send a valid file.")
        return WAIT_FOR_FILE
    if file.file_size > 2 * 1024 * 1024:
        await update.message.reply_text("❌ File too large. Max 2MB only.")
        return WAIT_FOR_FILE

    file_path = f"{file.file_id}.txt"
    telegram_file = await file.get_file()
    await telegram_file.download_to_drive(file_path)
    context.user_data["mlbb_file"] = file_path

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()
    context.user_data["mlbb_lines"] = lines

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Yes", callback_data="mlbb_check_yes"),
         InlineKeyboardButton("❌ No", callback_data="mlbb_check_no")]
    ])
    await update.message.reply_text(
        f"✅ *File received!*\n\n📄 Size: {round(file.file_size/1024, 2)} KB\n📝 Lines: {len(lines)}\n\nDo you want to proceed checking?",
        parse_mode="Markdown",
        reply_markup=keyboard
    )
    return CONFIRM_CHECK

async def mlbb_check_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "mlbb_check_no":
        await query.edit_message_text("❌ Check cancelled.")
        os.remove(context.user_data["mlbb_file"])
        return ConversationHandler.END

    await query.edit_message_text("🔍 Checking file, please wait...")

    lines = context.user_data["mlbb_lines"]
    valid_lines = []
    invalid_lines = []

    for line in lines:
        if validate_line(line.strip()):
            valid_lines.append(line)
        else:
            invalid_lines.append(line)

    
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zipf:
        zipf.writestr("valid.txt", '\n'.join(valid_lines))
        zipf.writestr("invalid.txt", '\n'.join(invalid_lines))
    zip_buffer.seek(0)


    await query.message.reply_document(
        document=InputFile(zip_buffer, filename="MLBB_Validator_Results.zip"),
        caption=(
            f"🏆 *MLBB Validator Results:*\n\n"
            f"✔️ Valid lines: {len(valid_lines)}\n"
            f"❌ Invalid lines: {len(invalid_lines)}\n"
            f"📊 Total lines: {len(lines)}\n\n"
            f"🔥 *Stay safe and avoid scams!*"
        ),
        parse_mode="Markdown"
    )

    
    os.remove(context.user_data["mlbb_file"])
    return ConversationHandler.END


mlbb_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(mlbb_validator_start, pattern="^mlbb_validator$")],
    states={
        MLBB_START: [CallbackQueryHandler(mlbb_response, pattern="^mlbb_yes|mlbb_no$")],
        WAIT_FOR_FILE: [MessageHandler(filters.Document.ALL, mlbb_receive_file)],
        CONFIRM_CHECK: [CallbackQueryHandler(mlbb_check_file, pattern="^mlbb_check_yes|mlbb_check_no$")]
    },
    fallbacks=[]
)

import os
import random
import asyncio

import os
import asyncio
from telegram import Update, InputFile
from telegram.ext import CallbackContext

import os
import asyncio
from telegram import Update
from telegram.ext import CallbackContext
from telegram import InputFile

import os
import asyncio
from telegram import Update
from telegram.ext import CallbackContext
from telegram import InputFile

import os
import asyncio
from telegram import InputFile

import os
import asyncio
from telegram import InputFile

import os
import asyncio
from telegram import Update, InputFile
from telegram.ext import CallbackContext

import os
import asyncio
from telegram import Update, InputFile
from telegram.ext import CallbackContext

import os
import asyncio
from telegram import Update, InputFile
from telegram.ext import CallbackContext
import os
import random
import asyncio

import random
import os
import asyncio
from telegram import Update, InputFile
from telegram.ext import CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


async def handle_logs_generation(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    try:
        _, size_mb = query.data.split(":")
        size_mb = int(size_mb)

        source_file = "Vlogs.txt"
        output_file = "Kenshiru_Logs_Vip.txt"

        if not os.path.exists(source_file):
            await query.message.edit_text("❌ Vlogs.txt not found.", parse_mode="Markdown")
            return

        # REMOVE the old buttons and show "Generating..." immediately
        await query.message.edit_text(
            "⚙️ *Generating your Logs... Please wait...*",
            parse_mode="Markdown",
            reply_markup=None
        )

        needed_bytes = size_mb * 1024 * 1024  # convert MB to bytes
        selected_lines = []

        # Read all lines into memory
        with open(source_file, "r", encoding="utf-8", errors="ignore") as file:
            lines = file.readlines()

        random.shuffle(lines)

        total_size = 0
        for line in lines:
            line_size = len(line.encode())
            if total_size + line_size > needed_bytes:
                break
            selected_lines.append(line)
            total_size += line_size

        # Write selected lines to output file
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("🔥 Kenshiru Logs Private 🔥\n")
            f.write("Made using KenshiruGen Bot\n")
            f.write("=================================\n\n")
            f.writelines(selected_lines)

        await asyncio.sleep(1.5)  # simulate work time

        with open(output_file, "rb") as f:
            await query.message.reply_document(
                document=InputFile(f),
                caption=(
                    f"✅ *File Generated Successfully!*\n\n"
                    f"📂 *Filename:* Kenshiru_Logs_Vip.txt\n"
                    f"📏 *Size:* {size_mb}MB\n"
                    f"📜 *Lines:* {len(selected_lines)}\n\n"
                    f"_Made using KenshiruGen Bot_"
                ),
                parse_mode="Markdown"
            )

        os.remove(output_file)

    except Exception as e:
        await query.message.edit_text(f"❌ Error: {e}", parse_mode="Markdown")

async def show_logs_menu(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    keyboard = [
        [
            InlineKeyboardButton("📄 1MB", callback_data="logs_size:1"),
            InlineKeyboardButton("📄 3MB", callback_data="logs_size:3"),
            InlineKeyboardButton("📄 5MB", callback_data="logs_size:5"),
        ],
        [
            InlineKeyboardButton("📄 8MB", callback_data="logs_size:8"),
            InlineKeyboardButton("📄 10MB", callback_data="logs_size:10")
        ]
    ]

    await query.message.edit_text(
        "📝 *Welcome to Kenshiru Logs Private!*\n\nChoose a file size to generate:",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, InputFile
from telegram.ext import CallbackContext

# === Store User State ===
import os
import random
import asyncio
import string
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import CallbackContext

# === GLOBAL DICTIONARY ===
import json
import os
import random
import string
import asyncio
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, InputFile
from telegram.ext import CallbackContext

user_custom = {}

# === LOAD ACCESS LIST ===
with open("user_access.json", "r", encoding="utf-8") as f:
    allowed_users = json.load(f)
allowed_users = set(map(int, allowed_users.keys()))

# === HELPERS ===
def generate_random_id(length=8):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def get_game_db_path(game):
    mapping = {
        "codm": "Call.txt",
        "mlbb": "Mall.txt",
        "roblox": "Roblox.txt"
    }
    return mapping.get(game)

def is_authorized(user_id):
    return user_id in allowed_users

# === MAIN HANDLERS ===

# Handle '🔥Your Name🔥' button
async def handle_your_name(update: Update, context: CallbackContext):
    query = update.callback_query
    user = query.from_user

    if not is_authorized(user.id):
        await query.answer("⛔ No access.", show_alert=True)
        return

    user_custom[user.id] = {}

    keyboard = [
        [InlineKeyboardButton("🎮 CODM", callback_data="yourname_select:codm")],
        [InlineKeyboardButton("🎮 MLBB", callback_data="yourname_select:mlbb")],
        [InlineKeyboardButton("🎮 Roblox", callback_data="yourname_select:roblox")],
    ]

    await query.message.edit_text(
        f"🔥 <b>Yo {user.first_name}!</b> 🔥\n\n"
        "Welcome to <b>Your Name</b> Mode! ⚡\n\n"
        "Let's forge your custom file. ✍️\n\n"
        "Pick your weapon (game) below:",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# Handle Game Choice
async def handle_game_choice(update: Update, context: CallbackContext):
    query = update.callback_query
    user = query.from_user

    if not is_authorized(user.id):
        await query.answer("⛔ No access.", show_alert=True)
        return

    _, game = query.data.split(":")
    user_custom[user.id]["game"] = game

    loading_texts = [
        "⚡ processing...",
        "✨ Eto na..",
        f"✅ Na Pick Mo <b>{game.upper()}</b>!"
    ]

    for text in loading_texts:
        await query.message.edit_text(text, parse_mode="HTML")
        await asyncio.sleep(0.2)

    await query.message.edit_text(
        "🧩 Now, choose your <b>file type</b>!\n\n"
        "Example: <code>/type8 Premium</code>\n\n"
        "🔹 Choices:\n"
        "- Premium\n"
        "- Hidden\n"
        "- VIP\n"
        "- Paldo",
        parse_mode="HTML"
    )

# Handle /type8 command
async def handle_type_command(update: Update, context: CallbackContext):
    user = update.effective_user

    if not is_authorized(user.id):
        await update.message.reply_text("⛔ No access.")
        return

    if not context.args:
        await update.message.reply_text("⚠️ Usage: /type8 <Type>")
        return

    if user.id not in user_custom:
        await update.message.reply_text("❌ Denied Please click The Button '🔥Your Name🔥' first to begin.")
        return

    chosen_type = context.args[0]
    user_custom[user.id]["type"] = chosen_type

    sent = await update.message.reply_text("⚙️ Syncing your file type...", parse_mode="HTML")

    steps = ["🔧 Na recieve na...", "⚙️ Lapit na...", "✅ Next Step Na "]
    for step in steps:
        await asyncio.sleep(0.2)
        await sent.edit_text(step, parse_mode="HTML")

    await asyncio.sleep(0.15)
    await sent.delete()

    await update.message.reply_text(
        f"✅ <b>Type selected:</b> <code>{chosen_type}</code>\n\n"
        "Next: drop your <b>custom name</b>! ✍️\n\n"
        "Example: <code>/name8 Yellow</code>",
        parse_mode="HTML"
    )

# Handle /name8 command (100 lines + Anti-Duplicate)
async def handle_name_command(update: Update, context: CallbackContext):
    user = update.effective_user

    if not is_authorized(user.id):
        await update.message.reply_text("⛔ No access.")
        return

    if not context.args:
        await update.message.reply_text("⚠️ Usage: /name8 <YourName>")
        return

    if user.id not in user_custom or "type" not in user_custom[user.id] or "game" not in user_custom[user.id]:
        await update.message.reply_text("❗ Please pick your game and type first!")
        return

    user_name = context.args[0]
    file_type = user_custom[user.id]["type"]
    selected_game = user_custom[user.id]["game"]
    db_path = get_game_db_path(selected_game)

    if not db_path or not os.path.exists(db_path):
        await update.message.reply_text("⚠️ Database not found.")
        return

    status = await update.message.reply_text("⏳ Getting things ready...")

    progress = [
        "Processing na ...",
        "⚙️ Eto na...",
        "🛠️ nahanap na ang  file...",
        "✅ Done..."
    ]
    for stage in progress:
        await asyncio.sleep(0.2)
        await status.edit_text(stage)

    await asyncio.sleep(0.15)
    await status.delete()

    # Load and clean database
    with open(db_path, "r", encoding="utf-8") as file:
        entries = [line.strip() for line in file if line.strip()]

    if not entries:
        await update.message.reply_text("⚠️ Empty database! No entries left.")
        return

    selected_entries = entries[:100]
    remaining_entries = entries[100:]

    # Save back remaining
    with open(db_path, "w", encoding="utf-8") as file:
        file.write('\n'.join(remaining_entries))

    # Build filename like "Name_Type_Game_Data.txt"
    output_filename = f"{user_name}_{file_type}_{selected_game}_Data.txt".replace(" ", "_")
    total_lines = len(selected_entries)
    file_id = generate_random_id()
    username = update.effective_user.username or "Unknown"

    # Write output
    with open(output_filename, "w", encoding="utf-8") as file:
        file.write("🔖 Kazii VIP Bot File\n\n")
        file.write(f"👤 Creator: {update.effective_user.full_name}\n")
        file.write(f"📄 Total Lines: {total_lines}\n")
        file.write(f"🆔 File ID: {file_id}\n")
        file.write(f"📌 Type: {file_type}\n")
        file.write(f"🎮 Game: {selected_game.upper()}\n\n")
        file.write("📝 Entries:\n")
        file.write('\n'.join(selected_entries))

    # Send file
    with open(output_filename, "rb") as file:
        await update.message.reply_document(
            document=InputFile(file),
            caption=(
                "<b>🎯 File Successfully Generated</b>\n\n"
                f"<b>👤 Creator:</b> @{username}\n"
                f"<b>📄 Total Lines:</b> {total_lines}\n"
                f"<b>🆔 File ID:</b> {file_id}\n"
                f"<b>📌 Type:</b> {file_type}\n"
                f"<b>🎮 Game:</b> {selected_game.upper()}\n\n"
                "<i>Generated via KenshiruGenBot</i>"
            ),
            parse_mode="HTML"
        )
# === To Add to Keyboard ===
# [InlineKeyboardButton("🔥Your Name🔥", callback_data="your_name")]

# === In Callback Handler ===
# elif data == "your_name":
#     await handle_your_name(update, context)
# elif data.startswith("yourname_select:"):
#     await handle_game_choice(update, context)

# === Command Handlers ===
# /type8 and /name8

import time
import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext

START_TIME = time.time()

def format_uptime():
    now = time.time()
    uptime_seconds = int(now - START_TIME)
    uptime_str = str(datetime.timedelta(seconds=uptime_seconds))
    hours, remainder = divmod(uptime_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    current_date = datetime.datetime.fromtimestamp(START_TIME).strftime("%Y-%m-%d %H:%M:%S")

    text = (
        "✨ <b>Bot Status Monitor</b> ✨\n\n"
        f"⏰ <b>Uptime:</b> <code>{uptime_str}</code>\n"
        f"⏳ <b>Exact:</b> {hours}h {minutes}m {seconds}s\n"
        f"🖥 <b>Hosted On:</b> <i>Private Server</i>\n"
        f"🚀 <b>Launched:</b> {current_date}\n"
        f"\n<em>Updated live with Kazii VIP Bot</em>"
    )
    return text

# === Handler Function ===
async def handle_uptime(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    text = format_uptime()

    keyboard = [
        [InlineKeyboardButton("🔄 Refresh", callback_data="refresh_uptime")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.edit_text(text, parse_mode="HTML", reply_markup=reply_markup)

# === Callback Router ===
async def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.data == "refresh_uptime":
        await handle_uptime(update, context)
    
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InputFile, Update
from telegram.ext import CallbackContext, CommandHandler
	
import os
import re
import random
import json
from telegram import InputFile, Update
from telegram.ext import CallbackContext

import os
import re
import json
import random
from telegram import Update, InputFile
from telegram.ext import CallbackContext

USED_LINES_FILE = "used_lines.txt"
ACCESS_FILE = "user_access.json"
LOG_FILE = "/sdcard/KENSHIN/ULP.txt"

# ------------------- File Utilities ------------------- #

def load_used_lines():
    if not os.path.exists(USED_LINES_FILE):
        return set()
    with open(USED_LINES_FILE, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f)

def save_used_lines(lines):
    with open(USED_LINES_FILE, "a", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")

def extract_user_pass(line):
    match = re.search(r'([^:/\s]+):([^:/\s]+)\)?$', line.strip())
    return f"{match.group(1)}:{match.group(2)}" if match else None

# ------------------- Access Control ------------------- #

def is_user_authorized(user_id):
    if not os.path.exists(ACCESS_FILE):
        return False
    try:
        with open(ACCESS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return str(user_id) in data
    except json.JSONDecodeError:
        print("Error: user_access.json is corrupted.")
        return False

def add_user_access(user_id):
    data = {}
    if os.path.exists(ACCESS_FILE):
        try:
            with open(ACCESS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            pass
    data[str(user_id)] = None
    with open(ACCESS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def remove_user_access(user_id):
    if not os.path.exists(ACCESS_FILE):
        return
    try:
        with open(ACCESS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        data.pop(str(user_id), None)
        with open(ACCESS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
    except json.JSONDecodeError:
        pass

# ------------------- Bot Command ------------------- #

async def handle_search_command(update: Update, context: CallbackContext):
    user_id = update.effective_user.id

    if not is_user_authorized(user_id):
        await update.message.reply_text("❌ You are not authorized to use this command.")
        return

    if len(context.args) == 0:
        await update.message.reply_text("⚠️ Usage: /search <keyword>", parse_mode="Markdown")
        return

    keyword = " ".join(context.args).lower()

    if not os.path.exists(LOG_FILE):
        await update.message.reply_text("❌ logs.txt not found.")
        return

    used_lines = load_used_lines()
    found_lines = []

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if keyword in line.lower():
                stripped = line.strip()
                if stripped not in used_lines:
                    found_lines.append(stripped)
                    if len(found_lines) >= 100:
                        break

    if not found_lines:
        await update.message.reply_text("❌ No new matches found.")
        return

    user_pass_results = []
    for line in found_lines:
        user_pass = extract_user_pass(line)
        if user_pass:
            user_pass_results.append(user_pass)

    temp_filename = f"SearchResult_{keyword[:10]}.txt"
    with open(temp_filename, "w", encoding="utf-8") as f:
        f.write("🔎 Search Results by Kazii VIP Bot\n")
        f.write(f"Keyword: {keyword}\n")
        f.write("-----------------------------------\n\n")
        f.write("\n".join(user_pass_results))

    with open(temp_filename, "rb") as f:
        await update.message.reply_document(
            document=InputFile(f),
            caption=f"✅ `{len(user_pass_results)}` result(s) found for: `{keyword}`\n⚡ Powered by Kazii VIP Bot",
            parse_mode="Markdown"
        )

    os.remove(temp_filename)
    save_used_lines(found_lines)   
         
import aiohttp
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

async def get_roblox_user_info(username, password):
    try:
        async with aiohttp.ClientSession() as session:
            # Step 1: Lookup user ID
            lookup_url = "https://users.roblox.com/v1/usernames/users"
            async with session.post(lookup_url, json={"usernames": [username]}) as res:
                if res.status != 200:
                    return {"error": f"❌ Roblox API Error ({res.status})"}
                data = await res.json()
                if not data.get("data") or not data["data"]:
                    return {"error": "❌ User not found"}
                user_id = data["data"][0].get("id")

            # Helper to get JSON safely
            async def fetch_json(url):
                try:
                    async with session.get(url) as r:
                        return await r.json() if r.status == 200 else {}
                except:
                    return {}

            # Step 2: Fetch profile-related data
            profile = await fetch_json(f"https://users.roblox.com/v1/users/{user_id}")
            friends = await fetch_json(f"https://friends.roblox.com/v1/users/{user_id}/friends/count")
            followers = await fetch_json(f"https://friends.roblox.com/v1/users/{user_id}/followers/count")
            badges = await fetch_json(f"https://badges.roblox.com/v1/users/{user_id}/badges")
            groups = await fetch_json(f"https://groups.roblox.com/v1/users/{user_id}/groups/roles")
            avatar_data = await fetch_json(f"https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={user_id}&size=150x150&format=Png")

            avatar = ""
            if avatar_data and avatar_data.get("data"):
                avatar = avatar_data["data"][0].get("imageUrl", "")

            return {
                "username": username,
                "password": password,
                "user_id": user_id,
                "display_name": profile.get("displayName", "N/A"),
                "name": profile.get("name", username),
                "age": profile.get("age", "?"),
                "created": profile.get("created", "Unknown"),
                "is_banned": profile.get("isBanned", False),
                "friends": friends.get("count", 0),
                "followers": followers.get("count", 0),
                "badges": len(badges.get("data", [])),
                "groups": len(groups.get("data", [])),
                "avatar": avatar,
                "profile_url": f"https://www.roblox.com/users/{user_id}/profile"
            }

    except Exception as e:
        return {"error": f"❌ Unexpected error: {str(e)}"}


from telegram.constants import ParseMode
import re
import re

def escape_md(text: str) -> str:
    escape_chars = r'\_*[]()~`>#+-=|{}.!'
    return re.sub(f'([{re.escape(escape_chars)}])', r'\\\1', str(text))

async def handle_roblox_combo(update: Update, context: CallbackContext):
    try:
        text = update.message.text.strip()
        if not text.startswith("/") or ":" not in text:
            await update.message.reply_text("❌ Invalid format. Use `/username:password`.")
            return

        creds = text[1:].split(":", 1)
        if len(creds) != 2:
            await update.message.reply_text("❌ Invalid format. Use `/username:password`.")
            return

        username, password = creds
        info = await get_roblox_user_info(username, password)

        if "error" in info:
            await update.message.reply_text(info["error"])
            return

        # Escape all dynamic fields
        escaped_username = escape_md(info['username'])
        escaped_display_name = escape_md(info['display_name'])
        escaped_password = escape_md(info['password'])
        escaped_created = escape_md(info['created'])
        escaped_url = escape_md(info['profile_url'])

        msg = (
            "🎮 *Roblox Profile Info*\n\n"
            f"👤 *Username:* `{escaped_username}` \{escaped_display_name}\\n"
            f"🔑 *Password:* `{escaped_password}`\n"
            f"🆔 *UserID:* `{info['user_id']}`\n"
            f"📅 *Account Age:* `{info['age']}` days\n"
            f"📆 *Join Date:* `{escaped_created}`\n"
            f"💼 *Groups:* `{info['groups']}`\n"
            f"🤝 *Friends:* `{info['friends']}`\n"
            f"👥 *Followers:* `{info['followers']}`\n"
            f"🏅 *Badges:* `{info['badges']}`\n"
            f"🚫 *Banned:* {'Yes' if info['is_banned'] else 'No'}\n\n"
            f"[🔗 View Profile]({escaped_url})"
        )

        keyboard = [
            [InlineKeyboardButton("👁 View Profile", url=info['profile_url'])],
            [InlineKeyboardButton("📋 Copy UserID", callback_data=f"copy:{info['user_id']}")]
        ]

        await update.message.reply_photo(
            photo=info["avatar"],
            caption=msg,
            parse_mode=ParseMode.MARKDOWN_V2,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    except Exception as e:
        await update.message.reply_text(f"❌ Handler error: {str(e)}")
import json

# A simple way to store reviews, you can replace this with a database or more complex storage system
ratings_file = 'ratings.json'

# Function to load ratings from the file
def load_ratings():
    if os.path.exists(ratings_file):
        with open(ratings_file, 'r') as file:
            return json.load(file)
    else:
        return {"ratings": [], "total_reviews": 0, "average_rating": 0}

# Function to save the ratings data
def save_ratings(ratings_data):
    with open(ratings_file, 'w') as file:
        json.dump(ratings_data, file)

async def callback_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data

    logging.info(f"Received callback query: {data}")
    await query.answer()  # Prevent Telegram timeout error

    try:
        # When user clicks Rate Us
        if data == "rate_us":
            rate_keyboard = [
                [InlineKeyboardButton("⭐ 1 Star", callback_data="rate_1"),
                 InlineKeyboardButton("⭐ 2 Stars", callback_data="rate_2"),
                 InlineKeyboardButton("⭐ 3 Stars", callback_data="rate_3")],

                [InlineKeyboardButton("⭐ 4 Stars", callback_data="rate_4"),
                 InlineKeyboardButton("⭐ 5 Stars", callback_data="rate_5")]
            ]
            rate_markup = InlineKeyboardMarkup(rate_keyboard)
            await query.edit_message_text("🌟 Please rate us by selecting a star rating:", reply_markup=rate_markup)

        # Handle rating selection (1 to 5 stars)
        elif data.startswith("rate_"):
            rating = int(data.split("_")[1])  # Extract rating value (1 to 5)
            ratings_data = load_ratings()

            # Add the new rating to the list
            ratings_data["ratings"].append(rating)

            # Calculate new total reviews and average rating
            ratings_data["total_reviews"] = len(ratings_data["ratings"])
            ratings_data["average_rating"] = sum(ratings_data["ratings"]) / ratings_data["total_reviews"]

            # Save the updated ratings data
            save_ratings(ratings_data)

            # Show the total reviews and average rating
            total_reviews = ratings_data["total_reviews"]
            average_rating = round(ratings_data["average_rating"], 2)

            await query.edit_message_text(
                f"Thank you for your rating! ⭐\n\n"
                f"Total Reviews: {total_reviews}\n"
                f"Average Rating: {average_rating} ⭐",
                parse_mode="Markdown"
            )

        # Handle other callback data (such as database menu, etc.)
        elif data == "database_menu":
            await database_menu(update, context)
        elif data == "generate_account":
            await generate_account(update, context)
        # Continue handling other callbacks...
    
    except Exception as e:
        logging.error(f"Error processing callback: {e}")
        await query.message.edit_text("⚠️ An error occurred while processing your request.", parse_mode="Markdown")
import json
import datetime
from telegram import Update
from telegram.ext import CallbackContext

# Load user IDs from JSON file
def load_all_users():
    try:
        with open("user_access.json", "r") as f:
            user_data = json.load(f)
        return set(map(int, user_data.keys()))
    except Exception as e:
        print(f"[ERROR] Failed to load user_access.json: {e}")
        return set()

# Announcement message handler
import datetime
import random
import asyncio
from telegram import Update
from telegram.ext import CallbackContext

async def announcement_message_handler(update: Update, context: CallbackContext):
    user = update.effective_user
    user_id = user.id

    if user_id in awaiting_announcement:
        awaiting_announcement.remove(user_id)
        text = update.message.text
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        message = (
            f"✨ *ANNOUNCEMENT* ✨\n\n"
            f"*📢 {text.upper()}*\n\n"
            f"---\n"
            f"From: @{user.username if user.username else 'Unknown User'} (`{user_id}`)\n"
            f"Time: {timestamp}\n"
        )

        all_users = list(load_all_users())
        selected_users = all_users  # Use full list, no more limiting to 15

        semaphore = asyncio.Semaphore(5)  # Max 5 concurrent sends

        async def send_announcement(recipient_id):
            async with semaphore:
                try:
                    await context.bot.send_message(chat_id=recipient_id, text=message, parse_mode="Markdown")
                    return True
                except Exception as e:
                    print(f"Failed to send to {recipient_id}: {e}")
                    return False

        tasks = [send_announcement(uid) for uid in selected_users]
        results = await asyncio.gather(*tasks)
        recipients = sum(results)

        admin_message = (
            f"📢 *Announcement Broadcasted*\n\n"
            f"✨ *Announcement successfully sent to {recipients} users!*\n\n"
            f"Details:\n"
            f"🔹 *Message sent by:* @{user.username if user.username else 'Unknown User'}\n"
            f"🔹 *Total Users Received:* {recipients}\n"
            f"🔹 *Timestamp of Announcement:* {timestamp}"
        )
        await context.bot.send_message(chat_id=admin_user_id, text=admin_message, parse_mode="Markdown")

        await update.message.reply_text(
            f"✅ *Announcement sent successfully to {recipients} users!*",
            parse_mode="Markdown"
        )

    else:
        await update.message.reply_text(
            "⚠️ *Oops!*\n\n"
            "It looks like you're trying to chat directly — but my powers work best through *commands only!*\n\n"
            "Here’s what I can help you with:\n\n"
            "🔑 */key* — Enter your access key to unlock features\n"
            "🎲 */generate* — Start generating accounts or combos\n\n"
            "— — — — — — — — — —\n"
            "*Access Key Pricing:* \n"
            "• 3 Days — 50 PHP\n"
            "• 5 Days — 80 PHP\n"
            "• 1 Month — 100 PHP\n"
            "• Lifetime — 200 PHP\n\n"
            "To get your key, send proof of payment to *@kazikamiii*"
            "\nLet’s get generating!",
            parse_mode="Markdown"
        )
admin_user_id = 7141864085  # Replace with your actual Telegram user ID

async def make_announcement(query, context):
    user_id = query.from_user.id

    # Check if the user is already awaiting an announcement
    if user_id not in awaiting_announcement:
        awaiting_announcement.add(user_id)
        await query.message.reply_text("📝 *Type your announcement message:*", parse_mode="Markdown")
    else:
        await query.message.reply_text("❗ You are already in the process of making an announcement.", parse_mode="Markdown")
        
awaiting_announcement = set()
       
        
async def handle_help(update: Update, context: CallbackContext):
    await context.bot.send_animation(
        chat_id=update.effective_chat.id,
        animation="https://media.giphy.com/media/UTdVUEGB4t0rS/giphy.gif",  # Smooth tech vibe animation
        caption=(
            "*🔧 Kenshiruu Bot — Help Panel*\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "*📂 Database*  ➤ Manage accounts\n"
            "*🎲 Generate Account*  ➤ Create new accounts\n"
            "*🚀 Ovi Gen*  ➤ Quick Ovi account generation\n"
            "*🌀 EH Combo Gen*  ➤ Generate combos (email:pass)\n"
            "*📜 View Logs*  ➤ Track generation history\n"
            "*📊 Total Gen*  ➤ View all generated accounts\n"
            "*👤 My Stats*  ➤ See personal stats\n"
            "*🔑 Access List*  ➤ View who has bot access\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "❓ *Need help? Message the admin.*\n"
            "⚙️ _Powered by Kazii VIP Bot_"
        ),
        parse_mode="Markdown"
    )
    
async def show_total_generated(update: Update, context: CallbackContext):
    try:
        if not os.path.exists("generation_history.txt"):
            await update.callback_query.message.reply_text("⚠️ No logs found.")
            return

        user_count = {}
        total_lines = 0

        with open("generation_history.txt", "r", encoding="utf-8") as f:
            logs = f.read().split("----------------------------------------\n")
            for block in logs:
                if "User:" in block and "Lines Generated:" in block:
                    lines = block.split("\n")
                    user_line = next((line for line in lines if line.startswith("User:")), None)
                    line_count = next((line for line in lines if line.startswith("Lines Generated:")), None)

                    if user_line and line_count:
                        name_id_part = user_line.replace("User:", "").strip()
                        lines_generated = int(line_count.split(":")[1].strip())

                        user_count[name_id_part] = user_count.get(name_id_part, 0) + lines_generated
                        total_lines += lines_generated

        msg = "📊 *Kazii VIP Bot - Total Generated Summary:*\n\n"
        msg += f"📦 *Overall Total Generated:* `{total_lines}` lines\n\n"
        msg += "👤 *User Contributions:*\n"

        for user, count in user_count.items():
            msg += f"• `{user}` → `{count}` lines\n"

        await update.callback_query.message.reply_text(msg, parse_mode="Markdown")

    except Exception as e:
        logging.error(f"Error in show_total_generated: {e}")
        await update.callback_query.message.reply_text("❌ Error reading logs.")
        
async def show_my_stats(update: Update, context: CallbackContext):
    query = update.callback_query
    user = query.from_user
    user_id = str(user.id)

    total_lines = 0
    count = 0

    if not os.path.exists("generation_history.txt"):
        await query.message.reply_text("⚠️ No logs yet.")
        return

    with open("generation_history.txt", "r", encoding="utf-8") as f:
        blocks = f.read().split("----------------------------------------\n")

    for block in blocks:
        if f"({user_id})" in block and "Lines Generated:" in block:
            lines = block.split("\n")
            for line in lines:
                if line.startswith("Lines Generated:"):
                    num = int(line.split(":")[1].strip())
                    total_lines += num
                    count += 1

    await query.message.reply_text(
        f"👤 *Your Stats, {user.first_name}:*\n\n"
        f"📄 Total Generations: `{count}`\n"
        f"📦 Total Lines: `{total_lines}`",
        parse_mode="Markdown"
    )        
    
import os
import asyncio

import os
import asyncio

async def combo_menu(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    await query.message.delete()  # Auto-delete to prevent spam 🗑️

    keyboard = [
        [InlineKeyboardButton("📧 Gmail 💌", callback_data="combo_gmail")],
        [InlineKeyboardButton("✉ Hotmail 📬", callback_data="combo_hotmail")],
        [InlineKeyboardButton("🔙 Back to Menu 🏠", callback_data="menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.reply_text("✨ *Pick your email provider!* 💖", parse_mode="Markdown", reply_markup=reply_markup)

async def combo_select_lines(update: Update, context: CallbackContext, provider: str):
    query = update.callback_query
    await query.answer()
    await query.message.delete()

    keyboard = [
        [InlineKeyboardButton("1️⃣ 1K Lines", callback_data=f"combo_lines:{provider}:1000")],
        [InlineKeyboardButton("5️⃣ 5K Lines", callback_data=f"combo_lines:{provider}:5000")],
        [InlineKeyboardButton("🔟 10K Lines", callback_data=f"combo_lines:{provider}:10000")],
        [InlineKeyboardButton("🔙 Back ↩️", callback_data="combo_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.reply_text(f"📌 *How many lines from {provider.upper()}?* 🤔", parse_mode="Markdown", reply_markup=reply_markup)

async def combo_confirm(update: Update, context: CallbackContext, provider: str, lines: int):
    query = update.callback_query
    await query.answer()
    await query.message.delete()

    keyboard = [
        [InlineKeyboardButton("✅ Yes, proceed 🚀", callback_data=f"combo_confirm:{provider}:{lines}")],
        [InlineKeyboardButton("❌ No, cancel 😢", callback_data="combo_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.reply_text(f"⚠️ *Are you sure you want {lines} lines from {provider.upper()}?* 🤔", parse_mode="Markdown", reply_markup=reply_markup)

async def generate_combo_file(update: Update, context: CallbackContext, provider: str, lines: int):
    query = update.callback_query
    await query.answer()
    await query.message.delete()

    file_path = f"{provider}.txt"
    output_file = f"combo_{provider}_{lines}.txt"

    try:
        # Step 1: Show cute loading animation ✨
        loading_texts = ["⏳ Preparing magic... 🎩✨", "🔄 Gathering lines... 📄", "🚀 Almost there... 💨"]
        loading_message = await query.message.reply_text(loading_texts[0], parse_mode="Markdown")

        for text in loading_texts[1:]:
            await asyncio.sleep(1.5)  # Smooth animation effect 🔄
            await loading_message.edit_text(text, parse_mode="Markdown")

        # Step 2: Read the database 📄
        with open(file_path, "r") as f:
            all_lines = f.readlines()

        if len(all_lines) < lines:
            await loading_message.edit_text("⚠️ *Oops! Not enough data available!* 😢", parse_mode="Markdown")
            return

        # Step 3: Get exact number of lines
        selected_lines = all_lines[:lines]

        # Step 4: Save selected lines to a new file
        with open(output_file, "w") as f:
            f.writelines(selected_lines)

        # Step 5: Delete loading message & send file 🎉
        await loading_message.delete()
        await context.bot.send_document(
            chat_id=query.message.chat_id,
            document=open(output_file, "rb"),
            filename=output_file,
            caption=f"🎉 *Here's your {lines} lines from {provider.upper()}!* 🎊 Enjoy! 🥳"
        )

        # Step 6: Clean up file after sending 🗑️
        os.remove(output_file)

    except Exception as e:
        await query.message.reply_text(f"❌ *Error:* {str(e)} 😞")
# === SHOW DATABASE MENU ===
import random
import time
import asyncio

import random
import asyncio
import random
import asyncio
import random
import asyncio

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import random
import asyncio

import logging
import random
import asyncio
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

async def generate_account(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    # Delete the button message immediately
    try:
        await query.message.delete()
    except:
        pass  

    # Show selection menu
    keyboard = [
        [InlineKeyboardButton("🎮 ML Account", callback_data="generate_ml")],
        [InlineKeyboardButton("🔫 CODM Account", callback_data="generate_codm")],
        [InlineKeyboardButton("🛒 Codashop Account", callback_data="generate_codashop")],
        [InlineKeyboardButton("📺 Netflix Account", callback_data="generate_netflix")],
        [InlineKeyboardButton("🎮 Roblox Account", callback_data="generate_roblox")],
        [InlineKeyboardButton("❌ Cancel", callback_data="cancel")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.reply_text("🔽 *Select an account type:*", parse_mode="Markdown", reply_markup=reply_markup)

import random
import asyncio
from telegram import Update
from telegram.ext import CallbackContext

import random
import asyncio
from telegram import Update, InputFile
from telegram.ext import CallbackContext

import random
import asyncio
from io import BytesIO
from telegram import Update, InputFile
from telegram.ext import CallbackContext

async def fetch_account(update: Update, context: CallbackContext, file_path):
    query = update.callback_query
    await query.answer()

    try:
        await query.message.delete()
    except:
        pass

    processing_message = await query.message.reply_text("⏳ Processing...")

    animation_frames = [
        "🔄 Connecting...",
        "⚙️ Fetching data...",
        "✨ Almost ready..."
    ]
    for frame in animation_frames:
        await asyncio.sleep(0.5)
        await processing_message.edit_text(frame)

    await asyncio.sleep(0.5)
    try:
        await processing_message.delete()
    except:
        pass

    try:
        with open(file_path, "r") as f:
            lines = f.readlines()

        if not lines:
            await query.message.reply_text("⚠️ No more available accounts!")
            return

        # Piliin ang 100 lines o mas kaunti kung kulang
        selected = random.sample(lines, min(50, len(lines)))
        selected_stripped = [line.strip() for line in selected]

        # Alisin sa original file
        with open(file_path, "w") as f:
            f.writelines(line for line in lines if line not in selected)

        # I-save sa used_lines.txt
        with open("used_lines.txt", "a") as f:
            for line in selected_stripped:
                f.write(line + "\n")

        # Gawin ang in-memory .txt file gamit BytesIO
        output = BytesIO()
        output.write("\n".join(selected_stripped).encode("utf-8"))
        output.seek(0)

        await query.message.reply_document(
            InputFile(output, filename="Accounts.txt"),
            caption="✅ *50 Accounts Generated*",
            parse_mode="Markdown"
        )

    except Exception as e:
        await query.message.reply_text(f"❌ Error: {str(e)}")
        
async def callback_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data  

    await query.answer()

    try:
        if data == "generate_account":
            await generate_account(update, context)  
        elif data == "generate_ml":
            await fetch_account(update, context, "M.txt")
        elif data == "generate_codm":
            await fetch_account(update, context, "C.txt")
        elif data == "generate_codashop":
            await fetch_account(update, context, "Co.txt")
        elif data == "generate_netflix":
            await fetch_account(update, context, "Net.txt")
        elif data == "generate_roblox":
            await fetch_account(update, context, "Rob.txt")
        elif data == "cancel":
            try:
                await query.message.delete()
            except:
                pass  
    except Exception as e:
        logging.error(f"Error processing callback: {e}")
# === DATABASE MENU ===
ITEMS_PER_PAGE = 9  

async def database_menu(update: Update, context: CallbackContext, page=0):
    user = update.callback_query.from_user
    user_id = user.id
    username = f"@{user.username}" if user.username else user.first_name

    if not has_access(user_id):
        await update.callback_query.answer("⚠️ Access Denied: Unauthorized User", show_alert=True)
        return

    game_list = list(DATABASE_FILES.keys())
    total_files = len(game_list)
    total_pages = (total_files // ITEMS_PER_PAGE) + (1 if total_files % ITEMS_PER_PAGE > 0 else 0)

    start = page * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    showed_files = game_list[start:end]

    button_list = [
        InlineKeyboardButton(f"📂 {game}", callback_data=f"select_game:{game}")
        for game in showed_files
    ]

    keyboard = [button_list[i:i + 3] for i in range(0, len(button_list), 3)]

    # Navigation buttons
    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton("⬅️ Previous", callback_data=f"page:{page - 1}"))
    if page < total_pages - 1:
        nav_buttons.append(InlineKeyboardButton("Next ➡️", callback_data=f"page:{page + 1}"))

    if nav_buttons:
        keyboard.append(nav_buttons)

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.callback_query.message.edit_text(
        f"👋 *Hello {username}!* \n"
        f"📡 *Welcome To Kazii VIP Bot*\n"
        f"🔹 Select a file from the list below.\n\n"
        f"📂 *Total Database Files:* {total_files}\n"
        f"📄 *Files on This Page:* {len(showed_files)}\n"
        f"📑 *Page:* {page + 1}/{total_pages}",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )
# === GENERATE FILE ===
async def generate_file(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id

    if not has_access(user_id):
        await query.answer("🚫 No access!")
        return

    _, game = query.data.split(":")
    file_name = DATABASE_FILES.get(game)

    if not file_name or not os.path.exists(file_name):
        await query.message.delete()
        await query.message.reply_text(f"❌ *No data available for {game}!*", parse_mode="Markdown")
        return

    await query.message.delete()  # Delete previous message

    keyboard = [
        [
            InlineKeyboardButton("📂 25", callback_data=f"generate_lines:{game}:25"),
            InlineKeyboardButton("📂 50", callback_data=f"generate_lines:{game}:50"),
            InlineKeyboardButton("📂 100", callback_data=f"generate_lines:{game}:100"),
            InlineKeyboardButton("📂 150", callback_data=f"generate_lines:{game}:150"),
        ],
        [
            InlineKeyboardButton("📂 200", callback_data=f"generate_lines:{game}:200"),
            InlineKeyboardButton("📂 250", callback_data=f"generate_lines:{game}:250"),
            InlineKeyboardButton("📂 350", callback_data=f"generate_lines:{game}:350"),
            InlineKeyboardButton("📂 400", callback_data=f"generate_lines:{game}:400"),
        ],
        [
            InlineKeyboardButton("📂 450", callback_data=f"generate_lines:{game}:450"),
            InlineKeyboardButton("📂 550", callback_data=f"generate_lines:{game}:550"),
            InlineKeyboardButton("📂 600", callback_data=f"generate_lines:{game}:600"),
            InlineKeyboardButton("📂 650", callback_data=f"generate_lines:{game}:650"),
        ],
        [
            InlineKeyboardButton("📂 700", callback_data=f"generate_lines:{game}:700"),
            InlineKeyboardButton("📂 750", callback_data=f"generate_lines:{game}:750"),
            InlineKeyboardButton("📂 800", callback_data=f"generate_lines:{game}:800"),
            InlineKeyboardButton("📂 850", callback_data=f"generate_lines:{game}:850"),
        ],
        [
            InlineKeyboardButton("📂 900", callback_data=f"generate_lines:{game}:900"),
            InlineKeyboardButton("📂 950", callback_data=f"generate_lines:{game}:950"),
            InlineKeyboardButton("📂 1000", callback_data=f"generate_lines:{game}:1000"),
            InlineKeyboardButton("📂 1100", callback_data=f"generate_lines:{game}:1100"),
        ],
        [
            InlineKeyboardButton("📂 1200", callback_data=f"generate_lines:{game}:1200"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.reply_text(
        f"📂 *{game} Database Selected!*\n🔹 Choose the number of lines:", 
        parse_mode="Markdown", 
        reply_markup=reply_markup
    )

import requests
import os
import random
import asyncio
import datetime
from telegram import Update, InputFile, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

import datetime

async def generate_selected_lines(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id

    if not has_access(user_id):
        await query.answer("🚫 You do not have access.")
        return

    _, game, num_lines = query.data.split(":")
    num_lines = int(num_lines)
    file_name = DATABASE_FILES.get(game)

    if not file_name or not os.path.exists(file_name):
        await query.message.delete()
        await query.message.reply_text(f"⚠️ No available data for *{game}*.", parse_mode="Markdown")
        return

    # Confirmation Step
    await query.message.delete()

    keyboard = [
        [
            InlineKeyboardButton("✅ Yes, Proceed", callback_data=f"confirm_generate:{game}:{num_lines}"),
            InlineKeyboardButton("❌ No, Cancel", callback_data="cancel_generation")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.reply_text(
        "✅ *Files have been found successfully!*\n\n"
        "Do you want to proceed with the generation?",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

async def confirm_generate(update: Update, context: CallbackContext):
    """Handles when the user clicks 'Yes'."""
    query = update.callback_query
    _, game, num_lines = query.data.split(":")
    num_lines = int(num_lines)
    file_name = DATABASE_FILES.get(game)
    used_lines_file = f"used_lines_{game}.txt"
    user_id = query.from_user.id
    username = query.from_user.username or query.from_user.first_name

    await query.message.edit_text("🔄 *Your Request Has Received, Please wait.....*", parse_mode="Markdown")
    await asyncio.sleep(0.5)

    # Read file data
    with open(file_name, "r", encoding="utf-8") as f:
        all_lines = set(f.readlines())

    if os.path.exists(used_lines_file):
        with open(used_lines_file, "r", encoding="utf-8") as f:
            used_lines = set(f.readlines())
    else:
        used_lines = set()

    available_lines = list(all_lines - used_lines)

    if not available_lines:
        await query.message.edit_text(f"⚠️ All data in *{game}* has been used up.", parse_mode="Markdown")
        return

    selected_lines = available_lines if len(available_lines) < num_lines else random.sample(available_lines, num_lines)

    with open(used_lines_file, "a", encoding="utf-8") as f:
        f.writelines(selected_lines)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result_file = f"{game}_Data_{num_lines}.txt"

    with open(result_file, "w", encoding="utf-8") as f:
        f.write(
            f"🔹Generated by Kazii VIP Bot\n"
            f"📅 Date: {timestamp}\n"
            f"🎮 Source : {game}\n"
            f"📑 Lines Generated: {num_lines}\n\n"
        )
        f.writelines(selected_lines)
        f.write("\n\n🔹Thank You For Using KENSHIRUU Bot")

    # Log the generation event in the history log
    with open("generation_history.txt", "a", encoding="utf-8") as log_file:
        log_file.write(
            f"User: {username} ({user_id})\n"
            f"Game: {game}\n"
            f"Lines Generated: {num_lines}\n"
            f"Timestamp: {timestamp}\n"
            f"----------------------------------------\n"
        )

    # Update total lines generated by user
    user_lines_log = "user_lines_log.txt"
    user_total_lines = 0
    existing_entries = []

    if os.path.exists(user_lines_log):
        with open(user_lines_log, "r", encoding="utf-8") as log_file:
            entry = ""
            for line in log_file:
                if "----------------------------------------" in line:
                    if f"User: {username} ({user_id})" in entry:
                        try:
                            old_count = int(entry.split("Lines Generated: ")[-1].split()[0])
                            user_total_lines = old_count
                        except Exception:
                            pass
                        continue
                    else:
                        existing_entries.append(entry + line)
                        entry = ""
                else:
                    entry += line

    user_total_lines += num_lines
    new_entry = (
        f"User: {username} ({user_id})\n"
        f"Lines Generated: {user_total_lines}\n"
        f"Timestamp: {timestamp}\n"
        f"----------------------------------------\n"
    )

    with open(user_lines_log, "w", encoding="utf-8") as log_file:
        for entry in existing_entries:
            log_file.write(entry)
        log_file.write(new_entry)

    await asyncio.sleep(0.5)
    await query.message.edit_text("✅ *Data has been Found. Please wait...*", parse_mode="Markdown")
    await asyncio.sleep(0.5)

    with open(result_file, "rb") as f:
        await query.message.reply_document(
            document=InputFile(f),
            caption=(
                f"📁{game} PREMIUM FILES\n"
                f"✔️ Lines Generated {num_lines} \n"
                f"📥 Download Your File Now!!.\n\n"
                f"🔹 The File Has Been Generated by Kenshiruu Bot"
            ),
            parse_mode="Markdown"
        )

import asyncio    
# === CALLBACK HANDLER (UPDATE) 
import json
import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

# A simple way to store reviews, you can replace this with a database or more complex storage system
ratings_file = 'ratings.json'

# Function to load ratings from the file
def load_ratings():
    if os.path.exists(ratings_file):
        with open(ratings_file, 'r') as file:
            return json.load(file)
    else:
        return {"ratings": [], "total_reviews": 0, "average_rating": 0}

# Function to save the ratings data
def save_ratings(ratings_data):
    with open(ratings_file, 'w') as file:
        json.dump(ratings_data, file)

async def callback_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data

    logging.info(f"Received callback query: {data}")
    await query.answer()  # Prevent Telegram timeout error

    try:
        # === DATABASE HANDLERS ===
        if data == "database_menu":
            await database_menu(update, context)
        elif data.startswith("select_game:"):
            await generate_file(update, context)
        elif data.startswith("generate_lines:"):
            await generate_selected_lines(update, context)
        elif data.startswith("page:"):
            page = int(data.split(":")[1])
            await database_menu(update, context, page)
        elif data.startswith("confirm_generate:"):
            await confirm_generate(update, context)
        elif data == "search_logs":
            await query.answer()
            await query.message.edit_text(
                "🔍 *Search Mode Activated!*\n\n"
                "Type what you're looking for using this format:\n"
                "`/search your-keyword-here`\n\n"
                "📌 *Example:* `/search mobilelegends.com`\n"
                "🔎 I will search `logs` and return up to 50 matching results in a downloadable file.\n\n"
                "_Powered by Kazii VIP Bot_",
                parse_mode="Markdown"
            )
        elif data == "cancel_generation":
            await cancel_generation(update, context)
        elif data == "access_list":
            await show_access_list(update, context)
        elif data.startswith("revoke_"):
            await revoke_access(update, context)
        elif data == "menu":
            await generate_menu(update, context)
        elif data == "your_name":
            await handle_your_name(update, context)
        elif data.startswith("yourname_select:"):
            await handle_game_choice(update, context)
        elif data == "generate_logs":
            await show_logs_menu(update,context)
        elif data.startswith("logs_size:"): 
            await handle_logs_generation(update, context)   

        # === ANNOUNCEMENT HANDLER ===
        elif data == "make_announcement":
            user_id = query.from_user.id
            awaiting_announcement.add(user_id)
            await query.message.reply_text("📝 *Type your announcement message:*", parse_mode="Markdown")

        # === VIEW LOGS ===
        elif data == "view_logs":
            try:
                with open("generation_history.txt", "r", encoding="utf-8") as log_file:
                    logs = log_file.read()
                log_entries = logs.strip().split("-------------------------------------")
                latest_logs = "-------------------------------------".join(log_entries[-10:])

                await query.message.edit_text(
                    f"📜 *Latest Generation Logs:*\n\n{latest_logs.strip()}",
                    parse_mode="Markdown"
                )
            except FileNotFoundError:
                await query.message.edit_text("⚠️ *No logs found yet.*", parse_mode="Markdown")

        # === OVI HANDLERS ===
        elif data == "ovi_confirm":
            await show_options(update, context)
        elif data == "cancel":
            await cancel_action(update, context)
        elif data.startswith("fetch_"):
            await fetch_lines(update, context)
        elif data == "ovi_warning":
            await show_options(update, context)
        elif data == "search_logs":
             await handle_search_button(update, context)

        # === VGen Tools ===
        elif data == "vgen_tools":
            tools_keyboard = [
                [InlineKeyboardButton("🔒 Encryption", callback_data="encryption_tool")],
                [InlineKeyboardButton("🔗 Separator", callback_data="separator_tool")],
                [InlineKeyboardButton("🔄 Merge", callback_data="merge_tool")],
                [InlineKeyboardButton("❌ Remove URL", callback_data="remove_url_tool")],
                [InlineKeyboardButton("🔀 Unmerge", callback_data="unmerge_tool")]
            ]
            await query.edit_message_text(
                "🛠️ *VGen Tools*\n\nChoose a tool to use:",
                reply_markup=InlineKeyboardMarkup(tools_keyboard),
                parse_mode="Markdown"
            )

        # Handling Each Tool
        elif data == "encryption_tool":
            await query.message.reply_text(
                "🔒 *Encryption Tool*\n\nUse this tool to encrypt your files. Download the tool here:\n"
                "[Encryption Tool - MediaFire](https://www.mediafire.com/file/nzvl3ebeq2gduss/HU.py_enc6.py/file)"
            )

        elif data == "separator_tool":
            await query.message.reply_text(
                "🔗 *Separator Tool*\n\nUse this tool to separate your data. Download the tool here:\n"
                "[Separator Tool - MediaFire](https://www.mediafire.com/file/b5aw3y7vytjj2is/kupal3.py/file)"
            )

        elif data == "merge_tool":
            await query.message.reply_text(
                "🔄 *Merge Tool*\n\nUse this tool to merge your files. Download the tool here:\n"
                "[Merge Tool - MediaFire](https://www.mediafire.com/file/owiw27puon7e7z8/merge.py/file)"
            )

        elif data == "remove_url_tool":
            await query.message.reply_text(
                "❌ *Remove URL Tool*\n\nUse this tool to remove URLs from your files. Download the tool here:\n"
                "[Remove URL Tool - MediaFire](https://www.mediafire.com/file/hvj04dq927gm10g/Shin.py/file)"
            )

        elif data == "unmerge_tool":
            await query.message.reply_text(
                "🔀 *Unmerge Tool*\n\nUse this tool to unmerge your files. Download the tool here:\n"
                "[Unmerge Tool - MediaFire](https://www.mediafire.com/file/jzmenw3lw0zs5jn/split.py/file)"
            )

        # === ACCOUNT HANDLERS ===
        elif data == "generate_account":
            await generate_account(update, context)
        elif data == "generate_ml":
            await fetch_account(update, context, "M.txt")
        elif data == "generate_codm":
            await fetch_account(update, context, "C.txt")
        elif data == "generate_codashop":
            await fetch_account(update, context, "Co.txt")
        elif data == "generate_netflix":
            await fetch_account(update, context, "Net.txt")
        elif data == "generate_roblox":
            await fetch_account(update, context, "Rob.txt")
                # === JOIN LINKS HANDLER ===
        elif data == "show_join_links":
            join_keyboard = [
                [InlineKeyboardButton("🔗 KENSHIRUU Channel", url="https://t.me/Kenshirupalaroo")],
                [InlineKeyboardButton("🪩 KENSHIRUU DC", url="https://t.me/Kenshirudiscussion")],
                [InlineKeyboardButton("🤖 KENSHIRUU PROOF", url="https://t.me/+_SrMBnHE4t8xMDQ9")]
            ]
            await query.edit_message_text(
                "🌐 *Join the KENSHIRUU Community!*\n\nChoose where you want to connect:",
                reply_markup=InlineKeyboardMarkup(join_keyboard),
                parse_mode="Markdown"
            )

        # === CONTACT SUPPORT HANDLER ===
        elif data == "contact_support":
            await query.message.reply_text(
                "📢 *Have a report or inquiry?* \n\n"
                "Please reach out to the support team: \n"
                "💬 *Contact:* @kazikamiii \n\n"
                "We're here to assist you with any questions or issues you might have. Feel free to reach out anytime! 😊",
                parse_mode="Markdown"
            )

        # === RATE US HANDLER ===
        elif data == "rate_us":
            rate_keyboard = [
                [InlineKeyboardButton("⭐ 1 Star", callback_data="rate_1"),
                 InlineKeyboardButton("⭐ 2 Stars", callback_data="rate_2"),
                 InlineKeyboardButton("⭐ 3 Stars", callback_data="rate_3")],

                [InlineKeyboardButton("⭐ 4 Stars", callback_data="rate_4"),
                 InlineKeyboardButton("⭐ 5 Stars", callback_data="rate_5")]
            ]
            rate_markup = InlineKeyboardMarkup(rate_keyboard)
            await query.edit_message_text("🌟 Please rate us by selecting a star rating:", reply_markup=rate_markup)

        # Handle rating selection (1 to 5 stars)
        elif data.startswith("rate_"):
            rating = int(data.split("_")[1])  # Extract rating value (1 to 5)
            
            # Assuming you have functions to load and save ratings
            ratings_data = load_ratings()  # Replace with the actual function to load ratings data

            # Add the new rating to the list
            ratings_data["ratings"].append(rating)

            # Calculate new total reviews and average rating
            ratings_data["total_reviews"] = len(ratings_data["ratings"])
            ratings_data["average_rating"] = sum(ratings_data["ratings"]) / ratings_data["total_reviews"]

            # Save the updated ratings data
            save_ratings(ratings_data)  # Replace with the actual function to save ratings data

            # Show the total reviews and average rating
            total_reviews = ratings_data["total_reviews"]
            average_rating = round(ratings_data["average_rating"], 2)

            await query.edit_message_text(
                f"Thank you for your rating! ⭐\n\n"
                f"Total Reviews: {total_reviews}\n"
                f"Average Rating: {average_rating} ⭐",
                parse_mode="Markdown"
            )
          
        elif data == "roblox_checker":
            await query.message.edit_text(
        "🔎 Send a Roblox combo in this format:\n\n`/user:password`\n\nWe’ll fe0pqpptch real-time info for you.",
        parse_mode="Markdown"
    )
        # === COMBO HANDLERS ===
        elif data == "bot_uptime":
            await handle_uptime(update,context)        
        elif data == "combo_menu":
            await combo_menu(update, context)
        elif data == "combo_gmail":
            await combo_select_lines(update, context, "gmail")
        elif data == "combo_hotmail":
            await combo_select_lines(update, context, "hotmail")
        elif data.startswith("combo_lines:"):
            _, provider, lines = data.split(":")
            await combo_confirm(update, context, provider, int(lines))
        elif data.startswith("combo_confirm:"):
            _, provider, lines = data.split(":")
            await generate_combo_file(update, context, provider, int(lines))
        elif data == "proxy_generator":
            await show_proxy_options(update, context)
        elif data.startswith("proxy_select:"):
            count = int(data.split(":")[1])  # <-- kulang ng indent dapat naka-indent to
            await confirm_proxy_choice(update, context, count)
        elif data.startswith("confirm_proxy:"):
            count = int(data.split(":")[1])
            await generate_proxies(update, context, count)
        elif data == "cancel_proxy":
            await cancel_proxy_generation(update, context)
        elif data == "ml_password_filter":
            context.user_data["ml_password_filter_active"] = True
            await update.callback_query.message.edit_text(
        "📂 *ML Password Filter Activated!*\n\n"
        "Please send your `.txt` file containing the accounts you want to filter.",
        parse_mode="Markdown"
    )
        elif data == "url_remover":
            context.user_data["url_remover_active"] = True
            await update.callback_query.message.edit_text(
        "📂 *URL Remover Activated!*\n\n"
        "Please send your `.txt` file to clean URLs now!",
        parse_mode="Markdown"
    )

        # ✅ HELP MENU HANDLER
        elif data == "help_menu":
            await handle_help(update, context)
         
        # === V2L/BYPASS TUTORIAL HANDLERS ===
        elif data == "v2l_tutorial":
          await show_v2l_menu(update, context)
        elif data == "access_users":
          await show_access_users(update, context)  
        elif data == "bypass_tutorial":
           await show_bypass_tutorial(update, context)
        elif data == "v2l_info":
           await show_v2l_tutorial(update, context)
        elif data == "search_logs":
           await handle_search_button(update,context)
         # === VIP DATABASE HANDLERS === 
        elif data == "vip_database":
            await handle_vip_database(update, context)
        elif data.startswith("vip_select:"):
            await handle_vip_selection(update, context)
        elif data.startswith("vip_lines:"):
            await handle_vip_line_selection(update, context)
        elif data == "vip_confirm":
            await confirm_vip_generate(update, context)
        elif data == "cancel_generation":
            await query.message.edit_text("❌ VIP file generation cancelled.", parse_mode="Markdown")
        elif data == "generate_logs":
           await show_logs_menu(update, context)
        elif data.startswith("logs_size:"):
          await handle_logs_generation(update, context)     
        # === NEW HANDLERS ===
        elif data == "total_generated":
            await show_total_generated(update, context)
        elif data == "my_stats":
            await show_my_stats(update, context)

        else:
            logging.warning(f"Unknown callback data received: {data}")

    except Exception as e:
        logging.error(f"Error processing callback: {e}")
        await query.message.edit_text("⚠️ An error occurred while processing your request.", parse_mode="Markdown")
        #main
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(encrypt_handler)
    app.add_handler(mlbb_separator_handler)
    app.add_handler(mlbb_handler)
    app.add_handler(CallbackQueryHandler(ip_tracker_start, pattern="^ip_tracker$"))
    app.add_handler(CallbackQueryHandler(ip_yes, pattern="^ip_yes$"))
    app.add_handler(CallbackQueryHandler(ip_no, pattern="^ip_no$"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ip_received))
    app.add_handler(CommandHandler("genkey", generate_key))
    app.add_handler(CommandHandler("key", enter_key))
    app.add_handler(CommandHandler("generate", generate_menu))
    app.add_handler(CommandHandler("search", handle_search_command))
    app.add_handler(CommandHandler("type8", handle_type_command))    # Added for Your Name feature
    app.add_handler(CommandHandler("name8", handle_name_command))    # Added for Your Name feature
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), announcement_message_handler))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex(r"^/\w+:\S+"), handle_roblox_combo))
    app.add_handler(MessageHandler(filters.Document.TEXT, handle_file))
    app.add_handler(CommandHandler("start", start_command))
    # Isang CallbackQueryHandler lang pero lahat ng actions kasama na!
    app.add_handler(CallbackQueryHandler(callback_handler))

    app.run_polling()
    
    app = Flask('')

    @app.route('/')
    def home():
      return "Bot Running!"

    def run_web():
      app.run(host='0.0.0.0', port=8080)

    threading.Thread(target=run_web).start()

if __name__ == "__main__":
    main()