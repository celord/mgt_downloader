import os
import tomllib

def get_config():
    """
    Go to users home directory and look for a file called mgt_downloader.toml
    :return: Dictionary with the configuration
    """
    home = os.path.expanduser("~")
    config_file = os.path.join(home, "mgt_downloader.toml")
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"Config file not found: {config_file}")
    with open(config_file, 'rb') as f:
        return tomllib.load(f)

