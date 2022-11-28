subprocess.call(['adb','install','com.michaldabski.filemanager'])
device.app_start('com.michaldabski.filemanager','.folders.FolderActivity')
el=device(className='android.widget.RelativeLayout')[4]
el.click()
el=device(className='android.widget.RelativeLayout')[0]
el.click()
el=device(resourceId='com.michaldabski.filemanager:id/menu_navigate_up')
el.click()
