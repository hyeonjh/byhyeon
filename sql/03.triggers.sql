-- 📌 append-only 트리거 함수 정의
CREATE OR REPLACE FUNCTION prevent_update_delete()
RETURNS trigger AS $$
BEGIN
  RAISE EXCEPTION '이 테이블은 append-only 구조입니다. 수정 또는 삭제는 허용되지 않습니다.';
END;
$$ LANGUAGE plpgsql;