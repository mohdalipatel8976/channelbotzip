import asyncio
from pyrogram import Client, filters
from convopyro import Conversation
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, ChatJoinRequest, Message
from pyrogram.types import ReplyKeyboardMarkup, KeyboardButton, RequestChannelInfo, ChatPrivileges, RequestChatInfo
from pyrogram.enums import ChatMemberStatus 
from pyrogram.enums import ChatType
from pyrogram import client
from pymongo import MongoClient
import logging
import random
from pyrogram.errors import ChatAdminRequired, UserNotParticipant, FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid
from cachetools import TTLCache
from time import time
#Coded By @AgentsTeamking, Contact for support

# MongoDB connection setup
client = MongoClient("mongodb+srv://mohdalipatel8976:newPassWord@cluster1.su7cd.mongodb.net/ChannelLogger?retryWrites=true&w=majority")
db = client["Approves_im_piro"]
channels_collection = db["channels"]
users = db["users"]
groups = db["groups_only"]
channels = db["channels_only"]
#Coded By @AgentsTeamking, Contact for support
# Pyrogram bot setup
API_ID = "28723446"  # From https://my.telegram.org/auth
API_HASH = "99c6dc17560ac32678fe67012374fe38"  # From https://my.telegram.org/auth
BOT_TOKEN = "7554556205:AAFQzB_BlWT1bVfrURVgynwGw4cGKeCDNfo"  # From BotFather
welcome_channel_id = -1002578051346
CHANNEL = -1002204422975 #Your public channel username without @ for force subscription.
OWNER_ID = 5996829431 #Go to Telegram and type id and put that value here.
LOG_ID = int("-1002578051346") #Coded By @AgentsTeamking, Contact for support
#Coded By @AgentsTeamking, Contact for support
app = Client("im_piro", api_id=API_ID, api_hash=API_HASH, workers=50, bot_token=BOT_TOKEN)
Conversation(app)
#Coded By @AgentsTeamking, Contact for support
# Default welcome message
DEFAULT_WELCOME_MSG = "5"
DEFAULT_FAREWELL_MSG = "4"  
# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def already_db(user_id):
        user = users.find_one({"user_id" : str(user_id)})
        if not user:
            return False
        return True
#Coded By @AgentsTeamking, Contact for support
def add_user(user_id):
    in_db = already_db(user_id)
    if in_db:
        return
    return users.insert_one({"user_id": str(user_id)}) 

def remove_user(user_id):
    in_db = already_db(user_id)
    if not in_db:
        return 
    return users.delete_one({"user_id": str(user_id)})

def all_users():
    return users.count_documents({})
def all_groups():
    return groups.count_documents({})
def all_channels():
    return channels.count_documents({})

bot_privileges = ChatPrivileges(
    can_invite_users=True,
    can_manage_chat=True,
    can_delete_messages=True,
    can_post_messages=True,
    can_edit_messages=True,
    is_anonymous=False,
    can_restrict_members=False,
    can_manage_video_chats=False,
    can_promote_members=True,
    can_change_info=False
)
#Coded By @AgentsTeamking, Contact for support
user_privileges = ChatPrivileges(
    can_invite_users=True,
    can_manage_chat=True,
    can_delete_messages=True,
    can_post_messages=True,
    can_edit_messages=True,
    is_anonymous=False,
    can_restrict_members=False,
    can_manage_video_chats=False,
    can_promote_members=True,
    can_change_info=False
)

request_channel_info = RequestChannelInfo(
    button_id=1,
    is_creator=False,
    bot_privileges=bot_privileges,
    user_privileges=user_privileges
)


bot_group = ChatPrivileges(
    can_invite_users=True,
    can_manage_chat=True,
    can_delete_messages=True,
    is_anonymous=False,
    can_manage_video_chats=False,
    can_promote_members=True,
    can_change_info=False
)
#Coded By @AgentsTeamking, Contact for support
user_group = ChatPrivileges(
    can_invite_users=True,
    can_manage_chat=True,
    can_delete_messages=True,
    is_anonymous=False,
    can_manage_video_chats=False,
    can_promote_members=True,
    can_change_info=False
)

request_group_info = RequestChatInfo(
    button_id=2,
    is_creator=False,
    bot_privileges=bot_group,
    user_privileges=user_group
)
#Coded By @AgentsTeamking, Contact for support
markup = ReplyKeyboardMarkup(
    [[
        KeyboardButton("Add Channel", request_peer=request_channel_info),
        KeyboardButton("Add Group", request_peer=request_group_info)
    ]],
    resize_keyboard=True,
    is_persistent=True
)

async def is_subscribed(filter, client, update):
    user_id = update.from_user.id
    try:
        member = await client.get_chat_member(chat_id = CHANNEL, user_id = user_id)
    except UserNotParticipant:
        return False#Coded By @AgentsTeamking, Contact for support
    if not member.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER]:
        return False
    else:
        return True

subscribed = filters.create(is_subscribed)

@app.on_message(filters.command("start"))
async def start(bot, message):
    add_user(message.from_user.id)
    mention = message.from_user.mention
    bot_name = app.me.mention  # Get the bot's mention
    effect_ids = [5104841245755180586, 5046509860389126442, 5159385139981059251]
    selected_effect_id = random.choice(effect_ids)
    start_msg = (
        f"**👋 Hi {mention},**\n\n"
        f"**I'm {bot_name}**\n\n"
        "🔖 **Exclusive Features:**\n"
        "- **Auto approve join requests**\n"
        "- **Set custom welcome messages**\n"
        "- **Set custom farewell messages**\n" 
        "- **Welcome users without approve**\n"
        "- **Manage your Chat settings easily**\n"
        "- **Unlimited Chats Supported**\n"
        "- **No downtime ⏳**\n"
        "- **Approve All Pending Requests (beta)**\n"
        "- **Only Works Pvt Channel & Group**\n\n"
        "**Completely Developed By @AgentsTeamking**\n"
        "**Click below to get started!**"
    )
