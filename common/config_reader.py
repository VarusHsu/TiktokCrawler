import yaml


class ConfigReader:
    config: dict
    server_ip: str
    server_port: int
    server_url: str

    def read_config(self):
        with open("./config/config.yaml", "r") as c:
            self.config = yaml.load(c.read(), Loader=yaml.Loader)
        self.server_port = self.config["server_port"]
        self.server_ip = self.config["server_address"]
        self.server_url ="http://" + self.server_ip + ":" + str(self.server_port)
    pass
