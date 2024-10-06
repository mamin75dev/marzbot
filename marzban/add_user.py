def body(username: str, user_id: str, data_limit, expire_duration):
    return {
        "username": username,
        "proxies": {
            "vless": {
                id: user_id,
            }
        },
        "inbounds": {
            "vmess": [],
            "vless": [
                "VLESS + TCP",
                "VLESS TCP Header NoTLS"
            ]
        },
        "expire": None,
        "data_limit": data_limit,
        "data_limit_reset_strategy": "no_reset",
        "status": "on_hold",
        "note": "",
        "on_hold_timeout": None,
        "on_hold_expire_duration": expire_duration
    }
