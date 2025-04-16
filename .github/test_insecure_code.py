import os

# ⚠️ Insecure: Hardcoded password
password = "123456"

# ⚠️ Insecure: Dangerous system call
os.system('rm -rf /')  # Just a test, don't run this
