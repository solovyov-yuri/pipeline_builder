import yaml


class Config:
    def __init__(self, config_file: str = "config.yaml"):
        """
        Initialize the Config object
        :param config_file: The path to the config file
        """
        with open(config_file, "r") as f:
            try:
                self.config = yaml.safe_load(f)
            except yaml.YAMLError as e:
                print(f"Error loading config file: {e}")

    def get(self, key_path, default=None):
        """
        Get a value from the config file using a key path
        :param key_path: The key path to the value
        :param default: The default value to return if the key path does not exist
        :return: The value at the key path or the default value
        """
        keys = key_path.split(".")
        data = self.config

        for key in keys:
            if isinstance(data, dict) and key in data:
                data = data[key]
            else:
                return default
        return data


config = Config()
