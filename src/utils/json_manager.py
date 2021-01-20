import json
from utils.logger import Logger
from config import  EXPORT_DIR

def save_json(data, file_name):
    logger = Logger()
    file = open(EXPORT_DIR + file_name, "w", encoding="utf8")
    json.dump(data["data"], file, indent=2, ensure_ascii=False)
    logger.successful("Saved json to " + EXPORT_DIR + file_name)