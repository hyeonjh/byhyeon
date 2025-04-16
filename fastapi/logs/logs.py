import logging
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime

log_dir = "logs"
# 로그 디렉토리 없으면 생성
os.makedirs(log_dir, exist_ok=True)


# ✅ 오늘 날짜 기준 로그파일명 (하루에 하나)
date_str = datetime.now().strftime("%Y-%m-%d")
log_path = os.path.join(log_dir, f"upload_{date_str}.log")


# 로거 설정
logger = logging.getLogger("upload_logger")
logger.setLevel(logging.INFO)

# 핸들러 중복 방지
if not logger.handlers:
    handler = RotatingFileHandler(log_path, maxBytes=5*1024*1024, backupCount=3)

    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
        )

    handler.setFormatter(formatter)
    logger.addHandler(handler)