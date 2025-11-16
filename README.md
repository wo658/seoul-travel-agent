# Seoul Travel Agent

AI 기반 서울 여행 계획 도우미 - React Native + FastAPI

## 빠른 시작

```bash
make webapp
# 30초 대기 → http://localhost:8081 접속
```

**주요 명령어**:
- `make webapp` - 모든 서비스 자동 실행 (권장)
- `make web` - Docker 전체 스택 (PostgreSQL)
- `make stop-webapp` - 서비스 중지
- `make help` - 전체 명령어 확인

## 기술 스택

**Frontend**: React Native 0.81 + Expo 54 + NativeWind + TypeScript
**Backend**: FastAPI + SQLAlchemy + SQLite/PostgreSQL + OpenAI API

## 개발 가이드

### 로컬 개발
```bash
# 의존성 설치
make install

# Terminal 1
make dev-backend

# Terminal 2
make dev-frontend
```

### Docker 개발
```bash
make build && make up
make logs        # 로그 확인
make down        # 중지
```

### 테스트 & 품질
```bash
make test        # 테스트 실행
make lint        # 코드 린트
make format      # 코드 포맷
```

## 문제 해결

```bash
# 포트 충돌
lsof -ti:8000 | xargs kill
lsof -ti:8081 | xargs kill

# 의존성 재설치
make clean && make install
```

## 개발 상태

**완료**: 프로젝트 구조, Docker 환경, UI 컴포넌트, 채팅 UI, 상태관리, API 서비스

**예정**: 사용자 인증, 프로덕션 배포 , 지도 API 연동

