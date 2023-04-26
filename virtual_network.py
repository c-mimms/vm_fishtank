import libvirt

class VirtualNetwork:

    def __init__(self, connection, network_settings: dict):
        self.connection = connection
        self.network_settings = network_settings
        self.network = None

    def create(self):
        network_xml = self.generate_network_xml(self.network_settings)
        self.network = self.connection.networkDefineXML(network_xml)
        self.network.create()
        self.network.setAutostart(True)

    def destroy(self):
        self.network.destroy()
        self.network.undefine()

    def generate_network_xml(self, network_settings: dict) -> str:
        network_xml = f"""
        <network>
            <name>private</name>
            <forward mode='nat'/>
            <bridge name='virbr0' stp='on' delay='0'/>
            <ip address='{network_settings["subnet"].split("/")[0]}' netmask='255.255.255.0'>
                <dhcp>
                    <range start='{network_settings["subnet"].split("/")[0][:-1] + "2"}' end='{network_settings["subnet"].split("/")[0][:-1] + "254"}'/>
                </dhcp>
            </ip>
        </network>
        """
        return network_xml
