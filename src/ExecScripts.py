from src.Model.ActionScripts import ActionScripts
import subprocess

class ExecScriptFile:
    def __init__(self,arp,scripts,driver):
        self.in_scripts=scripts
        self.arp=arp
        self.out_stmt=[]
        self.app=arp.get_app()
        self.driver=driver

    def install_app(self):
        apk=self.app.get_apk_path()
        cmd=['hdc','app','install',apk]
        subprocess.call(cmd)
        res='subprocess.call(['+\
            +'\''+cmd[0]+'\','+\
            +'\''+cmd[1]+'\','+\
            +'\''+cmd[2]+'\','+\
            +'\''+cmd[3]+'\'])'
        return res

    def launch_app(self):
        package=self.app.get_package_name()
        activity=self.app.get_main_activity()
        self.driver.app_start(package,activity)
        res='device.app_start('+\
            +'\''+package+'\','+\
            +'\''+activity+'\'])'
        return res
    
    def run_script(self):
        return True

    def get_stmt(self):
        return self.out_stmt

    def run(self):
        install=self.install_app()
        self.out_stmt.append(install+'\n\n')
        launch=self.launch_app()
        self.out_stmt.append(launch+'\n\n')
        for script in self.in_scripts:
            success=self.run_script()
            if success:
                self.out_stmt.append(script.get_location_stmt()+'\n')
                self.out_stmt.append(script.get_event_stmt()+'\n\n')
                continue
            else:
                #analysis_and_reconstruct()
                pass
