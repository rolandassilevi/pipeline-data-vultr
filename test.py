from datetime import datetime

value = "01/05/2022 0:05"

try:
    converted_value = datetime.strptime(value, "%d/%m/%Y %H:%M").strftime("%Y-%m-%d %H:%M:%S")
    print(f"✅ Conversion réussie : {converted_value}")
except ValueError as e:
    print(f"❌ Erreur de conversion : {e}")
