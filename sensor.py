import random
locations=[
    ("Sullia",12.5647,75.98768),
    ("Puttur",12.98765,75.0975),
    ("Mangalore",12.8996,75.9779),
    ("Mysore",12.1259,75.09868),
    ("Madikeri",12.66990,75.9876),
    ("Sakleshpur",12.0879,75.98990)
    ]
vehicle_numbers=[
    "KA21AB6789",
    "KA21345689",
    "KA21SD5677",
    "KA21ER5679",
    "KA21WE56799",
    "KA21DF78965"
    ]
accident_status=[
    "Minor",
    "Major",
    "Critical"
]
def get_location():
    return random.choice(locations)
def get_vehicle_number():
    return random.choice(vehicle_numbers)
def get_accident_status():
    return random.choice(accident_status)