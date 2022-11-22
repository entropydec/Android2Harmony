from time import sleep
from xml.etree.ElementPath import xpath_tokenizer
import uiautomator2
import subprocess

def wait():
    input('\npress any key to continue...')

if __name__=='__main__':
    wait()
    device=uiautomator2.connect_usb()

    wait()
    subprocess.call(['adb','uninstall','com.michaldabski.filemanager'])

    wait()
    subprocess.call(['adb','install','../apk/filemanager.apk'])

    wait()
    device.app_start('com.michaldabski.filemanager','.folders.FolderActivity')
    print('start the app')

    wait()
    device(className='android.widget.RelativeLayout')[4].click()

    wait()
    device(className='android.widget.RelativeLayout')[0].click()

    wait()
    device(resourceId='com.michaldabski.filemanager:id/menu_navigate_up').click()

    wait()
    device(className='android.widget.RelativeLayout')[1].long_click(1.0)

    wait()
    device(description='更多选项').click()

    wait()
    els=device(className='android.widget.LinearLayout')
    els[5].click()
    #el=device.xpath('//android.widget.ListView/android.widget.LinearLayout[6]/android.widget.RelativeLayout[1]')
    #el.click()

    wait()
    device(resourceId='android:id/button1').click()

    wait()
    device(resourceId='android:id/action_mode_close_button').click()

    quit()



