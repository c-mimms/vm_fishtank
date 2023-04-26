import libvirt
from agents.agent_interface import AgentInterface
from virtual_network import VirtualNetwork

class VMManager:

    def __init__(self, config: dict):
        self.config = config
        self.connection = libvirt.open("qemu:///system")
        self.network = VirtualNetwork(self.connection, self.config["network_settings"])
        self.vms = []
        self.agents = []

    def start(self):
        self.network.create()

        for _ in range(self.config["vm_count"]):
            vm = self.create_vm(self.config["vm_settings"])
            agent = self.create_agent(vm)
            self.vms.append(vm)
            self.agents.append(agent)

        for agent in self.agents:
            agent.connect()

        try:
            while True:
                for agent in self.agents:
                    agent.iterate()
                    time.sleep(5)  # Add a delay between iterations if needed
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        for agent in self.agents:
            agent.disconnect()

        for vm in self.vms:
            self.destroy_vm(vm)

        self.network.destroy()
        self.connection.close()
