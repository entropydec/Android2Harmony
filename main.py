import os,sys
sys.path.append('./lib/back')

from get_arp import MyARP
from src.MakeScripts import MakeScripts

exec('print(1)')

arp=MyARP().get_arp('../apk/filemanager.apk','test1.py')
#save arp(参考util.arphelpler)

trans1=arp.get_transitions()[0]
print(trans1)

scripts1=MakeScripts(trans1).get_scripts()
print(scripts1)