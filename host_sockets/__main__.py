from dynatrace_extension import Extension, Status, StatusValue
import subprocess
import re
import platform


class HostSocketStats(Extension):

    def get_ss_records(self, port:int):
        try:
            if platform.system() == "Linux":
                # Execute the ss command with filtering for a specific port
                command = [
                    "ss", "-ant", f"( sport = :{port} )"
                ]   
                result = subprocess.run(command,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        text=True,
                                        check=False)
                records = {}
                # Check for errors in command execution
                if result.returncode != 0:
                    self.logger.error("Error executing ss command: {result.stderr}")
                    return records

                # Parse the output into records
                lines = result.stdout.strip().split("\n")
                # Skip the header line and process the remaining lines
                for line in lines[1:]:
                    parts = re.split(r"\s+", line)
                    if len(parts)==5:
                        records[parts[0]] = records.get(parts[0],0)+1
                    return records
            elif platform.system() == "Windows":
                result = subprocess.run('netstat -ano',
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        text=True,
                                        check=False)
                records = {}
                lines = result.stdout.strip().split("\n")
                for i, line in enumerate(lines):
                    sline = line.lstrip()
                    parts = re.split(r"\s+", sline)
                    if len(parts)<2 or parts[0] not in ["TCP", "UDP"]:
                        continue
                    records[i] = sline
                return records
            else:
                return {}
        except Exception as e:
            print(f"Error: {e}")
            return []

    def initialize(self):
        pass

    def query(self):        
        for tcp_port in self.activation_config["tcp_ports"]:
            ss_output = self.get_ss_records(tcp_port)
            for state in ss_output.keys():
                self.report_metric("host.net.sockets", ss_output[state], dimensions={"protocol": "TCP", "port": tcp_port, "state":state})

    def fastcheck(self) -> Status:
        """
        Run ss command to check if present
        """
        command = [
            "ss", "-ant"
        ]            
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode != 0:
            return Status(StatusValue.GENERIC_ERROR)

        return Status(StatusValue.OK)


def main():
    HostSocketStats().run()

if __name__ == '__main__':
    main()
