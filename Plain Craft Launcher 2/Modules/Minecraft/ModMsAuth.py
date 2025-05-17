# -*- coding: utf-8 -*-
"""
Minecraft Microsoft 账户登录模块

使用 Microsoft Authentication Library (MSAL) for Python 实现 Minecraft 微软账户登录
再根据账户登录信息获取 Minecraft Profile 用于启动 Minecraft
"""

import os
import webbrowser
from typing import Dict, Any, Optional, List

import msal
import requests


class MinecraftMicrosoftLogin:
    """Minecraft Microsoft 账户登录类

    使用 MSAL 库实现 Minecraft 微软账户的登录流程，包括：
    1. 获取微软账户的访问令牌
    2. 使用访问令牌获取 Xbox Live 令牌
    3. 使用 Xbox Live 令牌获取 XSTS 令牌
    4. 使用 XSTS 令牌获取 Minecraft 令牌
    """

    # Microsoft OAuth 端点
    AUTHORITY = "https://login.microsoftonline.com/consumers"

    # Xbox Live 认证 URL
    XBOX_AUTH_URL = "https://user.auth.xboxlive.com/user/authenticate"

    # XSTS 认证 URL
    XSTS_AUTH_URL = "https://xsts.auth.xboxlive.com/xsts/authorize"

    # Minecraft 服务 URL
    MC_LOGIN_URL = "https://api.minecraftservices.com/authentication/login_with_xbox"
    MC_PROFILE_URL = "https://api.minecraftservices.com/minecraft/profile"

    # 默认的令牌缓存文件路径
    DEFAULT_CACHE_PATH = os.path.join(os.path.expanduser("~"), ".minecraft", "msal_token_cache.json")

    def __init__(self, client_id: str, cache_path: Optional[str] = None, scopes: Optional[List[str]] = None):
        """初始化 MinecraftMicrosoftLogin 实例

        Args:
            client_id: 应用程序的客户端 ID
            cache_path: 令牌缓存文件路径，默认为 ~/.minecraft/msal_token_cache.json
            scopes: 请求的权限范围，默认为 ['XboxLive.signin']
        """
        self.client_id = client_id
        self.cache_path = cache_path or self.DEFAULT_CACHE_PATH
        self.scopes = scopes or ["XboxLive.signin"]

        # 确保缓存目录存在
        os.makedirs(os.path.dirname(self.cache_path), exist_ok=True)

        # 初始化令牌缓存
        self.token_cache = msal.SerializableTokenCache()

        # 如果缓存文件存在，则加载缓存
        if os.path.exists(self.cache_path):
            try:
                with open(self.cache_path, "r") as cache_file:
                    self.token_cache.deserialize(cache_file.read())
            except Exception as e:
                print(f"加载令牌缓存失败: {e}")

        # 创建 MSAL 应用实例
        self.app = msal.PublicClientApplication(
            client_id=self.client_id,
            authority=self.AUTHORITY,
            token_cache=self.token_cache
        )

    def _save_cache(self) -> None:
        """保存令牌缓存到文件"""
        if self.token_cache.has_state_changed:
            try:
                with open(self.cache_path, "w") as cache_file:
                    cache_file.write(self.token_cache.serialize())
            except Exception as e:
                print(f"保存令牌缓存失败: {e}")

    def get_microsoft_token(self) -> Dict[str, Any]:
        """获取微软账户的访问令牌

        首先尝试从缓存中获取令牌，如果缓存中没有有效的令牌，则使用交互式登录获取新令牌

        Returns:
            包含访问令牌的字典，如果失败则包含错误信息
        """
        # 尝试从缓存中获取令牌
        accounts = self.app.get_accounts()
        result = None

        if accounts:
            # 使用第一个账户尝试静默获取令牌
            result = self.app.acquire_token_silent(self.scopes, account=accounts[0])

        if not result:
            # 如果缓存中没有令牌，则使用交互式登录
            try:
                # 生成设备代码流程
                flow = self.app.initiate_device_flow(scopes=self.scopes)

                if "user_code" not in flow:
                    return {"success": False, "error": "无法创建设备代码流程", "details": flow.get("error")}

                # 显示用户代码和验证 URL
                print(f"请访问: {flow['verification_uri']} 并输入代码: {flow['user_code']}")

                # 尝试自动打开浏览器
                try:
                    webbrowser.open(flow["verification_uri"])
                except Exception:
                    pass  # 如果无法打开浏览器，用户可以手动访问 URL

                # 等待用户完成登录
                result = self.app.acquire_token_by_device_flow(flow)
            except Exception as e:
                return {"success": False, "error": "登录过程中发生错误", "details": str(e)}

        # 保存令牌缓存
        self._save_cache()

        if "access_token" in result:
            return {"success": True, "token": result}
        else:
            return {"success": False, "error": "获取访问令牌失败", "details": result.get("error")}

    def get_xbox_token(self, ms_token: str) -> Dict[str, Any]:
        """使用微软访问令牌获取 Xbox Live 令牌

        Args:
            ms_token: 微软访问令牌

        Returns:
            包含 Xbox Live 令牌的字典，如果失败则包含错误信息
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        payload = {
            "Properties": {
                "AuthMethod": "RPS",
                "SiteName": "user.auth.xboxlive.com",
                "RpsTicket": f"d={ms_token}"
            },
            "RelyingParty": "http://auth.xboxlive.com",
            "TokenType": "JWT"
        }

        try:
            response = requests.post(self.XBOX_AUTH_URL, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            return {
                "success": True,
                "token": data["Token"],
                "user_hash": data["DisplayClaims"]["xui"][0]["uhs"]
            }
        except Exception as e:
            return {"success": False, "error": "获取 Xbox Live 令牌失败", "details": str(e)}

    def get_xsts_token(self, xbox_token: str) -> Dict[str, Any]:
        """使用 Xbox Live 令牌获取 XSTS 令牌

        Args:
            xbox_token: Xbox Live 令牌

        Returns:
            包含 XSTS 令牌的字典，如果失败则包含错误信息
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        payload = {
            "Properties": {
                "SandboxId": "RETAIL",
                "UserTokens": [xbox_token]
            },
            "RelyingParty": "rp://api.minecraftservices.com/",
            "TokenType": "JWT"
        }

        try:
            response = requests.post(self.XSTS_AUTH_URL, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            return {
                "success": True,
                "token": data["Token"],
                "user_hash": data["DisplayClaims"]["xui"][0]["uhs"]
            }
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                # 检查特定的 Xbox Live 错误代码
                try:
                    error_data = e.response.json()
                    xerr = error_data.get("XErr")
                    if xerr == 2148916233:
                        return {"success": False, "error": "此账户未关联 Xbox 账户", "details": "XErr: 2148916233"}
                    elif xerr == 2148916238:
                        return {"success": False, "error": "此账户来自不支持 Xbox Live 的国家/地区",
                                "details": "XErr: 2148916238"}
                except Exception:
                    pass
            return {"success": False, "error": "获取 XSTS 令牌失败", "details": str(e)}
        except Exception as e:
            return {"success": False, "error": "获取 XSTS 令牌失败", "details": str(e)}

    def get_minecraft_token(self, user_hash: str, xsts_token: str) -> Dict[str, Any]:
        """使用 XSTS 令牌获取 Minecraft 令牌

        Args:
            user_hash: 用户哈希
            xsts_token: XSTS 令牌

        Returns:
            包含 Minecraft 令牌的字典，如果失败则包含错误信息
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        payload = {
            "identityToken": f"XBL3.0 x={user_hash};{xsts_token}"
        }

        try:
            response = requests.post(self.MC_LOGIN_URL, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            return {"success": True, "token": data["access_token"], "expires_in": data["expires_in"]}
        except Exception as e:
            return {"success": False, "error": "获取 Minecraft 令牌失败", "details": str(e)}

    def get_minecraft_profile(self, mc_token: str) -> Dict[str, Any]:
        """获取 Minecraft 个人资料

        Args:
            mc_token: Minecraft 访问令牌

        Returns:
            包含 Minecraft 个人资料的字典，如果失败则包含错误信息
        """
        headers = {
            "Authorization": f"Bearer {mc_token}"
        }

        try:
            response = requests.get(self.MC_PROFILE_URL, headers=headers)
            response.raise_for_status()
            return {"success": True, "profile": response.json()}
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                return {"success": False, "error": "此账户未拥有 Minecraft", "details": "HTTP 404"}
            return {"success": False, "error": "获取 Minecraft 个人资料失败", "details": str(e)}
        except Exception as e:
            return {"success": False, "error": "获取 Minecraft 个人资料失败", "details": str(e)}

    def login(self) -> Dict[str, Any]:
        """执行完整的登录流程

        执行从微软账户登录到获取 Minecraft 令牌的完整流程

        Returns:
            包含登录结果的字典，成功时包含 Minecraft 令牌和个人资料，失败时包含错误信息
        """
        # 获取微软令牌
        ms_result = self.get_microsoft_token()
        if not ms_result["success"]:
            return ms_result

        ms_token = ms_result["token"]["access_token"]

        # 获取 Xbox Live 令牌
        xbox_result = self.get_xbox_token(ms_token)
        if not xbox_result["success"]:
            return xbox_result

        xbox_token = xbox_result["token"]
        user_hash = xbox_result["user_hash"]

        # 获取 XSTS 令牌
        xsts_result = self.get_xsts_token(xbox_token)
        if not xsts_result["success"]:
            return xsts_result

        xsts_token = xsts_result["token"]

        # 获取 Minecraft 令牌
        mc_result = self.get_minecraft_token(user_hash, xsts_token)
        if not mc_result["success"]:
            return mc_result

        mc_token = mc_result["token"]

        # 获取 Minecraft 个人资料
        profile_result = self.get_minecraft_profile(mc_token)
        if not profile_result["success"]:
            return profile_result

        # 返回完整的登录结果
        return {
            "success": True,
            "minecraft_token": mc_token,
            "profile": profile_result["profile"],
            "expires_in": mc_result["expires_in"]
        }

