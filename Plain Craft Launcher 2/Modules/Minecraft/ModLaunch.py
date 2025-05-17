# -*- coding: utf-8 -*-
"""
Minecraft 启动模块

使用 MinecraftMicrosoftLogin 类进行 Minecraft 微软账户登录
使用 minecraft_launcher_lib 进行游戏启动
"""

import sys
from ModMsAuth import MinecraftMicrosoftLogin
import minecraft_launcher_lib as mclib

CLIENT_ID = "c14b0370-8d75-42f8-b329-5b60d39e319f"


def launch(options):
    minecraft_dir = input("minecraft_dir: \n> ")
    if not minecraft_dir:
        minecraft_dir = ".minecraft"

    # 安装游戏版本 1.20.1
    version_id = "1.20.1"
    mclib.install.install_minecraft_version(version_id, minecraft_dir)

    launch_command = mclib.command.get_minecraft_command(
        version_id,
        minecraft_dir,
        options
    )

    # 启动游戏
    import subprocess
    subprocess.run(launch_command)


def main():
    """主函数，演示登录流程"""
    print("Minecraft Microsoft 账户登录示例")
    print("-" * 40)

    # 初始化登录模块
    mc_login = MinecraftMicrosoftLogin(client_id=CLIENT_ID)

    # 执行登录流程
    print("开始登录流程...")
    print("请按照提示在浏览器中完成 Microsoft 账户登录")
    print("-" * 40)

    result = mc_login.login()

    if result["success"]:
        # 登录成功，显示用户信息
        profile = result["profile"]
        print(f"登录成功！欢迎，{profile['name']}")
        print(f"UUID: {profile['id']}")
        print(f"令牌有效期: {result['expires_in']} 秒")

        options = {
            "username": profile['name'],  # 离线模式用户名
            "uuid": profile['id'],  # 离线模式留空
            "token": result['minecraft_token']  # 正版需填写微软令牌
        }
        launch(options)

        print("\n你现在可以使用此令牌启动游戏或执行其他操作")
    else:
        # 登录失败，显示错误信息
        print(f"登录失败: {result['error']}")
        if "details" in result:
            print(f"详细信息: {result['details']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
