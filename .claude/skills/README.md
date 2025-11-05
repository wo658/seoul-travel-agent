# Claude Skills - Shared Environment

공통 Python 환경을 사용하는 프로젝트 스킬 모음입니다.

## 환경 설정

### 공통 가상환경 (uv 기반)

모든 스킬은 `.claude/skills/.venv`의 공통 가상환경을 공유합니다.

```bash
# 최초 설정 (자동으로 완료됨)
cd .claude/skills
uv sync

# Playwright 브라우저 설치 (최초 1회)
uv run playwright install chromium
```

### 스킬 실행

스킬 스크립트를 실행할 때는 프로젝트 루트에서 `uv run`을 사용합니다:

```bash
# 프로젝트 루트에서
uv run python .claude/skills/webapp-testing/scripts/with_server.py --help
uv run python .claude/skills/webapp-testing/examples/element_discovery.py
```

## 사용 가능한 스킬

### [webapp-testing](./webapp-testing/SKILL.md)
React Native + Expo 웹 애플리케이션 테스팅을 위한 Playwright 기반 도구 모음

**주요 기능**:
- 서버 자동 관리 (`with_server.py`)
- DOM 요소 검색 및 상호작용
- 스크린샷 및 브라우저 로그 캡처
- E2E 테스팅 자동화

**프로젝트 특화 설정**:
- Backend: `http://localhost:8000` (FastAPI)
- Frontend: `http://localhost:8081` (Expo web)
- 시작: `make webapp`

### issue-workflow-manager
Linear 기반 이슈 워크플로우 관리 스킬

### skill-creator
새로운 스킬 생성 가이드

## 의존성 관리

### 공통 의존성 추가

모든 스킬에서 사용할 패키지를 추가하려면:

```bash
cd .claude/skills
uv add <package-name>
uv sync
```

### 현재 설치된 패키지

- `playwright>=1.40.0` - 브라우저 자동화
- `pytest>=7.4.0` (dev) - 테스팅 프레임워크
- `ruff>=0.1.0` (dev) - 린팅 및 포매팅

## 프로젝트 구조

```
.claude/skills/
├── pyproject.toml          # 공통 의존성 정의
├── uv.lock                 # 의존성 잠금 파일
├── .venv/                  # 공통 가상환경
├── README.md              # 이 문서
├── webapp-testing/        # 웹앱 테스팅 스킬
│   ├── SKILL.md
│   ├── scripts/
│   │   └── with_server.py
│   └── examples/
├── issue-workflow-manager/
└── skill-creator/
```

## 개발 가이드

### 새로운 스크립트 작성

```python
#!/usr/bin/env python3
"""스크립트 설명"""

# uv run python script.py 로 실행됩니다
# 공통 가상환경의 패키지를 자동으로 사용합니다

from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto('http://localhost:8081')
        page.wait_for_load_state('networkidle')
        # ... 작업 수행
        browser.close()

if __name__ == '__main__':
    main()
```

### 테스트 실행

```bash
# pytest 실행
uv run pytest

# 린팅
uv run ruff check .

# 포매팅
uv run ruff format .
```

## 문제 해결

### 가상환경 재생성

```bash
cd .claude/skills
rm -rf .venv uv.lock
uv sync
uv run playwright install chromium
```

### Playwright 브라우저 문제

```bash
# 브라우저 재설치
uv run playwright install chromium --force

# 의존성 확인
uv run playwright install --help
```

### 경로 문제

모든 스크립트는 프로젝트 루트에서 실행해야 합니다:

```bash
# ✅ 올바른 방법
cd /home/whdgns/seoul-travel-agent
uv run python .claude/skills/webapp-testing/scripts/with_server.py

# ❌ 잘못된 방법
cd .claude/skills/webapp-testing
python scripts/with_server.py  # 가상환경 인식 실패
```
