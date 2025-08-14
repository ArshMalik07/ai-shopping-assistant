import pandas as pd
import json

# 1. CSV file ka path
csv_file = "E:\\7th Sem\\ai-shopping-asistant\\amazon.csv"   # apna CSV file ka naam yaha daalo
json_file = "dataset.json" # output JSON file

# 2. CSV read karo
df = pd.read_csv(csv_file)

# 3. DataFrame ko JSON me convert karo
json_data = df.to_dict(orient="records")

# 4. JSON file save karo
with open(json_file, "w", encoding="utf-8") as f:
    json.dump(json_data, f, indent=4, ensure_ascii=False)

print(f"✅ CSV se JSON conversion complete! File saved as: {json_file}")
