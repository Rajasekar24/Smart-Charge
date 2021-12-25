import psutil
import tinytuya
import csv
import datetime
from win10toast import ToastNotifier
import emoji

toaster = ToastNotifier()
debugMode = False
action = "No Action"
statusCode = "No Request Made"


def plugRequest(switchState):
    d = tinytuya.OutletDevice('52585621c4dd571b8db0', '192.168.29.98', '32ba71b35d1df9a4')
    d.set_version(3.3)
    d.status()
    data = d.status()
    # if data['Error'] & data['Error'] == 'Network Error: Device Unreachable':
    #     toaster.show_toast("Smart-Charge", "Pls turn on Smart-plug")
    # else:
    d.set_status(switchState)
    if switchState:
        d.set_timer(5400)  # 1hour 30 mins is 5400secs
    txt = "charging :battery::electric_plug:" if switchState else "Charged :battery:"
    toaster.show_toast("Smart-Charge", emoji.emojize(txt))


battery = psutil.sensors_battery()
pluggedIn = battery.power_plugged
currentCharge = battery.percent

if not pluggedIn:
    chargeState = "Not Plugged In"
else:
    chargeState = "Plugged In"
print(f"{str(currentCharge)}% | {chargeState}")
if debugMode:
    toaster.show_toast("Smart-Charge", f"{str(currentCharge)}% | {chargeState}")

if pluggedIn and currentCharge >= 80:
    # unplug laptop
    print("Turning off plug")
    action = "Turn Off"
    plugRequest(False)
elif not pluggedIn and currentCharge < 30:
    # plug laptop in
    print("Turning on plug")
    action = "Turn On"
    plugRequest(True)

if debugMode:
    print("Debugging Mode On - writing to log file")
    dateTime = datetime.datetime.now()

    with open('D:\\MY PROJECT\\Smart-Charge\\log.csv', mode='a') as log_file:
        log_writer = csv.writer(log_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        # Date,    Time,    Battery Level,   ChargeState,    Action,    Status Code
        log_writer.writerow(
            [f"{dateTime.day}/{dateTime.month}/{dateTime.year}", dateTime.strftime("%X"), f"{str(currentCharge)}%",
             chargeState, action, statusCode])
