import discord
from discord.ext import commands, tasks
import json
import os
import requests
from datetime import datetime, timedelta
from discord.ui import Button, View
import sys
import asyncio


# Load configuration
def load_config():
    with open('config.json', 'r') as f:
        return json.load(f)

config = load_config()
file_path = __file__
file_name = os.path.basename(file_path)

# Bot setup
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='.', intents=intents, help_command=None)

# Helper functions
def load_json(file):
    if os.path.exists(file):
        with open(file, 'r') as f:
            return json.load(f)
    else:
        return {}

def save_json(file, data):
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)

# Formatting the EMBED_COLOR from config
def format_color(color):
    if color.startswith('#'):
        color = '0x' + color[1:]
    elif not color.startswith('0x'):
        color = '0x' + color
    return int(color, 16)

# Usage example
embed_color = format_color(config["EMBED_COLOR"])


def delete_old_unclaimed():
    now = datetime.now()
    for file in os.listdir(config['UNCLAIMED_FOLDER']):
        path = os.path.join(config['UNCLAIMED_FOLDER'], file)
        if os.path.isfile(path):
            creation_time = datetime.fromtimestamp(os.path.getctime(path))
            if now - creation_time > timedelta(weeks=1):
                os.remove(path)

def create_embed(title, description, color=embed_color):
    embed = discord.Embed(title=title, description=description, color=color)
    embed.set_thumbnail(url=config["THUMBNAIL_URL"])
    embed.set_footer(text=f"{config["FOOTER"]} • {datetime.now().strftime('%H:%M:%S')}", icon_url=config["THUMBNAIL_URL"])
    return embed

# Check admin or owner
def is_admin_or_owner():
    def predicate(ctx):
        return ctx.author.guild_permissions.administrator or ctx.author.id == config['OWNER_ID']
    return commands.check(predicate)

class OrderModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="Redeem Order")
        self.order_id = discord.ui.TextInput(label="Order ID", style=discord.TextStyle.short)
        self.add_item(self.order_id)

    async def on_submit(self, interaction):
        order_id = self.order_id.value
        unclaimed_path = os.path.join(config['UNCLAIMED_FOLDER'], f'{order_id}.json')

        if os.path.exists(unclaimed_path):
            with open(unclaimed_path, 'r') as f:
                order_data = json.load(f)

            if order_data.get('product_type') == 'SERVICE':
                claimed_data = load_json(config['CLAIMED_JSON'])
                claimed_data[order_id] = order_data
                save_json(config['CLAIMED_JSON'], claimed_data)
                os.remove(unclaimed_path)

                queue_embed = discord.Embed(
                    title="Queue System",
                    description=f"<:user:1263827156723826770>・__**Name**__ | <@{interaction.user.id}>\n<:world:1263827158397227061>・__**Product**__ | {order_data['product_title']}\n<:tool:1263827165737254933>・__**Quantity**__ | {order_data['quantity']}x\n<:check:1263827108581605427>・__**Status**__ | Pending",
                    color=embed_color
                )
                queue_embed.set_thumbnail(url=config["THUMBNAIL_URL"])
                queue_embed.set_footer(text=f"Order ID: {order_id}", icon_url=config["THUMBNAIL_URL"])
                queue_embed.set_image(url=config["IMAGE_URL"])

                channel = bot.get_channel(config['QUEUE_CHANNEL_ID'])
                if channel is not None:
                    message = await channel.send(embed=queue_embed)
                    claimed_data[order_id]['message_id'] = message.id
                    claimed_data[order_id]['channel_id'] = message.channel.id
                    save_json(config['CLAIMED_JSON'], claimed_data)

                    await interaction.response.send_message(embed=create_embed("Success", "Order has been successfully redeemed and added to the queue! Please be patient. You can also open a ticket in https://ptb.discord.com/channels/888116029803360317/1234847607684075542 for it to be delivered faster."), ephemeral=True)

                    owner = bot.get_user(config['OWNER_ID'])
                    if owner is not None:
                        dm_embed = discord.Embed(
                            title="New Pending Order",
                            description=f"A new order has been redeemed and is pending. Here are the details:",
                            color=embed_color
                        )
                        dm_embed.add_field(name="User", value=f"<@{interaction.user.id}>", inline=False)
                        dm_embed.add_field(name="Product", value=order_data['product_title'], inline=False)
                        dm_embed.add_field(name="Quantity", value=order_data['quantity'], inline=False)
                        dm_embed.add_field(name="Order ID", value=order_id, inline=False)
                        dm_embed.add_field(name="Status", value="Pending", inline=False)
                        dm_embed.set_thumbnail(url=config["THUMBNAIL_URL"])
                        dm_embed.set_footer(text=f"Order ID: {order_id}", icon_url=config["THUMBNAIL_URL"])
                        dm_embed.set_image(url=config["IMAGE_URL"])
                        await owner.send(embed=dm_embed)
                else:
                    await interaction.response.send_message(embed=create_embed(
                        "Error",
                        f"**Channel with ID {config['QUEUE_CHANNEL_ID']} not found or inaccessible.** "
                        "Please open a ticket in https://discord.com/channels/888116029803360317/1234847607684075542 and ask an admin to check the channel ID in the configuration and ensure the bot has access to the channel.",
                        discord.Color.red()
                    ), ephemeral=True)
            else:
                await interaction.response.send_message(embed=create_embed(
                    "Error",
                    "**The order is not redeemable**. Please ensure you have entered the correct order ID for a redeemable product. If you believe this is an error, open a ticket in https://ptb.discord.com/channels/888116029803360317/1234847607684075542 or make sure you didn't miss the product in your invoice.",
                    discord.Color.red()
                ), ephemeral=True)
        else:
            await interaction.response.send_message(embed=create_embed(
                "Error",
                "**Order ID not found**. Please ensure you have entered a valid order ID. If you believe this is an error, open a ticket in https://ptb.discord.com/channels/888116029803360317/1234847607684075542 and ping an admin.",
                discord.Color.red()
            ), ephemeral=True)

