-- 계정 생성
CREATE USER meta_user WITH PASSWORD 'your_strong_pw';

-- 메타데이터 전용 스키마
CREATE SCHEMA metadata AUTHORIZATION meta_user;

-- 스키마 작업 권한
GRANT USAGE ON SCHEMA metadata TO meta_user;
GRANT CREATE ON SCHEMA metadata TO meta_user;

-- 향후 생성될 시퀀스 권한도 같이 부여 (SERIAL 쓸 거니까)
ALTER DEFAULT PRIVILEGES IN SCHEMA metadata
GRANT USAGE, SELECT ON SEQUENCES TO meta_user;

-- 향후 생성될 테이블 자동 권한
ALTER DEFAULT PRIVILEGES IN SCHEMA metadata
GRANT SELECT, INSERT ON TABLES TO meta_user;

-- 기본 권한 설정
GRANT USAGE ON SCHEMA metadata TO meta_user;
GRANT CREATE ON SCHEMA metadata TO meta_user;