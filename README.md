# 🤖 Custom Discord Bot
A powerful, multipurpose Discord bot built using `discord.py`. Packed with moderation tools, self-role support, XP system, anonymous systems, and utility commands — all controlled with a simple prefix.

---

## ✨ Features

- ⚒️ Moderation: Ban, Kick, Mute, Warn, Unwarn
- 📊 XP System: Add XP, Reset XP, Leaderboard support
- 📢 Instagram Notification System
- 🔧 Utility Commands: Ping, About Owner, Rules
- 📚 Self Roles & Role Embeds
- 💬 Fully customizable and easy to expand
- 📩 Ban appeal system with tickets & transcripts
- 🎉 Booster detection
- 🛡️ Custom auto mod with link filtering and role restrictions
---

## 🛠️ Setup Instructions

Follow these steps to run the bot on your own machine:

### 1. 📦 Clone the Repository

```bash
git clone https://github.com/SwastikKaushal1/Custom-Discord-Bot.git
cd Custom-Discord-Bot
```

### 2. 📥 Install Requirements

Make sure you have Python installed (3.10+ recommended).

Install dependencies:

```bash
pip install -r requirements.txt
```

### 3. 🧾 Configuration

Open the bot file (e.g., `MAIN_BOT.py`) and scroll to the config section.

You MUST fill out all the following variables with values from your server:

```python
# 🔧 Configuration — Fill These Out
GUILD_ID = 123456789  # Main Server ID
APPEAL_SERVER_ID = 123456789  # Appeal Server ID
ADMIN_LOG_CHANNEL_ID = 123456789  # Admin Logs Channel
TRANSCRIPT_CHANNEL_ID = 123456789  # Ban Ticket Transcript Channel
APPEAL_CATEGORY_ID = 123456789  # Ticket category (Appeal Server)
MAIN_TICKET_CATEGORY_ID = 123456789  # Ticket category (Main Server)
APPEAL_SERVER_INVITE = "https://discord.gg/your-invite"
MAINSERVER = "https://discord.gg/main-server"

# ⚙️ Role & Channel IDs
IGNORED_ROLES = {role_id1, role_id2}  # Roles ignored by auto mod
BLOCKED_LINK_CHANNELS = {channel_id1, channel_id2}  # Link-blocked channels
MODERATOR_ROLES = {mod_role1, mod_role2}  # Moderator role IDs
INSTA_NOTI_CHANNEL_ID = 123456789  # Instagram notifications
BOOST_CHANNEL_ID = 123456789  # Boost shoutout channel
BOOSTER_ROLE_ID = 123456789  # Booster role ID
NO_XP_ROLE_ID = 123456789  # Role that disables XP gain
BOT_COMMAND_ID = 123456789  # Level-up message channel
setup_channel_id = 123456789  # Appeal setup channel (buttons)
welcome_channel = 123456789  # Welcome channel ID
SERVER_NAME = "Your Server Name"

# 🏷️ Required Roles
Banned_role = 123456789  # Role given to banned users
Appeal_role = 123456789  # Role given while appealing
```

> 💡 Tip: Use Developer Mode in Discord to get IDs.

---

## 💡 Usage

Run the bot using:

```bash
python MAIN_BOT.py
```

Make sure your bot is invited to both the main server and appeal server with necessary permissions (manage roles, manage channels, read message history, etc.).

---

## 💬 Commands

| Command       | Description                    |
|---------------|--------------------------------|
| `?helpadmin`  | 👑 Shows all admin commands     |
| `?helpmod`    | 🛠️ Shows all moderator commands |

---

## 🧠 Notes

- Make sure all role and channel IDs exist on your server.
- Don’t forget to create the `banned` and `appeal is open` roles.
- You must invite the bot with **message content** intent enabled.
- Ban appeal tickets are handled in the appeal server via buttons.

---

## 🧊 Credits

Made with ❤️ by [SwastikKaushal](https://github.com/SwastikKaushal1)  
Discord: `swastik.op`

---

## 🖼️ Screenshots or GIFs (Optional)

You can add GIFs or screenshots like this:

```markdown
![Bot Example](https://your-image-link)
```

---

Need me to plug in your actual server name/links or customize anything else? Just drop it here 💬
```