class RedeemView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(RedeemButton())

class RedeemButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="Redeem Order", emoji="🎟️", style=discord.ButtonStyle.primary, custom_id="redeem_button")

    async def callback(self, interaction: discord.Interaction):
        modal = OrderModal()
        await interaction.response.send_modal(modal)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    bot.add_view(RedeemView())  # Add the persistent view here
    await bot.wait_until_ready()  # Ensure the bot is fully ready
    check_sellix_orders.start()
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Game(config["BOT_STATUS"]))

# Task to check for new Sellix orders
@tasks.loop(seconds=10)
async def check_sellix_orders():
    headers = {
        'Authorization': f'Bearer {config["SELLIX_API_KEY"]}',
        'Content-Type': 'application/json',
    }
    response = requests.get('https://dev.sellix.io/v1/orders', headers=headers)
    orders = response.json().get('data', {}).get('orders', [])

    claimed_orders = load_json(config['CLAIMED_JSON'])

    for order in orders:
        order_id = order['uniqid']
        unclaimed_path = os.path.join(config['UNCLAIMED_FOLDER'], f'{order_id}.json')

        # Check if the order is a Sellix Service product, has a status of "COMPLETED", and is not in claimed_orders
        if order.get('product_type') == 'SERVICE' and order.get('status') == 'COMPLETED' and order_id not in claimed_orders:
            if not os.path.exists(unclaimed_path):
                with open(unclaimed_path, 'w') as f:
                    json.dump(order, f, indent=4)

@bot.command()
@is_admin_or_owner()
async def message(ctx):
    embed = create_embed("Queue System", "Click the button below to redeem your order.")
    embed.set_image(url=config["IMAGE_URL"])

    view = RedeemView()  # Use the persistent view here
    message = await ctx.send(embed=embed, view=view)
    claimed_data = load_json(config['CLAIMED_JSON'])
    claimed_data[message.id] = {
        "product": None,
        "quantity": None,
        "user": None,
        "status": "Pending"
    }
    save_json(config['CLAIMED_JSON'], claimed_data)

