import random
import pandas as pd

# กำหนดค่าสุ่มเพื่อให้ข้อมูลมีความหลากหลาย
random.seed(42)

vehicle_types = [
    "Truck (Logistics)",
    "Public Bus",
    "Delivery Van",
    "Personal Car",
]
route_zones = [
    "Bangkok - Chonburi",
    "City Route",
    "Urban Area",
    "Ayutthaya - Chiang Mai",
    "Inter-city",
    "Bangkok - Rayong",
]
revenue_plans = ["Business", "Basic", "Premium"]

data = []

# สร้างข้อมูลจำลองจำนวน 1,000 แถว
for i in range(1, 1001):
  trip_id = f"T{i:04d}"
  driver_id = f"D{random.randint(101, 300)}"
  v_type = random.choice(vehicle_types)
  r_zone = random.choice(route_zones)

  # กำหนดระยะทางและเวลาตามประเภทรถ
  if "Truck" in v_type:
    distance = random.randint(200, 800)
    duration = distance * random.uniform(0.8, 1.2)
    fatigue = random.randint(2, 10)
    drowsiness = random.randint(0, 4)
  elif "Bus" in v_type:
    distance = random.randint(50, 300)
    duration = distance * random.uniform(1.0, 1.5)
    fatigue = random.randint(1, 6)
    drowsiness = random.randint(0, 2)
  else:
    distance = random.randint(15, 150)
    duration = distance * random.uniform(1.2, 2.0)
    fatigue = random.randint(0, 3)
    drowsiness = random.randint(0, 1)

  obstacle = random.randint(0, 5)
  speeding = random.randint(0, 4)

  # คำนวณคะแนนความปลอดภัยจำลอง (ยิ่งแจ้งเตือนเยอะ คะแนนยิ่งน้อย)
  score = max(
      50,
      100
      - (fatigue * 3)
      - (drowsiness * 6)
      - (obstacle * 2)
      - (speeding * 3),
  )

  plan = (
      "Business"
      if "Truck" in v_type or "Bus" in v_type
      else random.choice(revenue_plans)
  )

  data.append({
      "trip_id": trip_id,
      "driver_id": driver_id,
      "vehicle_type": v_type,
      "route_zone": r_zone,
      "distance_km": int(distance),
      "duration_min": int(duration),
      "fatigue_alerts": fatigue,
      "drowsiness_alerts": drowsiness,
      "obstacle_detection_count": obstacle,
      "speeding_count": speeding,
      "overall_safety_score": int(score),
      "revenue_plan": plan,
  })

# แปลงเป็น DataFrame และบันทึกทับไฟล์เดิมในโฟลเดอร์ data
df_large = pd.DataFrame(data)
df_large.to_csv("data/roadsafe_ai_data.csv", index=False)
print("สร้างไฟล์ข้อมูล 1,000 แถวสำเร็จแล้ว!")