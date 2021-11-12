from pywinauto.application import Application
from time import sleep

def run_cisco():
    anyconnect = r"C:\Program Files (x86)\Cisco\Cisco AnyConnect Secure Mobility Client\vpnui.exe"
    app = Application().start(anyconnect)
    app = app.connect(path=anyconnect)

    win = app.window(best_match = 'Cisco AnyConnect Secure Mobility Client')

    child = win.child_window(best_match = 'ComboBox2').wrapper_object()
    return child

def connect_guest(child):
    child.select('A1 guest').click()
    sleep(5)

def connect_wired(child):
    child.select('Wired_Dot1x_MO').click()
    sleep(5)
