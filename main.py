import os,sys
sys.path.append('./lib/arp')

from get_arp import MyARP
from src.MakeScripts import MakeScripts
from src.GenerateFIle import GenerateFile
from src.ExecScripts import ExecScriptFile

arp=MyARP().get_arp('../apk/filemanager.apk','test1.py')
#save arp(参考util.arphelpler)

scripts=[]
trans=arp.get_transitions()
for id in trans:
    make=MakeScripts(trans[id])
    scripts.append(make.get_scripts())

exec=ExecScriptFile(arp,scripts)
exec.run()
stmts=exec.get_stmt()
GenerateFile([],stmts,'out.py').run()