@bot.command()
@is_admin_or_owner()
async def dele(ctx, order_id: str):
    claimed_data = load_json(config['CLAIMED_JSON'])
    if order_id in claimed_data:
        message_id = claimed_data[order_id]['message_id']
        channel_id = claimed_data[order_id]['channel_id']
        del claimed_data[order_id]
        save_json(config['CLAIMED_JSON'], claimed_data)
        channel = bot.get_channel(channel_id)
        message = await channel.fetch_message(message_id)
        await message.delete()
        await ctx.send(embed=create_embed("Order Removed", f"Order **{order_id}** has been removed from the queue."))
    else:
        await ctx.send(embed=create_embed("Error", f"Order **{order_id}** not found in the queue.", discord.Color.red()))

@bot.command()
@is_admin_or_owner()
async def add(ctx, order_id: str, product: str, quantity: int, user: discord.User):
    claimed_data = load_json(config['CLAIMED_JSON'])
    claimed_data[order_id] = {
        "product": product,
        "quantity": quantity,
        "user": user.id,
        "status": "Pending"
    }
    save_json(config['CLAIMED_JSON'], claimed_data)
    channel = bot.get_channel(config['QUEUE_CHANNEL_ID'])
    queue_embed = discord.Embed(
        title="Queue System",
        description=f"<:user:1263827156723826770>・__**Name**__ | <@{user.id}>\n<:world:1263827158397227061>・__**Product**__ | {product}\n<:tool:1263827165737254933>・__**Quantity**__ | {quantity}x\n<:check:1263827108581605427>・__**Status**__ | Pending",
        color=embed_color
    )
    queue_embed.set_thumbnail(url=config["THUMBNAIL_URL"])
    queue_embed.set_footer(text=f"Order ID: {order_id}", icon_url=config["THUMBNAIL_URL"])
    queue_embed.set_image(url=config["IMAGE_URL"])
    message = await channel.send(embed=queue_embed)
    claimed_data[order_id]['message_id'] = message.id
    claimed_data[order_id]['channel_id'] = message.channel.id
    save_json(config['CLAIMED_JSON'], claimed_data)

    owner = bot.get_user(config['OWNER_ID'])
    if owner is not None:
        dm_embed = discord.Embed(
            title="New Pending Order",
            description=f"A new order has been manually added and is pending. Here are the details:",
            color=embed_color
        )
        dm_embed.add_field(name="User", value=f"<@{user.id}>", inline=False)
        dm_embed.add_field(name="Product", value=product, inline=False)
        dm_embed.add_field(name="Quantity", value=quantity, inline=False)
        dm_embed.add_field(name="Order ID", value=order_id, inline=False)
        dm_embed.add_field(name="Status", value="Pending", inline=False)
        dm_embed.set_thumbnail(url=config["THUMBNAIL_URL"])
        dm_embed.set_footer(text=f"Order ID: {order_id}", icon_url=config["THUMBNAIL_URL"])
        dm_embed.set_image(url=config["IMAGE_URL"])
        await owner.send(embed=dm_embed)


@bot.command()
@is_admin_or_owner()
async def pend(ctx, order_id: str):
    claimed_data = load_json(config['CLAIMED_JSON'])
    if order_id in claimed_data:
        channel = bot.get_channel(claimed_data[order_id]['channel_id'])
        message = await channel.fetch_message(claimed_data[order_id]['message_id'])
        embed = message.embeds[0]
        embed.description = embed.description.replace("<:check:1263827108581605427>・__**Status**__ | Delivered", "<:check:1263827108581605427>・__**Status**__ | Pending")
        await message.edit(embed=embed)
        await ctx.send(embed=create_embed("Order Status Updated", f"Order **{order_id}** status has been updated to pending."))
    else:
        await ctx.send(embed=create_embed("Error", f"Order **{order_id}** not found in the queue.", discord.Color.red()))

