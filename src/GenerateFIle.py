class GenerateFile:
    def __init__(self,libs,scripts,file):
        self.libs=libs
        self.scripts=scripts
        self.file_name=file

    def run(self):
        file=open(self.file_name,'w+')
        for lib in self.libs:
            file.write(lib)
        for script in self.scripts:
            file.write(script)
        file.close()