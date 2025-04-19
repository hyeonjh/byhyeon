"""
📦 insert_row() 사용 예시

# 단건 insert 예시
insert_row("your_schema.your_table", {
    "col1": "value1",
    "col2": 123,
    "col3": "2025-04-21",
})

# 다건 insert 예시 (list[dict])
insert_row("your_schema.your_table", [
    {
        "col1": "value1",
        "col2": 123,
        "col3": "2025-04-21",
    },
    {
        "col1": "value2",
        "col2": 456,
        "col3": "2025-04-22",
    }
])
"""

from psycopg2.errors import UniqueViolation
import psycopg2
import os
from dotenv import load_dotenv
# 로그설정
from logs.logs import logger
import traceback

load_dotenv()



def insert_row(table_name: str, data):
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT", 5432)
        )
        cur = conn.cursor()

        # 자동 감지: 단건 vs 다건
        if isinstance(data, dict):
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['%s'] * len(data))
            values = list(data.values())

            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            cur.execute(query, values)

        elif isinstance(data, list) and isinstance(data[0], dict):
            columns = ', '.join(data[0].keys())
            placeholders = ', '.join(['%s'] * len(data[0]))
            values = [tuple(d.values()) for d in data]

            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            cur.executemany(query, values)

        else:
            logger.error("❌ insert_row 실패 - data는 dict 또는 list[dict] 여야 함")
            raise ValueError("data는 dict 또는 list[dict] 여야 함")

        conn.commit()
        logger.info(f"✅ Insert 성공: {table_name} ({'bulk' if isinstance(data, list) else 'single'})")

    except psycopg2.IntegrityError as e:
        conn.rollback()
        if isinstance(e.__cause__, UniqueViolation):
            logger.warning("❌ 중복된 파일: checksum UNIQUE 제약에 걸림")
            raise ValueError("중복된 파일입니다. checksum이 이미 존재합니다.")
        else:
            logger.error(f"❌ DB IntegrityError: {e}", exc_info=True)
            raise

    except Exception as e:
        logger.error(f"❌ insert 실패: {e}", exc_info=True)
        raise
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()