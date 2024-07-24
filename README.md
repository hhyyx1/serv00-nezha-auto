# serv00-nezha-auto
## 调度：这个workflow设置为每1小时运行一次，并且可以手动触发。
## 步骤：
Checkout code：检查出代码，虽然这里不需要代码，但是是GitHub Actions的惯例步骤。
Install sshpass：安装 sshpass 工具，用于非交互式SSH登录。
Restart Nezha Panel：通过SSH登录到服务器，并执行重启哪吒面板的命令。如果命令执行成功或失败，发送相应的消息到Telegram。


### 将代码fork到你的仓库并运行的操作步骤

#### 1. Fork 仓库

1. **访问原始仓库页面**：
    - 打开你想要 fork 的 GitHub 仓库页面。

2. **Fork 仓库**：
    - 点击页面右上角的 "Fork" 按钮，将仓库 fork 到你的 GitHub 账户下。

#### 2. 设置 GitHub Secrets

1. **创建 Telegram Bot**
    - 在 Telegram 中找到 `@BotFather`，创建一个新 Bot，并获取 API Token。
    - 获取到你的 Chat ID 方法，@KinhRoBot里发送/id@KinhRoBot`获取，返回用户信息中的`ID`就是Chat ID

2. **配置 GitHub Secrets**
    - 转到你 fork 的仓库页面。
    - 点击 `Settings`，然后在左侧菜单中选择 `Secrets`。
    - 添加以下 Secrets：
        - 修改 `ACCOUNTS_JSON`**

   ```json
   [
       {
           "host": "s7.serv00.com",   //ssh的连接地址
           "port": 22,
           "username": "user1",
           "password": "password1"
       },
       {
           "host": "example2.com",
           "port": 22,
           "username": "user2",
           "password": "password2"
       }
   ]

   ```
        - `TELEGRAM_BOT_TOKEN`: 你的 Telegram Bot 的 API Token。
        - `TELEGRAM_CHAT_ID`: 你的 Telegram Chat ID。

    - **获取方法**：
        - 在 Telegram 中创建 Bot，并获取 API Token 和 Chat ID。
        - 在 GitHub 仓库的 Secrets 页面添加这些值，确保它们安全且不被泄露。

#### 3. 启动 GitHub Actions

1. **配置 GitHub Actions**
    - 在你的 fork 仓库中，进入 `Actions` 页面。
    - 如果 Actions 没有自动启用，点击 `Enable GitHub Actions` 按钮以激活它。

2. **运行工作流**
    - GitHub Actions 将会根据你设置的定时任务（例如每三天一次，具体时间可自行设置）自动运行脚本。
    - 如果需要手动触发，可以在 Actions 页面手动运行工作流。