@bot.command()
@is_admin_or_owner()
async def deliver(ctx, order_id: str, *args):
    claimed_data = load_json(config['CLAIMED_JSON'])
    if order_id in claimed_data:
        user_id = claimed_data[order_id].get('user', None)
        
        if not user_id:
            await ctx.send(embed=create_embed("Ping User Required", f"Please ping the user for order **{order_id}**."))
            
            def check(m):
                return m.author == ctx.author and m.mentions

            try:
                message = await bot.wait_for('message', check=check, timeout=60)
                user = message.mentions[0]
                user_id = user.id
                claimed_data[order_id]['user'] = user_id
                save_json(config['CLAIMED_JSON'], claimed_data)
            except asyncio.TimeoutError:
                await ctx.send(embed=create_embed("Error", "No user pinged within 60 seconds. Command cancelled.", discord.Color.red()))
                return
        else:
            user = await bot.fetch_user(user_id)
            if not user:
                await ctx.send(embed=create_embed("Error", f"User with ID {user_id} not found.", discord.Color.red()))
                return

        product = claimed_data[order_id]['product_title']
        quantity = claimed_data[order_id]['quantity']
        total_price = claimed_data[order_id].get('total', config['MIN_PRODUCT_PRICE'])  # Extract total price from the order data
        claimed_data[order_id]['status'] = "Delivered"
        save_json(config['CLAIMED_JSON'], claimed_data)

        channel = bot.get_channel(claimed_data[order_id]['channel_id'])
        message = await channel.fetch_message(claimed_data[order_id]['message_id'])
        embed = message.embeds[0]
        embed.description = embed.description.replace("<:check:1263827108581605427>・__**Status**__ | Pending", "<:check:1263827108581605427>・__**Status**__ | Delivered")
        await message.edit(embed=embed)

        # Create the embed in the style of the queue system
        dm_embed = discord.Embed(
            title="Order Delivered",
            description=(
                f"<:user:1263827156723826770>・__**Name**__ | <@{user_id}>\n"
                f"<:world:1263827158397227061>・__**Product**__ | {product}\n"
                f"<:tool:1263827165737254933>・__**Quantity**__ | {quantity}x\n"
                f"<:check:1263827108581605427>・__**Status**__ | Delivered"
            ),
            color=embed_color
        )
        dm_embed.set_thumbnail(url=config["THUMBNAIL_URL"])
        dm_embed.set_footer(text=f"Order ID: {order_id}", icon_url=config["THUMBNAIL_URL"])
        dm_embed.set_image(url=config["IMAGE_URL"])

        if ctx.message.attachments:
            file = ctx.message.attachments[0]
            dm_embed.add_field(name="", value="\n__**Please check the attachment below:__**", inline=False)
            await user.send(embed=dm_embed)
            await user.send(file=await file.to_file())
        elif args:
            product_str = " ".join(args)
            dm_embed.add_field(name="Please see the product details below:", value=f"```\n{product_str}\n```", inline=False)
            await user.send(embed=dm_embed)
        else:
            dm_embed.add_field(name="", value="\n**Please check your ticket or DMs.**", inline=False)
            await user.send(embed=dm_embed)

        await ctx.send(embed=create_embed("Order Status Updated", f"Order **{order_id}** status has been updated to delivered. A message has been sent to the user."))
        
        if total_price <= config['MIN_PRODUCT_PRICE']:
            total_price = config['MIN_PRODUCT_PRICE']

        # Create the vouch message embed
        vouch_message = f"+rep <@{config['OWNER_ID']}> {product} {quantity}x ${total_price}"
        vouch_embed = discord.Embed(
            title="Vouch Message",
            description="Please copy and paste the following vouch message in https://discord.com/channels/888116029803360317/1234847586679263323 :",
            color=embed_color
        )
        vouch_embed.add_field(name="Vouch Message", value=f"```\n{vouch_message}\n```", inline=False)
        vouch_embed.set_thumbnail(url=config["THUMBNAIL_URL"])
        vouch_embed.set_footer(text=f"Order ID: {order_id}", icon_url=config["THUMBNAIL_URL"])

        # Send the vouch message embed to the user
        await user.send(embed=vouch_embed)

    else:
        await ctx.send(embed=create_embed("Error", f"Order **{order_id}** not found in the queue.", discord.Color.red()))


