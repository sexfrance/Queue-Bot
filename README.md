<div align="center">
 
  <h2 align="center">Discord - Queue Bot</h2>
  <p align="center">
    Discord Queue bot used to handle your discord orders! Every 15 seconds it will scan your sellix orders for a "sellix service order", you can of course easily change that. It will then save the orders into json and when someone presses the redeem button there will be an input asking for orderid then it will add the user to the queue! The bot is adapted for my server but you can rebrand it easily
    <br />
    <br />
    <a href="https://discord.gg/bestnitro">💬 Discord</a>
    ·
    <a href="https://github.com/sexfrance/Queue-Bot#-changelog">📜 ChangeLog</a>
    ·
    <a href="https://github.com/sexfrance/Queue-Bot/issues">⚠️ Report Bug</a>
    ·
    <a href="https://github.com/sexfrance/Queue-Bot/issues">💡 Request Feature</a>
  </p>
</div>

### ⚙️ Installation

- Requires: `Python 3.10+`
- Make a python virtual environment: `python3 -m venv venv`
- Source the environment: `venv\Scripts\activate` (Windows) / `source venv/bin/activate` (macOS, Linux)
- Install the requirements: `pip install -r requirements.txt`
- Start: `python3 main.py`

---

### 🔥 Features
- Nice Embeds
- Improved Logging
- Easy rebrand
- Dms user when new order gets redeemed
-  ℹ️  `.help` - List all available commands
- 📨 `.message` - Send a message with a redeem button
- 🗑️ `.dele <order_id>` - Remove an order from the queue
- 🔑 `.add <order_id> <product> <quantity> <user>` - Manually add an order to the queue
- ⏳ `.pend <order_id>` - Marks an order as pending
- 🔍 `.deliver <order_id>` - Marks an order as delivered
- 🧹 `.purge` - Delete all messages sent by the bot in the queue channel
- 🔧 `.set_queue <channel_id>` - Set the queue channel ID without accessing config.json

---
#### 📹 Preview

![Queue Bot Help Command](https://i.imgur.com/KnpXXTx.png) ![Queue Bot Queue System](https://i.imgur.com/jSW9edH.png) ![Queue Bot DM](https://i.imgur.com/dE6Dhp9.png)

---
### ❗ Disclaimers

- I am not responsible for anything that may happen, such as API Blocking, Account Termination, etc.
- This was a quick project that was made for fun and personal use if you want to see further updates, star the repo & create an "issue" [here](https://github.com/sexfrance/Queue-Bot/issues/)

---

### 📜 ChangeLog

```diff
v0.0.1 ⋮ 8/6/2024
! Initial release
```

---

<p align="center">
  <img src="https://img.shields.io/github/license/sexfrance/Queue-Bot.svg?style=for-the-badge&labelColor=black&color=f429ff&logo=IOTA"/>
  <img src="https://img.shields.io/github/stars/sexfrance/Queue-Bot.svg?style=for-the-badge&labelColor=black&color=f429ff&logo=IOTA"/>
  <img src="https://img.shields.io/github/languages/top/sexfrance/Queue-Bot.svg?style=for-the-badge&labelColor=black&color=f429ff&logo=python"/>
</p>
