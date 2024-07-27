<div align="center">
 
  <h2 align="center">Discord - Queue Bot</h2>
  <p align="center">
    Discord Queue bot used to handle your discord orders! Every 15 seconds it will scan your sellix orders for a "sellix service order", you can of course easily change that. It will then save the orders into json and when someone presses the redeem button there will be an input asking for orderid then it will add the user to the queue! The bot is adapted for my server but you can rebrand it easily. It also dms the owner of the bot when a new user redeems an order and has been added to the queue!
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
- 🔎 `.check /(user_ping)/(orderid)` - Shows all pending orders in the Queue, can also check pending order for a user/orderid
- ⚙️ `.restart` - Restarts the bot
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
v0.0.1 ⋮ 07/20/2024
! Initial release

v0.0.3 ⋮ 07/23/2024
! Made branding easier by adding a custom embed color directly into config.json with formatter in case of misuse. Improved .deliver command to also dm the user once the product has been delivered, made it so that it works with a str/int e.g. .deliver order-123 hi@gmail.com, with a file: e.g. .deliver order-123 product.txt (must be an attachment) or without anything e.g. .deliver order-123

v0.1.0 ⋮ 07/27/2024
! Efficiency: Reduced Sellix order checking interval from 15 to 10 seconds.
! Restart Command: Added `.restart` command for programmatic bot restarts.
! Check Command Improved to handle user-specific or order ID queries, displaying detailed pending orders.
! Deliver Command Added user ping handling if user ID is missing, and fallback for total prices.
! Embed Creation Standardized with dynamic footer text and image URL integration.
! Error Handling Enhanced error messages and user prompts.
! Helper Functions Updated format color function and ensured old unclaimed orders deletion at startup.
! Admin Checks Simplified predicate function for admin/owner command execution.
! Help Command Updated to reflect new and modified commands.
! Bug Fixes Improved embed character limit handling and accurate claimed orders management.
```

---

<p align="center">
  <img src="https://img.shields.io/github/license/sexfrance/Queue-Bot.svg?style=for-the-badge&labelColor=black&color=f429ff&logo=IOTA"/>
  <img src="https://img.shields.io/github/stars/sexfrance/Queue-Bot.svg?style=for-the-badge&labelColor=black&color=f429ff&logo=IOTA"/>
  <img src="https://img.shields.io/github/languages/top/sexfrance/Queue-Bot.svg?style=for-the-badge&labelColor=black&color=f429ff&logo=python"/>
</p>
