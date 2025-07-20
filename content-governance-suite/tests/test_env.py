import os
from dotenv import load_dotenv

load_dotenv()

required_vars = [
    "PPLX_API_KEY",
    "DATABASE_URL",
    "REDIS_URL"
]

print("Environment Variable Check:")
for var in required_vars:
    value = os.getenv(var)
    status = "✅ SET" if value else "❌ MISSING"
    print(f"{var}: {status}")
