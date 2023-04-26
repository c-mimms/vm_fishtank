import yaml
from vm_manager import VMManager

if __name__ == "__main__":
    with open("config.yaml", "r") as config_file:
        config = yaml.safe_load(config_file)

    vm_manager = VMManager(config)

    try:
        vm_manager.start()
    except KeyboardInterrupt:
        vm_manager.stop()
