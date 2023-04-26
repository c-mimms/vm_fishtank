from agents.agent_interface import AgentInterface
import libvirt
import paramiko
import xml.etree.ElementTree as ET

class ConcreteAgent(AgentInterface):

    def __init__(self, vm: libvirt.Domain):
        self.vm = vm
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.output = ""

    def connect(self):
        ip_address = self.get_vm_ip_address()
        self.ssh.connect(ip_address, username="root", password="your_vm_password_here")

    def disconnect(self):
        self.ssh.close()

    def get_vm_ip_address(self) -> str:
        iface = self.vm.interfaceAddresses(libvirt.VIR_DOMAIN_INTERFACE_ADDRESSES_SRC_LEASE)

        for _, iface_info in iface.items():
            for addr in iface_info["addrs"]:
                if addr["type"] == libvirt.VIR_IP_ADDR_TYPE_IPV4:
                    return addr["addr"]

        raise RuntimeError("IP address not found for the VM")

    def execute_command(self, command: str) ->str:
        stdin, stdout, stderr = self.ssh.exec_command(command)
        output = stdout.read().decode('utf-8')
        print("Ran command \"" + command + "\" Output: \"" + output +"\"")
        return output
    
    def iterate(self):
        next_command = self.generate_next_command(self.output)
        self.output = self.execute_command(next_command)

    def generate_next_command(self, command: str) ->str:
        return "pwd"