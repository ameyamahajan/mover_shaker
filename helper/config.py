import yaml
import os


class ConfigApp:
    """
    This class would load the configuration file based on the requirement
    """
    config_dir = '../config/'

    def __init__(self, client_name, type='POS'):
        self.client_name = client_name
        config_file = '../config/'+self.client_name+"_"+type.lower()+"_common.yaml"
        print(config_file)
        if os.path.exists(config_file):
            with open(config_file, 'r') as fd:
                self.conf_data = yaml.safe_load(fd)
        else:
            print("File missing!: Can perform any actions")

    def temp_funct(self):
        pass

    """
    def get_config_par(self):
        return self.conf_data
    
    def set_config_par(self, conf_data):
         self.conf_data = conf_data
    """
