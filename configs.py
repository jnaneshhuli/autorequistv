from os import path, getenv

class Config:
    API_ID = int(getenv("API_ID", "29570230"))
    API_HASH = getenv("API_HASH", "17c54577b97263cce14f01f820a7e478")
    BOT_TOKEN = getenv("BOT_TOKEN", "6852169715:AAG348M5ApqTY_jKJC-FS3bNYheQJnod3jE")
    FSUB = getenv("FSUB", "ROCKERSBACKUP")
    CHID = int(getenv("CHID", "-1001654950491"))
    SUDO = list(map(int, getenv("SUDO").split()))
    MONGO_URI = getenv("MONGO_URI", "mongodb+srv://jnanesh:jnanesh@cluster0.8pzxa6s.mongodb.net/?retryWrites=true&w=majority")
    
cfg = Config()
