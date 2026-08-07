import random
import time
def detect_accident():
    print("AI is analysing sensor data")
    time.sleep(2)
    result=random.choice([True])
    if result:
        print("accident detected")
    else:
        print("No accident detected")
    return result