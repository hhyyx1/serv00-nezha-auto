import os
import json
import subprocess
import requests

def send_telegram_message(token, chat_id, message):
    if not token or not chat_id:
        print("Telegram token 或 chat_id 未配置")
        return

    telegram_url = f"https://api.telegram.org/bot{token}/sendMessage"
    telegram_payload = {
        "chat_id": chat_id,
        "text": message,
        "reply_markup": '{"inline_keyboard":[[{"text":"问题反馈❓","url":"https://t.me/yxjsjl"}]]}'
    }

    response = requests.post(telegram_url, json=telegram_payload)
    print(f"Telegram 请求状态码：{response.status_code}")
    print(f"Telegram 请求返回内容：{response.text}")

    if response.status_code != 200:
        print("发送 Telegram 消息失败")
    else:
        print("发送 Telegram 消息成功")

# 从环境变量中获取密钥
accounts_json = os.getenv('ACCOUNTS_JSON')
telegram_token = os.getenv('TELEGRAM_TOKEN')
telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')

# 打印环境变量以调试
print(f"ACCOUNTS_JSON: {accounts_json}")
print(f"TELEGRAM_TOKEN: {telegram_token}")
print(f"TELEGRAM_CHAT_ID: {telegram_chat_id}")

# 检查并解析 JSON 字符串
try:
    servers = json.loads(accounts_json)
except json.JSONDecodeError:
    error_message = "ACCOUNTS_JSON 参数格式错误"
    print(error_message)
    send_telegram_message(telegram_token, telegram_chat_id, error_message)
    exit(1)

# 初始化汇总消息
summary_message = "哪吒面板恢复操作结果：\n"

# 默认恢复命令
default_restore_command = "cd ~/nezhapanel && pm2 start ./dashboard"

# 遍历服务器列表并执行恢复操作
for server in servers:
    host = server['host']
    port = server['port']
    username = server['username']
    password = server['password']
    cron_command = server.get('cron', default_restore_command)

    print(f"连接到 {host}...")

    # 查找 pm2 路径并执行恢复命令
    find_pm2_command = "which pm2"
    find_pm2_full_command = f"sshpass -p '{password}' ssh -o StrictHostKeyChecking=no -p {port} {username}@{host} '{find_pm2_command}'"
    try:
        pm2_path = subprocess.check_output(find_pm2_full_command, shell=True, stderr=subprocess.STDOUT).decode('utf-8').strip()
        if not pm2_path:
            raise Exception("无法找到 pm2 路径")
        restore_command = f"sshpass -p '{password}' ssh -o StrictHostKeyChecking=no -p {port} {username}@{host} 'cd ~/nezhapanel && {pm2_path} start ./dashboard'"
        print(f"Executing restore command on {host}: {restore_command}")
        output = subprocess.check_output(restore_command, shell=True, stderr=subprocess.STDOUT)
        summary_message += f"\n成功恢复 {host} 上的哪吒面板服务：\n{output.decode('utf-8')}"
    except subprocess.CalledProcessError as e:
        summary_message += f"\n无法恢复 {host} 上的哪吒面板服务：\n{e.output.decode('utf-8')}\nCommand: {restore_command}\nError: {str(e)}"
    except Exception as e:
        summary_message += f"\n在 {host} 上查找 pm2 失败：\n{str(e)}"

# 发送汇总消息到 Telegram
send_telegram_message(telegram_token, telegram_chat_id, summary_message)
