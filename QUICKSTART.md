# 🚀 Seoul Travel Agent - Quick Start

## 📦 옵션 1: Docker로 시작 (권장 - 웹 뷰 테스트)

가장 간단하고 빠른 방법입니다. 모든 서비스가 자동으로 설정됩니다.

### 1단계: 환경 변수 설정

```bash
# OpenAI API Key 설정 (선택사항)
echo 'OPENAI_API_KEY=your-key-here' >> backend/.env.docker
```

### 2단계: Docker 실행

```bash
# 모든 서비스 빌드 및 시작
make build
make up
```

### 3단계: 브라우저에서 확인

- **웹앱**: http://localhost:3000
- **API 문서**: http://localhost:8000/api/docs

### 로그 확인

```bash
# 모든 서비스 로그
make logs

# 프론트엔드 로그만
make logs-frontend

# 백엔드 로그만
make logs-backend
```

### 중지

```bash
make down
```

---

## 💻 옵션 2: 로컬 개발 (빠른 개발)

Hot reload가 더 빠르고, 디버깅이 쉽습니다.

### 1단계: 의존성 설치

```bash
make install
```

또는 개별적으로:
```bash
# 백엔드
cd backend
uv pip install -e ".[dev]"

# 프론트엔드
cd frontend
npm install
```

### 2단계: 환경 변수 설정

```bash
# backend/.env 파일 생성
cp backend/.env.example backend/.env

# OpenAI API Key 설정
echo 'OPENAI_API_KEY=your-key-here' >> backend/.env
```

### 3단계: 서비스 실행

**Terminal 1 - 백엔드**:
```bash
make dev-backend
# 또는
cd backend && uvicorn seoul_travel.main:app --reload --port 8000
```

**Terminal 2 - 프론트엔드**:
```bash
make dev-frontend
# 또는
cd frontend && npm run web
```

### 4단계: 브라우저에서 확인

- **웹앱**: http://localhost:8081 (또는 Expo가 표시하는 포트)
- **API**: http://localhost:8000
- **API 문서**: http://localhost:8000/api/docs

---

## 🧪 테스트 시나리오

### 1. 홈 화면 테스트
1. 웹앱 접속
2. "새 대화 시작" 버튼 클릭
3. 채팅 화면으로 이동 확인

### 2. 채팅 테스트 (백엔드 구현 후)
1. 메시지 입력: "3일간 서울 여행 계획 도와줘"
2. 전송 버튼 클릭
3. AI 응답 확인

### 3. API 직접 테스트
```bash
curl http://localhost:8000/health
```

---

## 📁 프로젝트 구조

```
seoul-travel-agent/
├── backend/                 # FastAPI 백엔드
│   ├── src/
│   │   └── seoul_travel/
│   │       ├── main.py     # FastAPI 앱
│   │       ├── ai/         # LLM 통합 (TODO)
│   │       ├── auth/       # 인증 모델
│   │       └── plan/       # 여행 계획 모델
│   ├── .env.example        # 환경 변수 예제
│   ├── .env.docker         # Docker 환경 변수
│   └── Dockerfile
├── frontend/               # React Native (Expo)
│   ├── src/
│   │   ├── components/
│   │   │   ├── ui/        # 재사용 UI 컴포넌트
│   │   │   └── chat/      # 채팅 컴포넌트 ✅
│   │   ├── screens/       # 화면 컴포넌트 ✅
│   │   ├── contexts/      # 상태 관리 ✅
│   │   ├── hooks/         # 커스텀 훅 ✅
│   │   ├── services/      # API 서비스 ✅
│   │   └── types/         # TypeScript 타입 ✅
│   ├── App.tsx            # 메인 앱 ✅
│   └── Dockerfile
├── docker-compose.yml      # Docker Compose 설정
├── Makefile               # 개발 명령어
├── DOCKER_WEB_SETUP.md    # Docker 웹 가이드
└── QUICKSTART.md          # 이 파일
```

---

## 🛠️ 유용한 명령어

### Docker 명령어

```bash
make build          # Docker 이미지 빌드
make up             # 서비스 시작
make down           # 서비스 중지
make restart        # 재시작
make logs           # 로그 확인
make ps             # 컨테이너 상태
make clean          # 모든 리소스 정리
```

### 개발 명령어

```bash
make dev-backend    # 백엔드만 실행
make dev-frontend   # 프론트엔드만 실행
make test           # 테스트 실행
make lint           # 코드 린트
make format         # 코드 포맷
```

### 데이터베이스 명령어

```bash
make db-migrate msg="description"  # 마이그레이션 생성
make db-upgrade                    # 마이그레이션 적용
make db-shell                      # DB 셸 접속
```

---

## 📚 다음 단계

### 백엔드 개발
1. [ ] AI 서비스 구현 (`backend/src/seoul_travel/ai/`)
2. [ ] 대화 API 엔드포인트 구현
3. [ ] SSE 스트리밍 구현
4. [ ] 데이터베이스 마이그레이션

### 프론트엔드 개선
1. [x] 채팅 UI 컴포넌트
2. [x] 상태 관리 (Context)
3. [x] API 서비스 레이어
4. [ ] SSE 라이브러리 통합
5. [ ] 에러 처리 개선

### 배포
1. [ ] 환경 변수 관리
2. [ ] 프로덕션 빌드
3. [ ] CI/CD 설정

---

## 🐛 문제 해결

### 포트 충돌
```bash
# 사용 중인 포트 확인
lsof -i :3000
lsof -i :8000

# Docker 포트 변경
vim docker-compose.yml
```

### 의존성 문제
```bash
# 캐시 정리 및 재설치
cd frontend
rm -rf node_modules package-lock.json
npm install

cd ../backend
uv pip install -e ".[dev]" --force-reinstall
```

### Docker 문제
```bash
# Docker 리소스 정리
make clean
docker system prune -a
```

---

## 🔗 참고 문서

- [DOCKER_WEB_SETUP.md](./DOCKER_WEB_SETUP.md) - Docker 웹 테스트 상세 가이드
- [Frontend README](./frontend/README.md) - 프론트엔드 문서
- [Backend README](./backend/README.md) - 백엔드 문서

## 💡 팁

1. **개발 속도**: 로컬 개발이 Docker보다 빠릅니다
2. **웹 테스트**: Docker가 전체 스택 테스트에 편리합니다
3. **Hot Reload**: 두 방식 모두 지원합니다
4. **디버깅**: 로컬 개발이 디버깅하기 쉽습니다
