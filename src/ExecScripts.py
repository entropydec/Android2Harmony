
class ExecScriptFile:
    def __init__(self,arp,scripts):
        self.in_scripts=scripts
        self.arp=arp
        self.out_scripts=[]

    def install_app(self):
        pass

    def launch_app(self):
        pass

    def run_script(self):
        pass

    def run(self):
        self.install_app()
        self.out_scripts.append()
        self.launch_app()
        self.out_scripts.append()
        for script in self.in_scripts:
            success=self.run(script)
            if success:
                self.out_scripts.append(script)
                continue
            else:
                analysis_and_reconstruct()
