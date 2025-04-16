

-- 현재유저확인
SELECT current_user;


-- 슈퍼유저인지확인 
SELECT usesuper FROM pg_user WHERE usename = 'hyeonjh'

-- 특정 계정의 권한 확인

SELECT * FROM pg_roles WHERE rolname = 'hyeonjh';
