from utils import config
import os


def env_config():
    if config.Env == "HRMS":
        login_env = {
            "BASE_URL": os.getenv('DEV_URL'),
            "DASHBOARD_URL": os.getenv('DEV_DASHBOARD_URL'),
            "USERNAME": os.getenv('DEV_USERNAME'),
            "PASSWORD": os.getenv('DEV_PASSWORD'),
            "ENVIRONMENT": "DEV"
        }
    else:
        raise ValueError(f"Unknown environment: {config.Env}")

    return login_env


def mobile_config():
    """
    iPhone 12 Pro
    Galaxy S5
    iPad
    iPad Pro
    Nexus 10
    """
    mobile_env = {
        "is_enabled": False,
        "deviceName": "iPhone 12 Pro"
    }
    return mobile_env
