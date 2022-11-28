import requests
import uiautomator2 as u2

def post_apk(apk_path, source_code_zip=None):
    url = "http://localhost:9002/commit_app"
    files = {'apk': open(apk_path, 'rb')}
    if source_code_zip is not None:
        files['source_code'] = open(source_code_zip, 'rb')
    response = requests.post(url, files=files)
    print(response)


if __name__ == '__main__':
    # post_apk('/Users/xuhao/Desktop/jacoco_apps/alarmclock_jacoco.apk',
    #          '/Users/xuhao/Desktop/Q-testing-benchmark1/alarmclock-2.2.3_r2.11.zip')
    device = u2.connect_usb('emulator-5554')
    button1 = device(resourceId="android:id/switch_widget")
    import time
    time.sleep(5)
    button2 = device(resourceId="android:id/switch_widget")
    print(button1)
    print(button2)