#Coded By @AgentsTeamking, Contact for support
    buttons = [
        [InlineKeyboardButton("❓ How to Use Me", callback_data="help")],
        [InlineKeyboardButton("📂 My Channels", callback_data="my_channels")],
        [InlineKeyboardButton("🔔 Updates", url="https://t.me/+8Hgte7sPT8c5NTY1")]
    ]
    try:
        await app.get_chat_member(chat_id=CHANNEL, user_id=message.from_user.id)
        await message.reply(start_msg, reply_markup=InlineKeyboardMarkup(buttons), effect_id=selected_effect_id)
    except UserNotParticipant:
        await message.reply_text(
            text=f"**You must join [Channel](https://t.me/autojoinrequestuse) to use me.**",
            reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Join Now", url=f"https://t.me/autojoinrequestuse"),
                InlineKeyboardButton("Joined ✅", url=f"https://t.me/{app.me.username}?start=im_piro")
            ],
            [
                InlineKeyboardButton(f"Join Updates Channel", url=f"https://t.me/+8Hgte7sPT8c5NTY1")
            ]
            ]),
            disable_web_page_preview = True,
            effect_id=selected_effect_id)
    except ChatAdminRequired:
        await app.send_message(text=f"I'm not admin in fsub chat, Ending fsub...", chat_id=OWNER_ID)

# Handle callback queries for "Help"
@app.on_callback_query(subscribed & filters.regex("help"))
async def help_callback(bot, callback_query: CallbackQuery):
    help_msg = ("Usage instructions:\n\nUse buttons to add me in chats, then go to mychannels to manage settings!\n\nI'm here to help automate tasks like approving join requests and managing your channel settings.")

    buttons = [
        [InlineKeyboardButton("📂 My Channels", callback_data="my_channels")],
        [InlineKeyboardButton("🏠 Main Menu", callback_data="start")]
    ]
    
    await callback_query.edit_message_text(help_msg, reply_markup=InlineKeyboardMarkup(buttons))
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text="👇 Use the buttons below to interact:",
        reply_markup=markup
    )