@bot.command()
@is_admin_or_owner()
async def purge(ctx):
    channel = bot.get_channel(config['QUEUE_CHANNEL_ID'])
    if channel is not None:
        await ctx.send(embed=create_embed("Purging Messages", f"Purging all messages sent by the bot in channel <#{config['QUEUE_CHANNEL_ID']}>."))
        async for message in channel.history(limit=None):
            if message.author == bot.user:
                await message.delete()
        await ctx.send(embed=create_embed("Purge Complete", f"All messages sent by the bot in channel <#{config['QUEUE_CHANNEL_ID']}> have been deleted."))
    else:
        await ctx.send(embed=create_embed(
            "Error",
            f"**Channel with ID {config['QUEUE_CHANNEL_ID']} not found or inaccessible.** "
            "Please check the channel ID in the configuration and ensure the bot has access to the channel.",
            discord.Color.red()
        ))

@bot.command()
@is_admin_or_owner()
async def set_queue(ctx, channel_id: int):
    config['QUEUE_CHANNEL_ID'] = channel_id
    save_json('config.json', config)
    await ctx.send(embed=create_embed("Queue Channel Updated", f"The queue channel ID has been updated to <#{channel_id}>."))

# Help command
@bot.command()
@is_admin_or_owner()
async def help(ctx):
    embed = create_embed("Help", "List of commands and their usage")
    embed.add_field(name=".message", value="Send a message with a redeem button", inline=False)
    embed.add_field(name=".dele <order_id>", value="Remove an order from the queue", inline=False)
    embed.add_field(name=".add <order_id> <product> <quantity> <user>", value="Manually add an order to the queue", inline=False)
    embed.add_field(name=".pend <order_id>", value="Mark an order as pending", inline=False)
    embed.add_field(name=".deliver <order_id> (product/attachment)", value="Mark an order as delivered", inline=False)
    embed.add_field(name=".purge", value="Delete all messages sent by the bot in the queue channel", inline=False)
    embed.add_field(name=".set_queue <channel_id>", value="Set the queue channel ID", inline=False)
    embed.add_field(name=".check /(user_ping)/(orderid)", value="Shows all pending orders in the Queue, can also check pending order for a user/orderid", inline=False)
    embed.add_field(name=".restart ", value="Restarts the bot", inline=False)
    await ctx.send(embed=embed)


@bot.command()
@is_admin_or_owner()
async def restart(ctx):
    await ctx.send(embed=create_embed("Restarting", "The bot is restarting..."))
    # Stop the bot
    await bot.close()
    # Restart the bot using a system command
    os.execv(sys.executable, ['python'] + [file_name] + [sys.argv[0]])

