import os,sys
sys.path.append('./lib/back')

from get_arp import MyARP
arp=MyARP.getARP('/Users/suou/study/Android2Harmony/files/hello.apk','test.py')
#save arp(参考util.arphelpler)

print(arp.get_states()[0])