#Coded By @AgentsTeamking, Contact for support
@app.on_callback_query(subscribed & filters.regex("start"))
async def start_callback(bot, callback_query: CallbackQuery):
    mention = callback_query.from_user.mention
    bot_name = app.me.mention  # Get the bot's mention

    start_msg = (
        f"**👋 Hi {mention},**\n\n"
        f"**I'm {bot_name}**\n\n"
        "🔖 **Exclusive Features:**\n"
        "- **Auto approve join requests**\n"
        "- **Set custom welcome messages**\n"
        "- **Set custom farewell messages**\n" 
        "- **Welcome users without approve**\n"
        "- **Manage your Chat settings easily**\n"
        "- **Unlimited Chats Supported**\n"
        "- **No downtime ⏳**\n"
        "- **Approve All Pending Requests (beta)**\n"
        "- **Only Works Pvt Channel & Group**\n\n"
        "**Completely Developed By @AgentsTeamking**\n"
        "**Click below to get started!**"
    )

    buttons = [
        [InlineKeyboardButton("❓ How to Use Me", callback_data="help")],
        [InlineKeyboardButton("📂 My Channels", callback_data="my_channels")],
        [InlineKeyboardButton("🔔 Updates", url="https://t.me/+8Hgte7sPT8c5NTY1")]
    ]

    await callback_query.edit_message_text(
        text=start_msg,
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@app.on_chat_join_request()#Coded By @AgentsTeamking, Contact for support
async def handle_join_request(client, request: ChatJoinRequest):
    channel_id = request.chat.id
    user_id = request.from_user.id

    channel = channels_collection.find_one({"channel_id": channel_id})

    if channel:
        if channel.get("approve_join", False):
            await client.approve_chat_join_request(channel_id, user_id)

        welcome_msg = channel.get("welcome_msg", DEFAULT_WELCOME_MSG)

        try:
            if welcome_msg == "5":
                default = await app.get_messages(welcome_channel_id, int(DEFAULT_WELCOME_MSG))
                print(default)
                copied_message = await default.copy(user_id)
                logger.info(f"Default to user {user_id} in {channel_id}")
            else:
                custom = await app.get_messages(welcome_channel_id, int(welcome_msg))
                if custom and not custom.empty:  # Check if custom message exists and is not empty
                    await custom.copy(user_id)
                    logger.info(f"Custom message sent to user {user_id} in {channel_id}")
                else:
                    # Fallback to default message
                    logger.warning(f"Custom message missing or deleted for {user_id} in {channel_id}. Falling back to default.")
                    default = await app.get_messages(welcome_channel_id, int(DEFAULT_WELCOME_MSG))
                    if default:  # Ensure default message exists
                        await default.copy(user_id)
                        logger.info(f"Default message sent to user {user_id} in {channel_id} as fallback.")
                    else:
                        logger.error("Failed to send any welcome message. Default message is also missing.")
        except Exception as e:
            logger.error(f"Failed to send welcome message to {user_id} from message ID {welcome_msg}: {e}")
    else:#Coded By @AgentsTeamking, Contact for support
        default = await app.get_messages(welcome_channel_id, int(DEFAULT_WELCOME_MSG))
        copied_message = await default.copy(user_id)
        logger.warning(f"No Config {channel_id}. {user_id} was not accepted. DWelcome Sent")


# Cache to store channel data (TTL: 1 hour)
channel_cache = TTLCache(maxsize=1000, ttl=3600)#Coded By @AgentsTeamking, Contact for support
# Dictionary to store the last access time of users
user_last_access = {}
@app.on_callback_query(subscribed & filters.regex("my_channels"))
async def my_channels_callback(bot, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    current_page = int(callback_query.data.split(":")[1]) if ":" in callback_query.data else 0
    channels_per_page = 6  # Number of channels to display per page
    cooldown_period = 4 # Cooldown period in seconds

    now = time()
    # Rate limiting: check if user is clicking too frequently
    if user_id in user_last_access and now - user_last_access[user_id] < cooldown_period:
        await callback_query.answer("Don't press too frequently, Please wait...", show_alert=True)
        return

    # Update the last access time
    user_last_access[user_id] = now

    # Fetch user's channels
    user_channels = channels_collection.find({"user_id": user_id})
    user_channels_list = list(user_channels)

    if len(user_channels_list) == 0:
        await callback_query.answer("You don't have any channels added.", show_alert=True)
        return

    # Pagination logic
    start_index = current_page * channels_per_page
    end_index = start_index + channels_per_page
    paginated_channels = user_channels_list[start_index:end_index]
#Coded By @AgentsTeamking, Contact for support
    channel_buttons = []
    for channel in paginated_channels:
        channel_id = channel["channel_id"]
        if channel_id in channel_cache:
            channel_title = channel_cache[channel_id]
        else:
            try:
                chat = await bot.get_chat(channel_id)
                channel_title = chat.title
                channel_cache[channel_id] = channel_title
            except Exception as e:
                logger.error(f"Error fetching channel {channel_id}: {e}")
                continue
        channel_buttons.append(
            [InlineKeyboardButton(channel_title, callback_data=f"config:{channel_id}")]
        )

    # Pagination buttons
    pagination_buttons = []
    if current_page > 0:
        pagination_buttons.append(
            InlineKeyboardButton("⬅️ Back", callback_data=f"my_channels:{current_page - 1}")
        )
    if end_index < len(user_channels_list):
        pagination_buttons.append(
            InlineKeyboardButton("➡️ Next", callback_data=f"my_channels:{current_page + 1}")
        )

    # Add "Add Channel" button at the bottom
    channel_buttons.append([InlineKeyboardButton("➕ Add Channel", callback_data="help")])
    if pagination_buttons:
        channel_buttons.append(pagination_buttons)

    # Display the current page
    await callback_query.edit_message_text(
        f"Here are your channels (Page {current_page + 1}/"
        f"{(len(user_channels_list) + channels_per_page - 1) // channels_per_page}):",
        reply_markup=InlineKeyboardMarkup(channel_buttons)
    )
#Coded By @AgentsTeamking, Contact for support

@app.on_callback_query(subscribed & filters.regex("welcome"))
async def set_custom_welcome_msg(bot, callback_query: CallbackQuery):
    try:
        _, channel_id = callback_query.data.split(":")
        channel_id = int(channel_id)
    except ValueError:
        await callback_query.answer("Invalid callback data format.", show_alert=True)
        return

    user_id = int(callback_query.from_user.id)
    chat_id = callback_query.message.chat.id

    channel = channels_collection.find_one({"user_id": user_id, "channel_id": channel_id})

    if not channel:
        await callback_query.answer("This channel is not configured for you.", show_alert=True)
        return

    welcome_msg = channel.get("welcome_msg", DEFAULT_WELCOME_MSG)
    try:
        if welcome_msg == "5":
            msg = "No custom welcome message is set yet. Please provide a new one."
            await callback_query.message.reply(msg)
        else:
            msg = "Your current custom welcome message is 👇"
            default = await app.get_messages(welcome_channel_id, int(welcome_msg))
            await callback_query.message.reply(msg)
            await default.copy(user_id)
    except Exception as e:
        logger.error(f"Failed to fetch welcome message for channel {channel_id}: {e}")
#Coded By @AgentsTeamking, Contact for support
    await callback_query.answer("Please provide the new custom welcome message.", show_alert=True)
    question = await callback_query.message.reply("Please provide the new custom welcome message in 30s.")
    try:
        #response = await app.ask(identifier=(chat_id, user_id, None), text="Please send me the new custom welcome message within 30 seconds", timeout=30)
        response = await app.listen.Message(filters.incoming , id = filters.user(user_id), timeout = 30)
    except asyncio.TimeoutError:

        buttons = [
            [InlineKeyboardButton("📂 My Channels", callback_data="my_channels")],
        ]
        return await callback_query.edit_message_text("Too late 30s gone. Please try again..", reply_markup=InlineKeyboardMarkup(buttons))
    
    try:
        copied_msg = await response.copy(chat_id=welcome_channel_id)
        copied_msg_id = copied_msg.id

        channels_collection.update_one(
            {"channel_id": channel_id},
            {"$set": {"welcome_msg": copied_msg_id}}
        )

        buttons = [
            [InlineKeyboardButton("📂 My Channels", callback_data="my_channels")],
            [InlineKeyboardButton("Set Custom Welcome Message ✨", callback_data=f"welcome:{channel_id}")],
            [InlineKeyboardButton("Remove Custom Welcome Message ❌", callback_data=f"remcustom:{channel_id}")],
            [InlineKeyboardButton("Set Custom Farewell Message ✨", callback_data=f"farewell:{channel_id}")],
            [InlineKeyboardButton("Remove Custom Farewell Message ❌", callback_data=f"remfarewell:{channel_id}")],
        ]
        await callback_query.message.reply(
            "Custom welcome message has been set.",
            reply_markup=InlineKeyboardMarkup(buttons)
        )#Coded By @AgentsTeamking, Contact for support
        await question.delete()
        logger.info(f"Custom welcome message updated for channel {channel_id} by user {user_id}, copied message ID: {copied_msg_id}")
    except Exception as e:
        logger.error(f"Error during welcome message setup: {e}")
        await question.delete()
        await callback_query.message.reply(f"An error occurred: {e}")

@app.on_callback_query(subscribed & filters.regex("remcustom"))
async def remove_custom_message(bot, callback_query: CallbackQuery):
    try:
        _, channel_id = callback_query.data.split(":")
        channel_id = int(channel_id)
    except ValueError:
        await callback_query.answer("Invalid callback data format.", show_alert=True)
        return

    user_id = callback_query.from_user.id

    # Fetch the channel from the database
    channel = channels_collection.find_one({"user_id": user_id, "channel_id": channel_id})

    if not channel:
        await callback_query.answer("This channel is not configured for you.", show_alert=True)
        return
#Coded By @AgentsTeamking, Contact for support
    # Check the current welcome message
    current_msg = channel.get("welcome_msg", DEFAULT_WELCOME_MSG)
    if current_msg == DEFAULT_WELCOME_MSG:
        await callback_query.answer("No custom welcome message is set.", show_alert=True)
        return

    # Reset the welcome message to the default
    channels_collection.update_one(
        {"channel_id": channel_id},
        {"$set": {"welcome_msg": DEFAULT_WELCOME_MSG}}
    )

    await callback_query.answer("Custom welcome message removed.", show_alert=True)

    approve_status = "✅ Enabled" if channel.get("approve_join", False) else "❌ Disabled"
    custom_welcome_status = "❌ Not Set"
    custom_farewell_status = "✅ Set" if channel.get("farewell_msg", DEFAULT_FAREWELL_MSG) != DEFAULT_FAREWELL_MSG else "❌ Not Set"

    settings_msg = (
        f"Channel Configuration for {channel_id}:\n\n"
        f"Auto-Approve Join Requests: {approve_status}\n"
        f"Custom Welcome Message: {custom_welcome_status}\n"
        f"Custom Farewell Message: {custom_farewell_status}\n\n"
        "Choose an option to configure:"
    )

    buttons = [
        [InlineKeyboardButton("Approve Join Request ✅" if channel.get("approve_join") else "Approve Join Request ❌", callback_data=f"approve:{channel_id}")],
        [InlineKeyboardButton("Set Custom Welcome Message ✨", callback_data=f"welcome:{channel_id}")],
        [InlineKeyboardButton("Remove Custom Welcome Message ❌", callback_data=f"remcustom:{channel_id}")],
        [InlineKeyboardButton("Set Custom Farewell Message ✨", callback_data=f"farewell:{channel_id}")],  # Added
        [InlineKeyboardButton("Remove Custom Farewell Message ❌", callback_data=f"remfarewell:{channel_id}")],  # Added
        [InlineKeyboardButton("Approve All Pending Requests 👥", callback_data="accept_all")],
        [InlineKeyboardButton("Remove Channel 🗑️", callback_data=f"remove:{channel_id}")],
        [InlineKeyboardButton("🏠 Main Menu", callback_data="start")]
    ]#Coded By @AgentsTeamking, Contact for support
    try:
        await callback_query.edit_message_text(settings_msg, reply_markup=InlineKeyboardMarkup(buttons))
    except Exception as e:
        await callback_query.answer(f"Error Agya {e}", show_alert=True)

@app.on_callback_query(subscribed & filters.regex("farewell"))
async def set_custom_farewell_msg(bot, callback_query: CallbackQuery):
    try:
        _, channel_id = callback_query.data.split(":")
        channel_id = int(channel_id)
    except ValueError:
        await callback_query.answer("Invalid callback data format.", show_alert=True)
        return

    user_id = int(callback_query.from_user.id)
    chat_id = callback_query.message.chat.id

    channel = channels_collection.find_one({"user_id": user_id, "channel_id": channel_id})
#Coded By @AgentsTeamking, Contact for support
    if not channel:
        await callback_query.answer("This channel is not configured for you.", show_alert=True)
        return

    farewell_msg = channel.get("farewell_msg", DEFAULT_FAREWELL_MSG)
    try:
        if farewell_msg == DEFAULT_FAREWELL_MSG:
            msg = "No custom farewell message is set yet. Please provide a new one."
            await callback_query.message.reply(msg)#Coded By @AgentsTeamking, Contact for support
        else:
            msg = "Your current custom farewell message is 👇"
            default = await app.get_messages(welcome_channel_id, int(farewell_msg))
            await callback_query.message.reply(msg)
            await default.copy(user_id)
    except Exception as e:
        logger.error(f"Failed to fetch farewell message for channel {channel_id}: {e}")
#Coded By @AgentsTeamking, Contact for support
    await callback_query.answer("Please provide the new custom farewell message.", show_alert=True)
    question = await callback_query.message.reply("Please provide the new farewell welcome message in 30s.")
    try:
        #response = await app.ask(identifier=(chat_id, user_id, None), text="Please send me the new custom farewell message within 30 seconds", timeout=30)
        response = await app.listen.Message(filters.incoming , id = filters.user(user_id), timeout = 30)
    except asyncio.TimeoutError:
        buttons = [
            [InlineKeyboardButton("📂 My Channels", callback_data="my_channels")],
        ]
        return await callback_query.edit_message_text("TimeUp, send farewell message in 30s. Please try again.", reply_markup=InlineKeyboardMarkup(buttons))
    
    try:
        copied_msg = await response.copy(chat_id=welcome_channel_id)
        copied_msg_id = copied_msg.id

        channels_collection.update_one(
            {"channel_id": channel_id},
            {"$set": {"farewell_msg": copied_msg_id}}
        )

        buttons = [
            [InlineKeyboardButton("📂 My Channels", callback_data="my_channels")],
            [InlineKeyboardButton("Set Custom Welcome Message ✨", callback_data=f"welcome:{channel_id}")],
            [InlineKeyboardButton("Remove Custom Welcome Message ❌", callback_data=f"remcustom:{channel_id}")],
            [InlineKeyboardButton("Set Custom Farewell Message ✨", callback_data=f"farewell:{channel_id}")],
            [InlineKeyboardButton("Remove Custom Farewell Message ❌", callback_data=f"remfarewell:{channel_id}")],
        ]#Coded By @AgentsTeamking, Contact for support
        await callback_query.message.reply(
            "Custom farewell message has been set.",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        logger.info(f"Custom farewell message updated for channel {channel_id} by user {user_id}, copied message ID: {copied_msg_id}")
        await question.delete()
    except Exception as e:
        logger.error(f"Error during farewell message setup: {e}")
        await question.delete()
        await callback_query.message.reply(f"An error occurred: {e}")


@app.on_callback_query(subscribed & filters.regex("remfarewell"))
async def remove_custom_farewell_msg(bot, callback_query: CallbackQuery):
    try:
        _, channel_id = callback_query.data.split(":")
        channel_id = int(channel_id)
    except ValueError:
        await callback_query.answer("Invalid callback data format.", show_alert=True)
        return
#Coded By @AgentsTeamking, Contact for support
    user_id = callback_query.from_user.id
#Coded By @AgentsTeamking, Contact for support
    # Fetch the channel from the database
    channel = channels_collection.find_one({"user_id": user_id, "channel_id": channel_id})

    if not channel:
        await callback_query.answer("This channel is not configured for you.", show_alert=True)
        return

    # Check the current farewell message
    current_msg = channel.get("farewell_msg", DEFAULT_FAREWELL_MSG)
    if current_msg == DEFAULT_FAREWELL_MSG:
        await callback_query.answer("No custom farewell message is set.", show_alert=True)
        return

    # Reset the farewell message to the default
    channels_collection.update_one(
        {"channel_id": channel_id},
        {"$set": {"farewell_msg": DEFAULT_FAREWELL_MSG}}
    )

    await callback_query.answer("Custom farewell message removed.", show_alert=True)
#Coded By @AgentsTeamking, Contact for support
    approve_status = "✅ Enabled" if channel.get("approve_join", False) else "❌ Disabled"
    custom_welcome_status = "✅ Set" if channel.get("welcome_msg") != DEFAULT_WELCOME_MSG else "❌ Not Set"
    custom_farewell_status = "❌ Not Set"
    
    settings_msg = (
        f"Channel Configuration for {channel_id}:\n\n"
        f"Auto-Approve Join Requests: {approve_status}\n"
        f"Custom Welcome Message: {custom_welcome_status}\n"
        f"Custom Farewell Message: {custom_farewell_status}\n\n"
        "Choose an option to configure:"
    )
#Coded By @AgentsTeamking, Contact for support
    buttons = [
        [InlineKeyboardButton("Approve Join Request ✅" if channel.get("approve_join") else "Approve Join Request ❌", callback_data=f"approve:{channel_id}")],
        [InlineKeyboardButton("Set Custom Welcome Message ✨", callback_data=f"welcome:{channel_id}")],
        [InlineKeyboardButton("Remove Custom Welcome Message ❌", callback_data=f"remcustom:{channel_id}")],
        [InlineKeyboardButton("Set Custom Farewell Message ✨", callback_data=f"farewell:{channel_id}")],
        [InlineKeyboardButton("Remove Custom Farewell Message ❌", callback_data=f"remfarewell:{channel_id}")],
        [InlineKeyboardButton("Approve All Pending Requests 👥", callback_data="accept_all")],
        [InlineKeyboardButton("Remove Channel 🗑️", callback_data=f"remove:{channel_id}")],
        [InlineKeyboardButton("🏠 Main Menu", callback_data="start")]
    ]
    try:
        await callback_query.edit_message_text(settings_msg, reply_markup=InlineKeyboardMarkup(buttons))
    except Exception as e:
        await callback_query.answer(f"Error occurred: {e}", show_alert=True)

#Coded By @AgentsTeamking, Contact for support

# Handle "Approve Join Request" button click to toggle approval setting
@app.on_callback_query(subscribed & filters.regex("approve"))
async def toggle_approve_request(bot, callback_query: CallbackQuery):
    try:
        _, channel_id = callback_query.data.split(":")
        channel_id = int(channel_id)
    except ValueError:
        await callback_query.answer("Invalid callback data format.", show_alert=True)
        return

    user_id = callback_query.from_user.id

    channel = channels_collection.find_one({"user_id": user_id, "channel_id": channel_id})
    
    if not channel:
        await callback_query.answer("This channel is not configured for you.", show_alert=True)
        return
#Coded By @AgentsTeamking, Contact for support
    new_approve_status = not channel.get("approve_join", False)
    
    channels_collection.update_one(
        {"channel_id": channel_id},
        {"$set": {"approve_join": new_approve_status}}
    )

    approve_status = "✅ Enabled" if new_approve_status else "❌ Disabled"
    custom_welcome_status = "✅ Set" if channel.get("welcome_msg") != DEFAULT_WELCOME_MSG else "❌ Not Set"
    custom_farewell_status = "✅ Set" if channel.get("farewell_msg", DEFAULT_FAREWELL_MSG) != DEFAULT_FAREWELL_MSG else "❌ Not Set"

    settings_msg = (
        f"Channel Configuration for {channel_id}:\n\n"
        f"Auto-Approve Join Requests: {approve_status}\n"
        f"Custom Welcome Message: {custom_welcome_status}\n"
        f"Custom Farewell Message: {custom_farewell_status}\n\n"
        "Choose an option to configure:"
    )

    buttons = [
        [InlineKeyboardButton("Approve Join Request ✅" if new_approve_status else "Approve Join Request ❌", callback_data=f"approve:{channel_id}")],
        [InlineKeyboardButton("Set Custom Welcome Message ✨", callback_data=f"welcome:{channel_id}")],
        [InlineKeyboardButton("Remove Custom Welcome Message ❌", callback_data=f"remcustom:{channel_id}")],
        [InlineKeyboardButton("Set Custom Farewell Message ✨", callback_data=f"farewell:{channel_id}")],
        [InlineKeyboardButton("Remove Custom Farewell Message ❌", callback_data=f"remfarewell:{channel_id}")],
        [InlineKeyboardButton("Approve All Pending Requests 👥", callback_data="accept_all")],
        [InlineKeyboardButton("Remove Channel 🗑️", callback_data=f"remove:{channel_id}")],
        [InlineKeyboardButton("🏠 Main Menu", callback_data="start")]
    ]#Coded By @AgentsTeamking, Contact for support

    await callback_query.edit_message_text(settings_msg, reply_markup=InlineKeyboardMarkup(buttons))
    await callback_query.answer(f"Join request approval has been {'enabled' if new_approve_status else 'disabled'} for this channel.", show_alert=True)

# Callback for configuring a channel
@app.on_callback_query(subscribed & filters.regex("config"))
async def configure_channel(bot, callback_query: CallbackQuery):
    try:
        _, channel_id = callback_query.data.split(":")
        channel_id = int(channel_id)
    except ValueError:
        await callback_query.answer("Invalid callback data format.", show_alert=True)
        return
    #Coded By @AgentsTeamking, Contact for support
    user_id = callback_query.from_user.id

    # Check if the channel exists in MongoDB for the user
    channel = channels_collection.find_one({"user_id": user_id, "channel_id": channel_id})
    
    if not channel:
        await callback_query.answer("This channel is not configured for you.", show_alert=True)
        return

    # Show channel settings
    approve_status = "✅ Enabled" if channel.get("approve_join", False) else "❌ Disabled"
    custom_welcome_status = "✅ Set" if channel.get("welcome_msg") != DEFAULT_WELCOME_MSG else "❌ Not Set"
    custom_farewell_status = "✅ Set" if channel.get("farewell_msg", DEFAULT_FAREWELL_MSG) != DEFAULT_FAREWELL_MSG else "❌ Not Set"
    
    chat = await bot.get_chat(channel_id)
    channel_title = chat.title
    settings_msg = (
        f"Channel Configuration for {channel_title}:\n\n"
        f"Auto-Approve Join Requests: {approve_status}\n"
        f"Custom Welcome Message: {custom_welcome_status}\n"
        f"Custom Farewell Message: {custom_farewell_status}\n\n"
        "Choose an option to configure:"
    )
#Coded By @AgentsTeamking, Contact for support
    buttons = [
        [InlineKeyboardButton("Approve Join Request ✅", callback_data=f"approve:{channel_id}")],
        [InlineKeyboardButton("Set Custom Welcome Message ✨", callback_data=f"welcome:{channel_id}")],
        [InlineKeyboardButton("Remove Custom Welcome Message ❌", callback_data=f"remcustom:{channel_id}")],
        [InlineKeyboardButton("Set Custom Farewell Message ✨", callback_data=f"farewell:{channel_id}")],  # New button
        [InlineKeyboardButton("Remove Custom Farewell Message ❌", callback_data=f"remfarewell:{channel_id}")],  # New button
        [InlineKeyboardButton("Approve All Pending Requests 👥", callback_data="accept_all")],
        [InlineKeyboardButton("Remove Channel 🗑️", callback_data=f"remove:{channel_id}")],
        [InlineKeyboardButton("🏠 Main Menu", callback_data="start")]
    ]
    
    await callback_query.edit_message_text(settings_msg, reply_markup=InlineKeyboardMarkup(buttons))
#Coded By @AgentsTeamking, Contact for support
#-------------------------------------Approveall-----------------------------------------------
@app.on_callback_query(subscribed & filters.regex("accept_all"))
async def accept_all(bot, callback_query: CallbackQuery):
    await callback_query.answer("Coming Very Soon, Stay Updated...! ✅", show_alert=True)#Coded By @AgentsTeamking, Contact for support
#----------------------------------------------------------------------------------------------
# Handle "Remove Channel" button click to remove the channel
@app.on_callback_query(subscribed & filters.regex("remove"))
async def remove_channel(bot, callback_query: CallbackQuery):
    try:
        # Extract channel_id from the callback data
        _, channel_id = callback_query.data.split(":")
        channel_id = int(channel_id)
    except ValueError:
        await callback_query.answer("Invalid callback data format.", show_alert=True)
        return

    user_id = callback_query.from_user.id

    # Check if the channel exists in MongoDB for the user
    channel = channels_collection.find_one({"user_id": user_id, "channel_id": channel_id})
    if not channel:
        await callback_query.answer("This channel is not configured for you.", show_alert=True)
        return#Coded By @AgentsTeamking, Contact for support

    # Remove the channel from the user's configuration
    channels_collection.delete_one({"user_id": user_id, "channel_id": channel_id})

    # Attempt to fetch the channel's chat information
    try:
        chat = await bot.get_chat(channel_id)
        chat_title = chat.title if hasattr(chat, "title") else "No title available"
    except Exception as e:
        logger.error(f"Error fetching chat details for channel_id {channel_id}: {e}")
        chat_title = "Unknown Channel"

    # Check and delete from groups_only and channels_only collections
    group_result = groups.delete_one({"chat_id": channel_id})
    channel_result = channels.delete_one({"chat_id": channel_id})
#Coded By @AgentsTeamking, Contact for support
    if group_result.deleted_count > 0:
        logger.info(f"channel_id {channel_id} removed from groups_only collection.")
    elif channel_result.deleted_count > 0:
        logger.info(f"channel_id {channel_id} removed from channels_only collection.")
    else:
        logger.warning(f"channel_id {channel_id} not found in groups_only or channels_only collections.")

    # Notify the user that the channel has been removed
    
    await callback_query.answer(f"{chat_title} has been removed from your list.", show_alert=True)

    # Send a confirmation message
    buttons = [
        [InlineKeyboardButton("📂 My Channels", callback_data="my_channels")],
        [InlineKeyboardButton("🏠 Main Menu", callback_data="start")]
    ]#Coded By @AgentsTeamking, Contact for support
    await callback_query.message.edit_text(
        f"{chat_title} has been successfully removed from your list.",
        reply_markup=InlineKeyboardMarkup(buttons)
    )
    try:
        await bot.leave_chat(channel_id)
    except Exception as e:
        logger.error(f"Error leaving chat details for channel_id {channel_id}: {e}")
        pass

    # Update the user's channel list
    #await my_channels_callback(bot, callback_query)  # Refresh the list of channels for the user
#Coded By @AgentsTeamking, Contact for support
@app.on_message(filters.service)
async def anything(_, m):
    #print(m)
    if str(m.service) == "MessageServiceType.REQUESTED_CHAT":
        if m.requested_chats.chats:
            print(m.requested_chats)
            requested_chat = m.requested_chats.chats[0] 
            chat_id = requested_chat.id 
            chat = await _.get_chat(chat_id)
            chat_title = chat.title if hasattr(chat, 'title') else 'No title available'
            user_id = m.from_user.id  
            channel_id = chat.id
            print(f"Added to: {channel_id}, By: {user_id}, Title: {chat_title}")
            existing_channel = channels_collection.find_one({"channel_id": channel_id})
            buttons = [
                [InlineKeyboardButton("⚒️ Configure", callback_data=f"config:{chat_id}")],
                [InlineKeyboardButton("🏠 Main Menu", callback_data="start")]
            ]
      #Coded By @AgentsTeamking, Contact for support      
            if chat.type == ChatType.SUPERGROUP or chat.type == ChatType.GROUP:
                print("trying groups")
                if not groups.find_one({"chat_id": chat.id}):
                    groups.insert_one({"chat_id": chat.id})
                    print(f"Group/Supergroup with chat_id {chat.id} added to the groups collection.")
                    try:
                        await app.send_message(
                            chat_id=LOG_ID,
                            text=f"New Group\n\n"
                                 f"Chat: {chat_title}\n"
                                 f"Chat Username: @{chat.username if chat.username else 'No Username'}\n"
                                 f"Chat Id: {chat.id}\n"
                                 f"Members Count: {await app.get_chat_members_count(chat.id)}\n"
                                 f"⚒️ Bot Dev: @AgentsTeamking"
                        )#Coded By @AgentsTeamking, Contact for support  
                    except Exception as e:
                        await app.send_message(
                            chat_id=LOG_ID,
                            text=f"{e}")
                        pass
            elif chat.type == ChatType.CHANNEL:
                print("trying channels")
                if not channels.find_one({"chat_id": chat.id}):
                    channels.insert_one({"chat_id": chat.id})
                    print(f"Channel with chat_id {chat.id} added to the channels collection.")
                    try:#Coded By @AgentsTeamking, Contact for support
                        await app.send_message(
                            chat_id=LOG_ID,
                            text=f"New Channel\n\n"
                                 f"Chat: {chat_title}\n"
                                 f"Chat Username: @{chat.username if chat.username else 'No Username'}\n"
                                 f"Chat Id: {chat.id}\n"
                                 f"Members Count: {await app.get_chat_members_count(chat.id)}\n"
                                 f"⚒️ Bot Dev: @AgentsTeamking"
                        )
                    except Exception as e:
                        await app.send_message(
                            chat_id=LOG_ID,
                            text=f"{e}")
                        pass
#Coded By @AgentsTeamking, Contact for support
            if existing_channel:
                print("existing_channel")
                alrtext = f"{chat_title} Already added in db!"
                await m.reply_text(alrtext, reply_markup=InlineKeyboardMarkup(buttons))
                return
            channels_collection.insert_one({
                "user_id": user_id,
                "channel_id": chat_id, 
                "approve_join": False,
                "welcome_msg": DEFAULT_WELCOME_MSG,
                "farewell_msg": DEFAULT_FAREWELL_MSG  # Add default farewell message
            })#Coded By @AgentsTeamking, Contact for support
            print("inserted in channels_collection")
            config_msg = f"Bot added to {chat_title}!"
            await m.reply_text(config_msg, reply_markup=InlineKeyboardMarkup(buttons))
        else:
            print(f"Error")
    #elif str(m.service) == "MessageServiceType.LEFT_CHAT_MEMBERS":
        #user_id = m.left_chat_member.id
        #await app.send_message(text=f"GoodBye", chat_id=user_id)
    else:
        print("Nothing Bro")

@app.on_chat_member_updated()
async def tedjdjdjdjst(app, m):
    if m.old_chat_member and not m.new_chat_member:  # User left the chat
        user_id = m.old_chat_member.user.id
        channel_id = m.chat.id
        #Coded By @AgentsTeamking, Contact for support
        # Fetch channel configuration
        channel = channels_collection.find_one({"channel_id": channel_id})
        if channel:
            farewell_msg = channel.get("farewell_msg", DEFAULT_FAREWELL_MSG)
            try:
                farewell = await app.get_messages(welcome_channel_id, int(farewell_msg))
                await farewell.copy(user_id)
                logger.info(f"Sent farewell message to {user_id} from channel {channel_id}")
            except Exception as e:
                logger.error(f"Failed to send farewell message to {user_id}: {e}")
                await app.send_message(user_id, "Goodbye! Join @autojoinrequestuse")
        else:
            try:
                await app.send_message(user_id, "Goodbye! Join @autojoinrequestuse")
            except Exception:
                pass
    elif m.new_chat_member:  # User joined the chat (no change needed here)
        pass
    else:
        pass
#Coded By @AgentsTeamking, Contact for support
@app.on_message(filters.command("stats") & filters.user(OWNER_ID))
async def dbtool(app, m: Message):
    user_count = all_users()
    group_count = all_groups()
    channels_count = all_channels()
    total_count = group_count + channels_count 
    await m.reply_text(
        text=(
            f"Stats for {app.me.mention}\n"
            f"🙋‍♂️ Users: {user_count}\n"
            f"👥 Groups: {group_count}\n"
            f"📣 Channels: {channels_count}\n"
            f"📊 Total: {total_count}"
        )
    )
#Coded By @AgentsTeamking, Contact for support

@app.on_message(filters.command("fastcast") & filters.user(OWNER_ID))
async def fastcast(_, m: Message):
    allusers = users
    lel = await m.reply_text("⚡️ Processing...")
    total_users = allusers.count_documents({})  # Get total number of users
    success = 0
    failed = 0
    deactivated = 0
    blocked = 0
    peer = 0
    tasks = []
    progress_report_threshold = 2000  # Set threshold to 1000 successful broadcasts
    start_time = time()
#Coded By @AgentsTeamking, Contact for support
    async def send_message(userid):
        nonlocal success, failed, deactivated, blocked, peer
        try:
            await m.reply_to_message.copy(int(userid))
            success += 1
            # Check if 1000 successful messages have been sent and report progress
            if success % progress_report_threshold == 0:
                await app.send_message(OWNER_ID, f"🎉 {success}/{total_users} completed!")
        except FloodWait as ex:
            await asyncio.sleep(ex.value)
            await send_message(userid)  # Retry after sleeping
        except InputUserDeactivated:
            deactivated += 1
            remove_user(userid)
        except UserIsBlocked:
            blocked += 1
        except PeerIdInvalid:
            peer += 1
            remove_user(userid)
        except Exception as e:
            print(e)
            failed += 1
#Coded By @AgentsTeamking, Contact for support
    # Process in batches to avoid rate limits
    batch_size = 28  # Adjust this to Telegram's 30 messages/second limit
    for usrs in allusers.find():
        userid = usrs["user_id"]
        tasks.append(send_message(userid))

        if len(tasks) == batch_size:
            await asyncio.gather(*tasks)
            tasks.clear()
            await asyncio.sleep(1)  # 1 second delay between batches
#Coded By @AgentsTeamking, Contact for support
    if tasks:
        await asyncio.gather(*tasks)

    end_time = time()
    elapsed_time = end_time - start_time

    # Calculate hours, minutes, and seconds
    hours, remainder = divmod(elapsed_time, 3600)  # Convert to hours and remainder
    minutes, seconds = divmod(remainder, 60)       # Convert remainder to minutes and seconds
#Coded By @AgentsTeamking, Contact for support
    # Create time string based on the duration
    if hours > 0:
        time_str = f"{int(hours)} hr, {int(minutes)} m, and {int(seconds)} s."
    elif minutes > 0:
        time_str = f"{int(minutes)} m and {int(seconds)} s."
    else:
        time_str = f"{int(seconds)} s."

    await lel.edit(
        f"✅ Successful to `{success}` users.\n"
        f"❌ Failed to `{failed}` users.\n"
        f"👾 Blocked by `{blocked}` users.\n"
        f"👻 Deactivated accounts `{deactivated}`.\n"
        f"⚠️ Invalid Peer IDs `{peer}`.\n"
        f"⏱ Completed in {time_str}"
    )
#Coded By @AgentsTeamking, Contact for support

@app.on_callback_query(filters.regex("start|help|settings|remove|config|approve|remcustom|accept_all|welcome|my_channels|farewell|remfarewell"))
async def handle_multiple_regex_callbacks(client: Client, callback_query: CallbackQuery):
    try:
        effect_ids = [5104841245755180586, 5046509860389126442, 5159385139981059251]
        selected_effect_id = random.choice(effect_ids)
        reply_markup = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Join Now", url="https://t.me/autojoinrequestuse"),
                InlineKeyboardButton("Joined ✅", url=f"https://t.me/{(await client.get_me()).username}?start=im_piro")
            ],
            [
                InlineKeyboardButton(f"Join Updates Channel", url=f"https://t.me/+8Hgte7sPT8c5NTY1")
            ]
        ])
        await callback_query.edit_message_text(
            "**You must join [Channel](https://t.me/autojoinrequestuse) to use me.**",
            reply_markup=reply_markup, disable_web_page_preview = True
        )
    except Exception as e:
        await client.send_message(
            chat_id=OWNER_ID,
            text=f"Error while handling callback query:\n{e}"
        )
#Coded By @AgentsTeamking, Contact for support
if __name__ == "__main__":
    logger.info("Bot is started.. Coded By @AgentsTeamking, Contact for support.") 
    app.run()  
    logger.info("Bot has stopped. Coded By @AgentsTeamking, Contact for support") 
