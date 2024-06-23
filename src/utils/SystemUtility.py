import subprocess


class SystemUtility():

    def run_command(self, command, timeout=30):
        """
        executes given system command and returns the output or error
        :param command: array. Ex ["ls", "-l"] or String "ls -l"
        :param timeout: command timeout
        :return:
        """

        # determine if the command is a list or string
        if isinstance(command, list):
            # list
            shell = False
        else:
            # string
            shell = True

        # try:
        byte_output = subprocess.check_output(command, shell=shell, timeout=timeout)
        return byte_output.decode('UTF-8').rstrip()
        # except Exception as e:
        #     return str(e)
