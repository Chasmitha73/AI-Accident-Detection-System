
from ai_detection import detect_accident
from database import save_accident_details
from alert import send_alert
from sensor import get_location,get_vehicle_number,get_accident_status
from datetime import datetime
print("-"*40)
print("🚨AI ACCIDENT DETECTION SYSTEM🚨")
print("-"*40)
if detect_accident():
    current_time=datetime.now()
    location,latitude,longitude=get_location()
    vehicle_number=get_vehicle_number()
    status=get_accident_status()
    send_alert(location,latitude,longitude,vehicle_number,status)
    save_accident_details(location,vehicle_number,current_time)
    print("\n⏰ Date Time:⏰",current_time)
    print("\n Alert process completed✅.")
else:
    print("No accident occured.")
