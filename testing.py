from decouple import config
CONNECTION_STRING = config("CONNECTION_STRING")
print(CONNECTION_STRING)