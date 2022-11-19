import os,sys
sys.path.append('./lib/back')

from get_arp import MyARP
arp=MyARP.getARP('../apk/filemanagerpro.apk','testcase.py')
#save arp(参考util.arphelpler)

print(arp.get_states()[0])