

최적화 포인트
1. Checksum을 기반으로 빠르게 중복 체크
checksum = hashlib.md5(await file.read()).hexdigest()
await file.seek(0)

SELECT 1 FROM upload_metadata WHERE checksum = ... LIMIT 1


멱등성 보장(idempotency)
동시 요청에 대한 요청 단위로 멱등성 키(idempotency key) 생성
예: 파일의 checksum + 요청 시간 기반 해시
체크섬 : 파일자체의 해쉬값으로 중복방지
클라이언트가 직접 UUID 만들고 요청마다 넘기도록


체크섬 해결전략
| 상황            | 처리 방법                                                                 |
| 작은 파일     | `await file.read()` 후 해시 계산 (FastAPI에서 수 MB 파일은 무리 없음)       |
| 대용량 파일   | chunk 단위 반복 (`while chunk := await file.read(n): ...`)로 해싱 처리      |
| 재사용 필요시 | 해시 계산 후 `await file.seek(0)` 호출해 스트림 초기화                      |