@bot.command()
@is_admin_or_owner()
async def check(ctx, *, query=None):
    # Fetch the queue channel
    queue_channel_id = config["QUEUE_CHANNEL_ID"]
    queue_channel = bot.get_channel(queue_channel_id)
    if not queue_channel:
        await ctx.send(embed=create_embed("Error", "Queue channel not found."))
        return

    # Dictionary to store message statuses
    message_status = {}

    # Fetch the last 500 messages from the queue channel
    async for message in queue_channel.history(limit=500):
        if message.embeds:
            embed = message.embeds[0]
            footer_text = embed.footer.text
            order_id = footer_text.replace('Order ID: ', '').strip()
            message_status[order_id] = embed

    # Load claimed data from the JSON file
    claimed_data = load_json(config['CLAIMED_JSON'])

    # Extract detailed order information
    detailed_orders = {k: v for k, v in claimed_data.items() if isinstance(v, dict) and 'status' in v}
    # Dictionary to store pending orders
    pending_orders = {}
    for order_id, embed in message_status.items():
        description = embed.description
        if 'Pending' in description:
            pending_orders[order_id] = embed

    if query:
        if query in claimed_data:  # Check if query is an order ID
            if query in pending_orders:
                await ctx.send(embed=pending_orders[query])
            else:
                await ctx.send(embed=create_embed("Error", f"Order **{query}** not found in the queue.", discord.Color.red()))
        else:
            try:
                user = await commands.MemberConverter().convert(ctx, query)
                user_orders = [
                    order for order, data in detailed_orders.items()
                    if isinstance(data, dict)
                    and isinstance(data.get('custom_fields'), dict)
                    and data['custom_fields'].get('discord_id') == str(user.id)
                    and data.get('status', '').lower() == 'completed'
                ]
                

                if user_orders:
                    # Create embeds for user orders
                    embeds = []
                    current_embed = create_embed(f"Pending Orders for {user}", "")
                    
                    field_count = 0
                    current_embed_size = len(current_embed.title) + len(current_embed.description)

                    for order_id in user_orders:
                        embed = pending_orders.get(order_id)
                        if embed:
                            description = embed.description
                            # Parse the description for user, product, quantity, and status
                            user_line, product_line, quantity_line, status_line = description.split('\n')
                            user_mention = user_line.split('|')[1].strip()
                            product = product_line.split('|')[1].strip()
                            quantity = quantity_line.split('|')[1].strip()
                            status = status_line.split('|')[1].strip()

                            order_info = (
                                f"**<:user:1263827156723826770> Name**: {user_mention}\n"
                                f"**<:world:1263827158397227061> Product**: {product}\n"
                                f"**<:tool:1263827165737254933> Quantity**: {quantity}\n"
                                f"**<:check:1263827108581605427> Order ID**: {order_id}\n"
                                f"**<:check:1263827108581605427> Status**: {status}\n"
                            )

                            order_info_size = len(f"Order {order_id}") + len(order_info)

                            if field_count + 1 > 25 or current_embed_size + order_info_size > 6000:
                                embeds.append(current_embed)
                                current_embed = create_embed(f"Pending Orders for {user} (cont.)", "")
                                field_count = 0
                                current_embed_size = len(current_embed.title) + len(current_embed.description)

                            current_embed.add_field(name=f"Order {order_id}", value=order_info, inline=False)
                            current_embed.set_image(url=config["IMAGE_URL"])
                            field_count += 1
                            current_embed_size += order_info_size

                    if current_embed.fields:
                        embeds.append(current_embed)

                    for embed in embeds:
                        await ctx.send(embed=embed)
                else:
                    await ctx.send(embed=create_embed("Error", f"No pending orders found for {user}.", discord.Color.red()))
            except commands.BadArgument:
                await ctx.send(embed=create_embed("Error", "Invalid query. Please provide a valid order ID or user mention.", discord.Color.red()))
    else:
        # List all pending orders if no query is provided
        if pending_orders:
            embeds = []
            current_embed = create_embed("Pending Orders", "")
            field_count = 0
            current_embed_size = len(current_embed.title) + len(current_embed.description)

            for order_id, embed in pending_orders.items():
                description = embed.description
                user_line, product_line, quantity_line, status_line = description.split('\n')
                user_mention = user_line.split('|')[1].strip()
                product = product_line.split('|')[1].strip()
                quantity = quantity_line.split('|')[1].strip()
                status = status_line.split('|')[1].strip()

                order_info = (
                    f"**<:user:1263827156723826770> Name**: {user_mention}\n"
                    f"**<:world:1263827158397227061> Product**: {product}\n"
                    f"**<:tool:1263827165737254933> Quantity**: {quantity}\n"
                    f"**<:check:1263827108581605427> Order ID**: {order_id}\n"
                    f"**<:check:1263827108581605427> Status**: {status}\n"
                )

                order_info_size = len(f"Order {order_id}") + len(order_info)

                if field_count + 1 > 25 or current_embed_size + order_info_size > 6000:
                    embeds.append(current_embed)
                    current_embed = create_embed("Pending Orders (cont.)", "")
                    field_count = 0
                    current_embed_size = len(current_embed.title) + len(current_embed.description)

                current_embed.add_field(name=f"Order {order_id}", value=order_info, inline=False)
                field_count += 1
                current_embed_size += order_info_size

            if current_embed.fields:
                embeds.append(current_embed)

            for embed in embeds:
                await ctx.send(embed=embed)
        else:
            await ctx.send(embed=create_embed("Info", "No pending orders found."))


# Ensure the unclaimed orders folder exists
os.makedirs(config['UNCLAIMED_FOLDER'], exist_ok=True)
delete_old_unclaimed()

# Run the bot
bot.run(config['TOKEN'])
