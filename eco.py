import discord
from discord.ext import commands
from discord import app_commands
import sqlite3
import os
import random
from datetime import datetime, timedelta

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_path = os.path.join(os.getcwd(), "database", "economy.db")
        self.init_db()
        self.work_messages = [
            "You helped a local farmer and earned **{coins}** coins!",
            "You cleaned the streets and earned **{coins}** coins!",
            "You worked at a local cafe and earned **{coins}** coins!",
            "You sold lemonade and earned **{coins}** coins!",
            "You painted fences and earned **{coins}** coins!",
            "You did some odd jobs for neighbors and earned **{coins}** coins!",
            "You worked at a bookstore and earned **{coins}** coins!",
            "You helped a friend move and earned **{coins}** coins!",
            "You baked cookies for a local event and earned **{coins}** coins!",
            "You walked dogs for a neighbor and earned **{coins}** coins!",
            "You did some gardening and earned **{coins}** coins!",
            "You organized a local cleanup and earned **{coins}** coins!",
            "You babysat for a family and earned **{coins}** coins!",
            "You delivered newspapers and earned **{coins}** coins!",
            "You mowed lawns and earned **{coins}** coins!",
            "You did yard work and earned **{coins}** coins!",
            "You worked as a waiter and earned **{coins}** coins!",
            "You created an online course and earned **{coins}** coins from sign-ups!",
            "You organized a bake sale and earned **{coins}** coins!",
            "You gave a talk at a conference and earned **{coins}** coins!",
            "You helped a local artist and earned **{coins}** coins!",
            "You did a science experiment and earned **{coins}** coins for participation!",
            "You volunteered at a library and earned **{coins}** coins!",
            "You participated in a local festival and earned **{coins}** coins!",
            "You cleaned up a beach and earned **{coins}** coins!",
            "You organized a knitting circle and earned **{coins}** coins!",
            "You did some house sitting and earned **{coins}** coins!",
            "You worked at a garage sale and earned **{coins}** coins!",
            "You assisted at a community center and earned **{coins}** coins!",
            "You gave a music lesson and earned **{coins}** coins!",
            "You participated in a charity run and earned **{coins}** coins!",
            "You helped out at a pet shelter and earned **{coins}** coins!",
            "You took part in a dance recital and earned **{coins}** coins!",
            "You worked as a lifeguard and earned **{coins}** coins!",
            "You offered to tutor someone and earned **{coins}** coins!",
        ]
        self.beg_messages = [
            "You begged for coins and received **{coins}** coins!",
            "You asked a passerby for help and received **{coins}** coins!",
            "You pleaded with a stranger and they gave you **{coins}** coins!",
            "You showed your best puppy eyes and received **{coins}** coins!",
            "You told a touching story and earned **{coins}** coins!",
            "You performed a little dance and earned **{coins}** coins!",
            "You held a sign saying 'Will work for coins' and received **{coins}** coins!",
            "You did a magic trick and earned **{coins}** coins!",
            "You sang a song and people threw **{coins}** coins at you!",
            "You made a heartfelt plea and received **{coins}** coins!",
            "You shared a smile and earned **{coins}** coins!",
            "You offered to carry someone's bags and received **{coins}** coins!",
            "You tried your luck and received **{coins}** coins!",
            "You approached a group and shared your story, earning **{coins}** coins!",
            "You entertained some kids and they gave you **{coins}** coins!",
            "You showed off a trick and earned **{coins}** coins!",
            "You wore a funny hat and received **{coins}** coins!",
            "You held a guitar and strummed a tune, earning **{coins}** coins!",
            "You shared a joke and people laughed, giving you **{coins}** coins!",
            "You waved at people and received **{coins}** coins!",
            "You told a silly story and earned **{coins}** coins!",
            "You gave compliments and received **{coins}** coins in return!",
            "You offered to help someone and they gave you **{coins}** coins!",
            "You danced on the street and people donated **{coins}** coins!",
            "You performed an impression and earned **{coins}** coins!",
            "You painted a little picture and earned **{coins}** coins!",
            "You helped an elderly person cross the street and received **{coins}** coins!",
            "You shared a kind word and got rewarded with **{coins}** coins!",
            "You made origami and people gave you **{coins}** coins!",
            "You sold a flower you picked and received **{coins}** coins!",
            "You shared a dessert and earned **{coins}** coins!",
            "You made people laugh and they gave you **{coins}** coins!",
            "You picked up litter and received **{coins}** coins as thanks!",
            "You showed a cool trick and earned **{coins}** coins!",
            "You helped someone find their way and they rewarded you with **{coins}** coins!",
            "You participated in a group activity and earned **{coins}** coins!",
            "You shared a heartfelt moment and received **{coins}** coins!",
            "You offered a ride and received **{coins}** coins in thanks!",
            "You helped someone with their groceries and earned **{coins}** coins!",
            "You held a sign that said 'Need coins' and received **{coins}** coins!",
            "You offered to walk someone's pet and received **{coins}** coins!",
            "You tried to charm people and earned **{coins}** coins!",
            "You told people you're saving up for a special cause and received **{coins}** coins!",
            "You offered to help with a chore and earned **{coins}** coins!",
            "You wore a funny costume and people gave you **{coins}** coins!",
            "You made a little performance and earned **{coins}** coins!",
            "You approached a food truck and offered to help in exchange for **{coins}** coins!",
            "You made a sweet plea and earned **{coins}** coins!",
            "You juggled and earned **{coins}** coins!",
            "You participated in a scavenger hunt and found **{coins}** coins!",
            "You ran an impromptu quiz and earned **{coins}** coins!",
            "You shared a funny story and people laughed, giving you **{coins}** coins!",
            "You made a paper airplane and earned **{coins}** coins!",
            "You helped organize a neighborhood event and earned **{coins}** coins!",
            "You played a friendly game and received **{coins}** coins as a prize!",
            "You joined a community project and earned **{coins}** coins!",
            "You gave a high-five and received **{coins}** coins!",
            "You told people you love gardening and received **{coins}** coins!",
            "You made a sign saying 'Please help!' and received **{coins}** coins!",
            "You participated in a fun run and earned **{coins}** coins!",
            "You showed off your collection and earned **{coins}** coins!",
            "You offered to clean a park and earned **{coins}** coins!",
        ]

    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            user_id INTEGER PRIMARY KEY,
                            balance INTEGER DEFAULT 0,
                            bank_balance INTEGER DEFAULT 0,
                            last_daily DATETIME DEFAULT NULL,
                            last_work DATETIME DEFAULT NULL,
                            last_beg DATETIME DEFAULT NULL,
                            last_rob DATETIME DEFAULT NULL)''')  

        cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id INTEGER,
                            amount INTEGER,
                            description TEXT,
                            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY (user_id) REFERENCES users(user_id))''')

        conn.commit()
        conn.close()

    eco_group = app_commands.Group(name="eco", description="Economy commands")

    @eco_group.command(name="balance", description="Check your current balance.")
    async def balance(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        balance = self.get_balance(user_id)
        embed = discord.Embed(
            title="💰 Current Balance",
            description=f"{interaction.user.mention}, your current balance is **{balance}** coins.",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed)

    @eco_group.command(name="work", description="Earn currency through work.")
    async def work(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        now = discord.utils.utcnow()
        last_work_str = self.get_last_work(user_id)

        if last_work_str:
            last_work = datetime.fromisoformat(last_work_str)
        else:
            last_work = None

        if last_work and now < last_work + timedelta(hours=1):
            remaining_time = (last_work + timedelta(hours=1)) - now
            hours, remainder = divmod(int(remaining_time.total_seconds()), 3600)
            minutes, seconds = divmod(remainder, 60)
            time_left = f"{hours}h {minutes}m {seconds}s"
            embed = discord.Embed(
                title="⏰ Work Unavailable",
                description=f"{interaction.user.mention}, you need to wait **{time_left}** before you can work again.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed)
            return

        earnings = random.randint(50, 200) 
        work_message = random.choice(self.work_messages).format(coins=earnings)
        self.update_balance(user_id, earnings)
        self.set_last_work(user_id, now.isoformat()) 

        embed = discord.Embed(title="💼 Work Result", description=work_message, color=discord.Color.blue())
        await interaction.response.send_message(embed=embed)

    @eco_group.command(name="beg", description="Beg for currency.")
    async def beg(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        now = discord.utils.utcnow()
        last_beg_str = self.get_last_beg(user_id)

        if last_beg_str:
            last_beg = datetime.fromisoformat(last_beg_str)
        else:
            last_beg = None

        if last_beg and now < last_beg + timedelta(hours=1):
            remaining_time = (last_beg + timedelta(hours=1)) - now
            hours, remainder = divmod(int(remaining_time.total_seconds()), 3600)
            minutes, seconds = divmod(remainder, 60)
            time_left = f"{hours}h {minutes}m {seconds}s"
            embed = discord.Embed(
                title="⏰ Beg Unavailable",
                description=f"{interaction.user.mention}, you need to wait **{time_left}** before you can beg again.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed)
            return

        earnings = random.randint(10, 100)  
        beg_message = random.choice(self.beg_messages).format(coins=earnings)
        self.update_balance(user_id, earnings)
        self.set_last_beg(user_id, now.isoformat())  

        embed = discord.Embed(title="🙏 Beg Result", description=beg_message, color=discord.Color.blue())
        await interaction.response.send_message(embed=embed)

    @eco_group.command(name="daily", description="Claim your daily reward.")
    async def daily(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        now = discord.utils.utcnow()

        last_daily_str = self.get_last_daily(user_id)
        
        if last_daily_str:
            last_daily = datetime.fromisoformat(last_daily_str)
        else:
            last_daily = None

        if last_daily and now < last_daily + timedelta(days=1):
            embed = discord.Embed(
                title="⏰ Daily Reward Unavailable",
                description=f"{interaction.user.mention}, you can only claim your daily reward once every 24 hours. Please try again later!",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed)
            return

        daily_reward = random.randint(50, 150)
        self.update_balance(user_id, daily_reward)
        self.set_last_daily(user_id, now.isoformat())

        embed = discord.Embed(
            title="🎉 Daily Reward",
            description=f"{interaction.user.mention}, you claimed your daily reward of **{daily_reward}** coins!",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed)

    @eco_group.command(name="bankbalance", description="Check your bank balance.")
    async def bank_balance(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        bank_balance = self.get_bank_balance(user_id)
        embed = discord.Embed(
            title="🏦 Bank Balance",
            description=f"{interaction.user.mention}, your current bank balance is **{bank_balance}** coins.",
            color=discord.Color.blue()
        )
        await interaction.response.send_message(embed=embed)

    @eco_group.command(name="bankdeposit", description="Deposit coins into your bank.")
    @app_commands.describe(amount="Amount of coins to deposit")
    async def bank_deposit(self, interaction: discord.Interaction, amount: int):
        user_id = interaction.user.id
        balance = self.get_balance(user_id)

        if amount <= 0:
            await interaction.response.send_message("You cannot deposit zero or negative coins.", ephemeral=True)
            return

        if amount > balance:
            await interaction.response.send_message("You don't have enough coins to deposit that amount.", ephemeral=True)
            return

        self.update_balance(user_id, -amount) 
        self.update_bank_balance(user_id, amount) 

        embed = discord.Embed(
            title="🏦 Deposit Successful",
            description=f"{interaction.user.mention}, you have deposited **{amount}** coins into your bank!",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed)

    @eco_group.command(name="bankwithdraw", description="Withdraw coins from your bank.")
    @app_commands.describe(amount="Amount of coins to withdraw")
    async def bank_withdraw(self, interaction: discord.Interaction, amount: int):
        user_id = interaction.user.id
        bank_balance = self.get_bank_balance(user_id)

        if amount <= 0:
            await interaction.response.send_message("You cannot withdraw zero or negative coins.", ephemeral=True)
            return

        if amount > bank_balance:
            await interaction.response.send_message("You don't have enough coins in your bank to withdraw that amount.", ephemeral=True)
            return

        self.update_bank_balance(user_id, -amount) 
        self.update_balance(user_id, amount)

        embed = discord.Embed(
            title="🏦 Withdrawal Successful",
            description=f"{interaction.user.mention}, you have withdrawn **{amount}** coins from your bank!",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed)
    
    @eco_group.command(name="leaderboard", description="Show the top 10 users based on coin balance.")
    async def leaderboard(self, interaction: discord.Interaction):
        top_users = self.get_top_users()
        
        if not top_users:
            embed = discord.Embed(
                title="🏆 Leaderboard",
                description="No users found.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed)
            return

        description = ""
        for idx, (user_id, balance) in enumerate(top_users, start=1):
            user = self.bot.get_user(user_id)
            user_mention = user.mention if user else "Unknown User"
            description += f"{idx}. {user_mention} - **{balance}** coins\n"

        embed = discord.Embed(
            title="🏆 Leaderboard",
            description=description,
            color=discord.Color.gold()
        )
        embed.set_footer(text="Keep grinding to reach the top!")
        embed.timestamp = discord.utils.utcnow()
        
        await interaction.response.send_message(embed=embed)

    @eco_group.command(name="give", description="Give coins to another user.")
    @app_commands.describe(amount="Amount of coins to give", user="User to give coins to")
    async def give(self, interaction: discord.Interaction, amount: int, user: discord.User):
        sender_id = interaction.user.id
        receiver_id = user.id

        if amount <= 0:
            await interaction.response.send_message("You cannot give zero or negative coins.", ephemeral=True)
            return

        sender_balance = self.get_balance(sender_id)

        if amount > sender_balance:
            await interaction.response.send_message("You don't have enough coins to give that amount.", ephemeral=True)
            return

        self.update_balance(sender_id, -amount)
        self.update_balance(receiver_id, amount)

        embed = discord.Embed(
            title="💸 Transfer Successful",
            description=f"{interaction.user.mention} has given **{amount}** coins to {user.mention}!",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed)

    @eco_group.command(name="rob", description="Attempt to rob another user.")
    @app_commands.describe(user="User  to rob")
    async def rob(self, interaction: discord.Interaction, user: discord.User):
        robber_id = interaction.user.id
        target_id = user.id
        now = discord.utils.utcnow()
        if robber_id == target_id:
            await interaction.response.send_message("You cannot rob yourself!", ephemeral=True)
            return
        last_rob_str = self.get_last_rob(robber_id)
        if last_rob_str:
            last_rob = datetime.fromisoformat(last_rob_str)
        else:
            last_rob = None

        if last_rob and now < last_rob + timedelta(hours=3):
            remaining_time = (last_rob + timedelta(hours=3)) - now
            hours, remainder = divmod(int(remaining_time.total_seconds()), 3600)
            minutes, seconds = divmod(remainder, 60)
            time_left = f"{hours}h {minutes}m {seconds}s"
            embed = discord.Embed(
                title="⏰ Robbery Unavailable",
                description=f"{interaction.user.mention}, you need to wait **{time_left}** before you can attempt to rob again.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed)
            return
        target_balance = self.get_balance(target_id)

        if target_balance <= 0:
            await interaction.response.send_message(f"{user.mention} has no coins to rob!", ephemeral=True)
            return

        success_chance = random.randint(1, 100)
        success_threshold = 50 

        if success_chance <= success_threshold:
            rob_amount = min(target_balance, random.randint(1, target_balance))
            self.update_balance(robber_id, rob_amount)
            self.update_balance(target_id, -rob_amount)
            self.set_last_rob(robber_id, now.isoformat())

            embed = discord.Embed(
                title="💰 Robbery Successful!",
                description=f"{interaction.user.mention} successfully robbed **{rob_amount}** coins from {user.mention}!",
                color=discord.Color.green()
            )
        else:
            penalty_amount = random.randint(1, 10)
            self.update_balance(robber_id, -penalty_amount)
            
            embed = discord.Embed(
                title="🚫 Robbery Failed!",
                description=f"{interaction.user.mention} failed to rob {user.mention} and lost **{penalty_amount}** coins as a penalty!",
                color=discord.Color.red()
            )

        await interaction.response.send_message(embed=embed)

    @eco_group.command(name="bet", description="Gamble coins on a game of chance.")
    async def bet(self, interaction: discord.Interaction, amount: int):
        user_id = interaction.user.id
        current_balance = self.get_balance(user_id)

        if amount <= 0:
            await interaction.response.send_message("You must bet a positive amount.", ephemeral=True)
            return
        if amount > current_balance:
            await interaction.response.send_message("You don't have enough coins to make that bet.", ephemeral=True)
            return
        outcome = random.choice(["win", "lose"])
        if outcome == "win":
            winnings = amount * 2 
            self.update_balance(user_id, winnings)
            result_message = f"You won! You now have **{current_balance + winnings}** coins."
        else:
            self.update_balance(user_id, -amount) 
            result_message = f"You lost! You now have **{current_balance - amount}** coins."
        embed = discord.Embed(
            title="🎲 Bet Result",
            description=result_message,
            color=discord.Color.blue()
        )
        await interaction.response.send_message(embed=embed)


    def get_top_users(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT user_id, balance FROM users ORDER BY balance DESC LIMIT 10")
        top_users = cursor.fetchall()
        
        conn.close()
        return top_users

    def get_balance(self, user_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()

        if result is None:
            cursor.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
            conn.commit()
            return 0 
        else:
            return result[0]

    def update_balance(self, user_id, amount):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
        cursor.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?", (amount, user_id))

        cursor.execute("INSERT INTO transactions (user_id, amount, description) VALUES (?, ?, ?)",
                       (user_id, amount, "Earned from begging" if amount < 100 else "Earned from work"))

        conn.commit()
        conn.close()

    def get_bank_balance(self, user_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT bank_balance FROM users WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()

        if result is None:
            cursor.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
            conn.commit()
            return 0 
        else:
            return result[0]

    def update_bank_balance(self, user_id, amount):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
        cursor.execute("UPDATE users SET bank_balance = bank_balance + ? WHERE user_id = ?", (amount, user_id))

        conn.commit()
        conn.close()

    def set_last_daily(self, user_id, timestamp):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
        cursor.execute("UPDATE users SET last_daily = ? WHERE user_id = ?", (timestamp, user_id))

        conn.commit()
        conn.close()

    def get_last_daily(self, user_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT last_daily FROM users WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()

        if result:
            return result[0]
        return None

    def set_last_work(self, user_id, timestamp):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
        cursor.execute("UPDATE users SET last_work = ? WHERE user_id = ?", (timestamp, user_id))

        conn.commit()
        conn.close()

    def get_last_work(self, user_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT last_work FROM users WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()

        if result:
            return result[0]
        return None

    def set_last_beg(self, user_id, timestamp):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
        cursor.execute("UPDATE users SET last_beg = ? WHERE user_id = ?", (timestamp, user_id))

        conn.commit()
        conn.close()

    def get_last_beg(self, user_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT last_beg FROM users WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()

        if result:
            return result[0]
        return None
    
    def set_last_rob(self, user_id, timestamp):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
        cursor.execute("UPDATE users SET last_rob = ? WHERE user_id = ?", (timestamp, user_id))

        conn.commit()
        conn.close()

    def get_last_rob(self, user_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT last_rob FROM users WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()

        if result:
            return result[0]
        return None

    def reset_user_progress(self, user_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("UPDATE users SET balance = 0, bank_balance = 0, last_daily = NULL, last_work = NULL, last_beg = NULL, last_rob = NULL WHERE user_id = ?", (user_id,))
        conn.commit()
        conn.close()

class EcoAdmin(commands.Cog):
    def __init__(self, bot, economy):
        self.bot = bot
        self.economy = economy 
    eco_admin_group = app_commands.Group(name="ecoadmin", description="Admin commands for managing the economy.")

    @eco_admin_group.command(name="addcoin", description="Add coins to a user's balance.")
    @commands.has_permissions(administrator=True) 
    async def addcoin(self, interaction: discord.Interaction, user: discord.User, amount: int):
        if amount <= 0:
            await interaction.response.send_message("You must add a positive amount of coins.", ephemeral=True)
            return
        self.economy.update_balance(user.id, amount)
        await interaction.response.send_message(f"Added **{amount}** coins to {user.mention}'s balance.", ephemeral=True)
    @eco_admin_group.command(name="removecoin", description="Remove coins from a user's balance.")
    @commands.has_permissions(administrator=True)
    async def removecoin(self, interaction: discord.Interaction, user: discord.User, amount: int):
        if amount <= 0:
            await interaction.response.send_message("You must remove a positive amount of coins.", ephemeral=True)
            return
        self.economy.update_balance(user.id, -amount)
        await interaction.response.send_message(f"Removed **{amount}** coins from {user.mention}'s balance.", ephemeral=True)

    @eco_admin_group.command(name="reset", description="Reset all progress of a user.")
    @commands.has_permissions(administrator=True)
    async def reset(self, interaction: discord.Interaction, user: discord.User):
        self.economy.reset_user_progress(user.id)
        await interaction.response.send_message(f"Reset all progress for {user.mention}.", ephemeral=True)

    @eco_admin_group.command(name="viewbalance", description="View the balance of a user.")
    @commands.has_permissions(administrator=True) 
    async def viewbalance(self, interaction: discord.Interaction, user: discord.User):
        balance = self.economy.get_balance(user.id)
        await interaction.response.send_message(f"{user.mention} has **{balance}** coins.", ephemeral=True)

async def setup(bot):
    economy = Economy(bot)
    await bot.add_cog(economy)
    await bot.add_cog(EcoAdmin(bot, economy)) 