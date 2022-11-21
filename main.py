import os,sys
sys.path.append('./lib/back')

from get_arp import MyARP
arp=MyARP.getARP('../apk/filemanager.apk','test1.py')
#save arp(参考util.arphelpler)

print(arp.get_transitions()[0])