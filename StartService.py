import ctypes
import subprocess
import schedule
import time
import psutil


service_name = "mosquitto"

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
def check_service_status(service_name):
    for service in psutil.win_service_iter():
        if service.name() == service_name:
            if service.as_dict()['status'] == 'running':
                return "Running"
            else:
                return "Stopped"
    return "Service not found"

def start_service(service_name):
    if is_admin():
        try:
            if(check_service_status(service_name)!= "Running"):
                subprocess.check_call(["sc", "start", service_name])
                #print("Service {} started successfully".format(service_name))
        except subprocess.CalledProcessError as e:
            pass
            #print("Error starting service {}: {}".format(service_name, e))
    else:
        pass
        #print("This script requires administrator privileges to run.")

start_service(service_name)


schedule.every().second.do(start_service, service_name)

# Continuously run the schedule
while True:
    schedule.run_pending()
    time.sleep(1)
