from abc import ABC, abstractmethod

class AgentInterface(ABC):

    @abstractmethod
    def connect(self):
        """
        Connect to the VM using SSH.
        """
        pass

    @abstractmethod
    def disconnect(self):
        """
        Disconnect from the VM.
        """
        pass

    @abstractmethod
    def execute_command(self, command: str) -> str:
        """
        Execute a command on the VM and return the output.

        :param command: The command to run on the VM.
        :return: The output from the command.
        """
        pass

    @abstractmethod
    def iterate(self, output: str) -> str:
        """
        Process the output from the VM and return the next command to run.

        :param output: The output from the previous command executed on the VM.
        :return: The next command to run on the VM.
        """
        pass
