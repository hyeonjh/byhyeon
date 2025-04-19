CREATE TABLE metadata.s3_file_metadata (
    id SERIAL PRIMARY KEY,                             -- 내부용 PK
    upload_uuid UUID NOT NULL UNIQUE,                    -- 업로드 고유 ID (Python에서 생성)
    original_filename TEXT NOT NULL,                   -- 사용자가 업로드한 원래 이름
    s3_folder_path TEXT ,                              -- S3 폴더경로 
    s3_filename TEXT NOT NULL,                         -- 저장된 S3 파일이름 UUID 포함 경로
    file_size BIGINT,                                  -- 바이트 단위 크기
    file_type TEXT,                                    -- File type 또는 확장자 (e.g. audio/wav)
    checksum TEXT UNIQUE,                              -- 중복 방지용 해시 → UNIQUE 제약
    created_at TIMESTAMP DEFAULT now()                 -- 업로드 시각
);
-- 삭제된 메타 (백업용)
CREATE TABLE metadata.s3_file_metadata_archive (
    LIKE metadata.s3_file_metadata INCLUDING ALL,
    deleted_at TIMESTAMP DEFAULT now()
);


--  트리거 적용
CREATE TRIGGER trg_block_update_delete
BEFORE UPDATE OR DELETE ON metadata.s3_file_metadata
FOR EACH ROW
EXECUTE FUNCTION prevent_update_delete();


--  트리거 적용
CREATE TRIGGER trg_block_update_delete
BEFORE UPDATE OR DELETE ON metadata.s3_file_metadata_archive
FOR EACH ROW
EXECUTE FUNCTION prevent_update_delete();