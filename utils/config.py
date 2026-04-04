import os
from dotenv import load_dotenv

load_dotenv()


Env = "HRMS"

# === [ENVIRONMENT PROPERTIES] ===
Browser = os.getenv("BROWSER", "Chrome")
AppVersion = "0.1.0"
run_type = None
parallel_run = False  # set as False by default. to run parallel - set parallel_run = True and run run_parallel.py file.