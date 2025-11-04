# 🏯 Seoul Travel Agent

AI 기반 서울 여행 계획 도우미 - React Native + FastAPI

LLM 기반 대화형 인터페이스로 맞춤형 서울 여행 계획을 생성합니다.

## 🚀 빠른 시작

### Docker로 웹 뷰 테스트 (권장)

```bash
# 1. 환경 변수 설정 (선택사항)
echo 'OPENAI_API_KEY=your-key-here' >> backend/.env.docker

# 2. 서비스 시작
make web

# 3. 브라우저에서 확인
# 웹앱: http://localhost:3000
# API: http://localhost:8000/api/docs
```

**상세 가이드**: [QUICKSTART.md](./QUICKSTART.md) | [DOCKER_WEB_SETUP.md](./DOCKER_WEB_SETUP.md)

---

## 📚 프로젝트 개요

### 주요 기능

- ✅ **채팅 인터페이스**: 자연어로 여행 선호도 입력
- 🤖 **AI 대화**: LLM 기반 실시간 응답 (스트리밍)
- 📅 **여행 계획 생성**: 대화 기반 맞춤형 일정 생성
- 💾 **대화 히스토리**: 모든 대화 저장 및 이어가기

### 기술 스택

**Frontend**
- React Native 0.81.5 + Expo 54
- NativeWind (Tailwind CSS)
- TypeScript
- Context API (상태 관리)

**Backend**
- FastAPI (Python 3.13)
- SQLAlchemy 2.0 (ORM)
- PostgreSQL / SQLite
- OpenAI API / Anthropic API

**Infrastructure**
- Docker + Docker Compose
- uv (Python 패키지 관리)

---

## 🏗️ 프로젝트 구조

```
seoul-travel-agent/
├── frontend/                    # React Native (Expo)
│   ├── src/
│   │   ├── components/
│   │   │   ├── ui/             # 재사용 UI 컴포넌트
│   │   │   │   ├── button.tsx
│   │   │   │   ├── card.tsx
│   │   │   │   ├── input.tsx
│   │   │   │   └── ...
│   │   │   └── chat/           # 채팅 컴포넌트 ✅
│   │   │       ├── MessageBubble.tsx
│   │   │       ├── MessageInput.tsx
│   │   │       └── StreamingIndicator.tsx
│   │   ├── screens/            # 화면 컴포넌트 ✅
│   │   │   ├── HomeScreen.tsx
│   │   │   ├── ChatScreen.tsx
│   │   │   └── ConversationListScreen.tsx
│   │   ├── contexts/           # 상태 관리 ✅
│   │   │   └── ChatContext.tsx
│   │   ├── hooks/              # 커스텀 훅 ✅
│   │   │   └── useChat.ts
│   │   ├── services/           # API 서비스 ✅
│   │   │   └── api/chat.ts
│   │   └── types/              # TypeScript 타입 ✅
│   │       └── chat.ts
│   └── App.tsx                 # 메인 앱 ✅
│
├── backend/                     # FastAPI
│   ├── src/seoul_travel/
│   │   ├── main.py             # FastAPI 앱
│   │   ├── ai/                 # LLM 통합 (TODO)
│   │   │   ├── service.py
│   │   │   ├── prompts.py
│   │   │   └── router.py
│   │   ├── auth/               # 인증 모델
│   │   └── plan/               # 여행 계획 모델
│   ├── .env.example
│   └── Dockerfile
│
├── docker-compose.yml          # Docker Compose 설정
├── Makefile                    # 개발 명령어
├── QUICKSTART.md               # 빠른 시작 가이드
└── DOCKER_WEB_SETUP.md         # Docker 웹 가이드
```

---

## 🛠️ 개발 가이드

### 로컬 개발 (빠른 개발)

```bash
# 의존성 설치
make install

# Terminal 1 - 백엔드
make dev-backend

# Terminal 2 - 프론트엔드
make dev-frontend
```

### Docker 개발 (전체 스택)

```bash
# 빌드 및 시작
make build
make up

# 로그 확인
make logs

# 중지
make down
```

### 유용한 명령어

```bash
make help           # 모든 명령어 확인
make test           # 테스트 실행
make lint           # 코드 린트
make format         # 코드 포맷
make clean          # 리소스 정리
```

---

## 📖 API 문서

서비스 실행 후 다음 URL에서 확인:
- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

### 주요 엔드포인트 (예정)

```
POST   /api/ai/conversations              # 새 대화 시작
GET    /api/ai/conversations              # 대화 목록
GET    /api/ai/conversations/{id}         # 대화 조회
POST   /api/ai/conversations/{id}/messages/stream  # 스트리밍 채팅
POST   /api/ai/conversations/{id}/generate-plan    # 여행 계획 생성
```

---

## 🧪 테스트

```bash
# 백엔드 테스트
make test-backend

# 프론트엔드 테스트 (예정)
cd frontend && npm test
```

---

## 📝 개발 상태

### ✅ 완료
- [x] 프로젝트 기본 구조 설정
- [x] Docker 개발 환경 구축
- [x] UI 컴포넌트 시스템 (NativeWind)
- [x] 채팅 UI 컴포넌트
- [x] 채팅 상태 관리 (Context)
- [x] API 서비스 레이어
- [x] 화면 네비게이션

### 🚧 진행 중
- [ ] 백엔드 AI 서비스 구현
- [ ] 대화 API 엔드포인트
- [ ] SSE 스트리밍 구현
- [ ] 데이터베이스 마이그레이션

### 📋 예정
- [ ] 여행 계획 생성 기능
- [ ] 사용자 인증
- [ ] 프로덕션 배포
- [ ] 모바일 앱 빌드 (iOS/Android)

---

## 🤝 기여

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 라이선스

This project is licensed under the MIT License.

---

## 🔗 관련 문서

- [Quick Start Guide](./QUICKSTART.md)
- [Docker Web Setup](./DOCKER_WEB_SETUP.md)
- [Frontend README](./frontend/README.md)
- [Backend README](./backend/README.md)

---

## 📞 문의

프로젝트에 대한 질문이나 제안사항이 있으시면 이슈를 생성해주세요.
