import os
from dotenv import load_dotenv
load_dotenv()
if (os.getenv('DEBUG', '')):
    print(os.getenv('FORSAN2', ''))
    print(os.getenv('UPADD', ''))