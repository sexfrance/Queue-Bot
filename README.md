<!-- SPONSOR-START -->
---

<div align="center">

### 🌐 Need Proxies? Check out my services

<a href="https://vaultproxies.com" target="_blank" rel="noopener noreferrer">
  <img src="https://i.imgur.com/TF165pP.gif" alt="VaultProxies">
</a>
<p></p>

<table>
  <tr>
    <th>Service</th>
    <th>Pricing</th>
    <th>Features</th>
  </tr>
  <tr>
    <td><b><a href="https://vaultproxies.com" target="_blank" rel="noopener noreferrer">🔮 VaultProxies</a></b></td>
    <td><code>$1.00/GB</code> residential</td>
    <td>Residential · IPv6 · Residential Unlimited · Datacenter</td>
  </tr>
  <tr>
    <td><b><a href="https://nullproxies.com" target="_blank" rel="noopener noreferrer">🌑 NullProxies</a></b></td>
    <td><code>$0.75/GB</code> residential</td>
    <td>Residential · Residential Unlimited · DC Unlimited · Mobile Proxies</td>
  </tr>
  <tr>
    <td><b><a href="https://strikeproxy.net" target="_blank" rel="noopener noreferrer">⚡ StrikeProxy</a></b></td>
    <td><code>$0.75/GB</code> residential</td>
    <td>Residential · Residential Unlimited · DC Unlimited · Mobile Proxies</td>
  </tr>
</table>
</div>

<!-- SPONSOR-END -->

<div align="center">
 
  <h2 align="center">Discord - Queue Bot</h2>
  <p align="center">
    Discord Queue bot used to handle your discord orders! Every 10 seconds it will scan your sellix orders for a "sellix service order", you can of course easily change that. It will then save the orders into json and when someone presses the redeem button there will be an input asking for orderid then it will add the user to the queue! The bot is adapted for my server but you can rebrand it easily. It also dms the owner of the bot when a new user redeems an order and has been added to the queue!
    <br />
    <br />
    <a href="https://discord.cyberious.xyz">💬 Discord</a>
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
- Creates vouch messages
- Can dm the user with his product (file/text)
- Dms owner when new order gets redeemed
- More to discover!
-  ℹ️  `.help` - List all available commands
- 📨 `.message` - Send a message with a redeem button
- 🗑️ `.dele <order_id>` - Remove an order from the queue
- 🔑 `.add <order_id> <product> <quantity> <user>` - Manually add an order to the queue
- ⏳ `.pend <order_id>` - Marks an order as pending
- 🔍 `.deliver <order_id>` - Marks an order as delivered
- 🧹 `.purge` - Delete all messages sent by the bot in the queue channel
- 🔧 `.set <setting> <value>` - Set various bot configurations. Use `.set help` for details.
- 🔎 `.check /(user_ping)/(orderid)` - Shows all pending orders in the Queue, can also check pending order for a user/orderid
- ⚙️ `.restart` - Restarts the bot
---
#### 📹 Preview

![Queue Bot Help Command](https://i.imgur.com/FD6djpT.png) ![Queue Bot Queue System](https://i.imgur.com/uJk313w.png) ![Queue Bot DM](https://i.imgur.com/dE6Dhp9.png)

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

v0.0.4 ⋮ 07/27/2024
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

v0.1.0 ⋮ 08/10/2024
! Added: .set command to update bot configurations directly from Discord.
! Added: .set help command to display available settings and usage instructions.
! Added: Role assignment functionality for redeemed, delivered, and deleted events.
! Added: Optional role removal functionality when an order is redeemed.
! Updated: Help command to include .set command details.
! Removed: .set_queue command, now part of the .set command.
! Fixed: Error handling for invalid settings or values in the .set command
```

---

<p align="center">
  <img src="https://img.shields.io/github/license/sexfrance/Queue-Bot.svg?style=for-the-badge&labelColor=black&color=f429ff&logo=IOTA"/>
  <img src="https://img.shields.io/github/stars/sexfrance/Queue-Bot.svg?style=for-the-badge&labelColor=black&color=f429ff&logo=IOTA"/>
  <img src="https://img.shields.io/github/languages/top/sexfrance/Queue-Bot.svg?style=for-the-badge&labelColor=black&color=f429ff&logo=python"/>
</p>
