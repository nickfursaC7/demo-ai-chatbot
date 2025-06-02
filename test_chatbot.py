import os
from dotenv import load_dotenv
load_dotenv()
from handler import ask, Query

resp = ask(Query(query="How to achieve high elite status with Marriott?", user_id="test_user_123"))
resp = ask(Query(query="How many United miles do I have?", user_id="test_user_123"))
resp = ask(Query(query="How many Delta miles do I have?", user_id="test_user_123"))