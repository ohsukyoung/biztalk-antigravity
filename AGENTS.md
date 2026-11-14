# AGENTS.md — Antigravity 개발 및 협업 가이드

이 문서는 **업무 말투 변환기(`biztalk_antigravity`)** 프로젝트를 개발할 때, AI 코딩 에이전트(Antigravity)가 반드시 준수해야 하는 행동 규칙, 개발 원칙, 기술 스택 및 프로젝트 아키텍처 개요를 정의합니다.

---

## 1. 프로젝트 개요 (Project Overview)

### 1.1 서비스 소개
- **프로젝트명**: 업무 말투 변환기 (BizTalk Antigravity)
- **개념**: 사용자가 일상적인 구어나 거친 문장을 입력하면, 수신자(상사, 타팀 동료, 고객, 팀 동료)의 맥락과 격식에 맞춘 자연스러운 비즈니스 언어로 자동 변환해주는 웹 서비스입니다.
- **실습 형태**: 바이브 코딩(Vibe Coding) 기반의 One Day MVP(작동하는 서비스) 구축 프로젝트.

### 1.2 핵심 타깃 및 변환 페르소나
| 대상 코드 (`target_audience`) | 수신 대상 | 변환 스타일 및 어조 |
| :--- | :--- | :--- |
| `boss` | 상사 / 임원 | 격식 있고 공손한 정중 경어체 |
| `colleague` | 타팀 동료 | 정중하면서도 상호 협조적인 비즈니스 어조 |
| `client` | 고객 / 외부 | 친절하고 전문적이며 신뢰감을 주는 서비스 어조 |
| `team` | 팀 내 동료 | 간결하고 명확하며 실무적인 어조 |

### 1.3 범위 정의 (Scope)
- **In-Scope (오늘 구현할 기능)**:
  - 단일 웹 화면(텍스트 입력, 대상 선택 4종, 변환 실행 버튼, 결과 복사, 로딩 상태 표시)
  - FastAPI 기반 백엔드 API (`POST /api/convert`, `GET /health`, Swagger UI `/docs`)
  - Upstage Solar-Pro4(`solar-pro`) LLM 및 LangChain 연동
  - Vercel 배포 준비
- **Out-of-Scope (절대 임의로 추가하지 말 것)**:
  - 사용자 로그인 / 인증 및 회원가입
  - 데이터베이스(DB) 연결 및 변환 히스토리 영구 저장
  - 복잡한 상태 관리 프레임워크나 외부 UI 라이브러리 도입
  - 과도한 에러 재시도 로직이나 불필요한 마이크로서비스화

---

## 2. 기술 스택 및 디렉토리 구조

### 2.1 기술 스택
- **프론트엔드**: HTML5, CSS3, Vanilla JavaScript (ES6+ / 프레임워크 미사용)
- **백엔드**: Python 3.11+, FastAPI, Uvicorn, Pydantic, python-dotenv
- **AI / LLM 연동**: LangChain, `langchain-upstage`, Upstage Solar-Pro4 (`solar-pro`)
- **환경 관리**: Python Virtualenv (`.venv`)
- **배포 및 버전 관리**: Git, GitHub, Vercel

### 2.2 목표 디렉토리 구조
```text
biztalk_antigravity/
├── .agents/                    # 에이전트 스킬 및 MCP 구성
│   ├── mcp_config.json
│   └── skills/
│       ├── frontend-design/
│       └── karpathy-guidelines/
├── .venv/                      # Python 가상환경 (Git 제외)
├── backend/
│   ├── main.py                 # FastAPI 앱 진입점, CORS, 정적 파일 라우팅
│   ├── requirements.txt        # 백엔드 의존성 목록
│   ├── models/
│   │   └── schemas.py          # Pydantic 요청/응답 스키마
│   ├── prompts/
│   │   └── templates.py        # 4대 대상별 프롬프트 템플릿
│   ├── routers/
│   │   └── convert.py          # /api/convert 라우터 정의
│   └── services/
│       └── tone_converter.py   # LangChain + Solar-Pro4 비즈니스 로직
├── frontend/
│   ├── index.html              # 단일 페이지 인터페이스
│   ├── css/
│   │   └── style.css           # UI 스타일시트
│   └── js/
│       └── app.js              # 이벤트 처리 및 Fetch API 통신
├── .env                        # API 키 등 보안 변수 (절대 Git 커밋 금지)
├── .gitignore                  # .env, .venv, __pycache__ 등 제외
├── AGENTS.md                   # 에이전트 지침서 (본 문서)
├── PRD_업무말투변환기.md             # 상세 요구사항 명세서
└── 개요서_업무말투변환기.md           # 기획 개요서
```

### 2.3 API 명세 요약
- `POST /api/convert`
  - Request: `{"text": string, "target_audience": "boss" | "colleague" | "client" | "team"}`
  - Response (200): `{"converted_text": string, "target_audience": string, "original_text": string}`
  - Error (422): 입력값 누락 유효성 실패
  - Error (500): LLM API 연동 예외
- `GET /health`
  - Response: `{"status": "ok"}`

---

## 3. Antigravity 핵심 개발 지침 (Rules for AI Agent)

Antigravity는 이 프로젝트에서 코드를 생성·수정하거나 명령을 실행할 때 아래의 규칙을 엄격하게 지켜야 합니다.

### 3.1 바이브 코딩 3대 원칙
1. **완료 기준을 먼저 정의하라 (Definition of Done First)**:
   - PRD의 완료 체크리스트 항목에 정의된 범위만 구현합니다.
   - 요청받지 않은 "멋져 보이는" 추가 기능(다크모드 토글, 음성 변환, 세션 스토리지 저장 등)을 자의적으로 추가하지 않습니다.
2. **조사 먼저, 구현 나중 (Investigate First, Code Later)**:
   - Upstage Solar-Pro4 연동 및 최신 `langchain-upstage` 패키지의 인터페이스 규격을 먼저 확인한 뒤 코드를 작성합니다.
   - 추측에 의존해 구버전 문법을 적용하지 않으며, 필요 시 공식 명세나 MCP를 참고합니다.
3. **버그는 분석 먼저, 수정 나중 (Analyze Cause First, Fix Later)**:
   - 에러 발생 시(예: CORS 에러, 422 Validation Error 등), 즉시 코드를 무작정 고치지 않고 **에러의 근본 원인을 사용자에게 먼저 설명**한 후 정밀하게 수정합니다.

### 3.2 Karpathy 코딩 원칙 (Pragmatic & Surgical)
- **외과 수술식 변경 (Surgical Changes)**: 수정이 필요한 코드 블록만 정확히 수정합니다. 주변의 무관한 코드나 포맷을 대규모로 뒤흔들지 않습니다.
- **단순함 유지 (Anti-Overengineering)**:
  - 바닐라 JS와 간단한 FastAPI 구조를 유지합니다.
  - 불필요한 클래스 계층, 과도한 추상 팩토리, 불필요한 유틸리티 함수 생성을 지양합니다.
- **가정 노출 (Surface Assumptions)**: 모호한 기술적 선택지가 있을 경우, 임의로 결정하지 않고 사용자에게 옵션과 가정을 제시합니다.

### 3.3 프론트엔드 디자인 원칙 (.agents/skills/frontend-design)
- Generic한 기본 템플릿(흔한 보라색 그라디언트, 무개성한 카드 디자인)을 피하고, **깔끔하고 신뢰감을 주는 비즈니스 도구 룩앤필**을 구성합니다.
- 충분한 여백, 명확한 타이포그래피 위계, 상태 전환(로딩, 성공, 복사 완료 알림) 피드백을 인터랙티브하게 제공합니다.

### 3.4 보안 및 환경 격리 지침 (절대 금지 사항)
- **`.env` 파일 보호**:
  - `.env` 파일의 내용을 화면/터미널에 출력하거나 유출하지 않습니다.
  - `.gitignore`에 `.env`와 `.venv`가 반드시 포함되어 있는지 항상 확인합니다.
- **파괴적 명령 금지**:
  - `git push --force`, `git reset --hard`, `rm -rf` 등의 비가역적 명령은 절대 실행하지 않습니다.
- **가상환경 준수**:
  - 패키지 설치 시 시스템 전역이 아닌 프로젝트 루트의 `.venv` 가상환경 내에 설치되도록 주의합니다.

---

## 4. 단계별 작업 절차 (Workflow Checklist)

Antigravity는 사용자와 개발을 진행할 때 아래 단계를 순차적으로 밟아 진행해야 합니다:

- [x] **STEP 1. 환경 및 디렉토리 준비**
  - [x] 폴더 구조(`backend`, `frontend`, `plan`) 생성
  - [x] `.gitignore` 갱신 (`.env`, `.venv`, `__pycache__` 등)
  - [x] `backend/requirements.txt` 작성 및 가상환경 세팅 및 검증 완료
- [ ] **STEP 2. 백엔드 구현 (FastAPI + Upstage)**
  - `schemas.py` 모델 정의
  - `templates.py` 4대 페르소나 시스템 프롬프트 작성
  - `tone_converter.py`에 Solar-Pro4 연동 로직 작성
  - `convert.py` 라우터 및 `main.py` CORS/Static 설정
  - 로컬 서버 구동 및 Swagger UI(`/docs`) 검증
- [ ] **STEP 3. 프론트엔드 구현 (HTML/CSS/JS)**
  - `index.html` 시맨틱 구조 작성
  - `style.css` 비즈니스 룩앤필 디자인 적용
  - `app.js` API 비동기 통신, 버튼 상태 토글, 복사 기능 구현
- [ ] **STEP 4. 배포 준비 및 검증**
  - 프론트-백엔드 연동 종합 테스트
  - Vercel 배포 설정 (`vercel.json` 등 필요 시) 점검
  - README / 문서 정리

---

## 5. 자주 사용하는 명령어 참고

```bash
# 가상환경 활성화 (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# 의존성 설치
pip install -r backend/requirements.txt

# 백엔드 서버 로컬 실행 (포트 8000)
cd backend
uvicorn main:app --reload --port 8000

# Swagger 문서 접속
# http://localhost:8000/docs
```

---

## 6. PRD 및 AGENTS.md 문서 항상 최신화 원칙

프로젝트 진행 중 변경사항이 발생하거나 작업이 완료될 때마다 문서를 실시간으로 동기화합니다:

1. **변경사항 즉시 반영**:
   - 기능, 요구사항, 화면 명세, 소스 코드 구조, 라이브러리 및 버전 변경 등이 발생하면 관련 마크다운 문서(`PRD_업무말투변환기.md`, `AGENTS.md`)를 즉시 업데이트합니다.
2. **완료 체크리스트 동기화**:
   - 단위 기능이 구현될 때마다 `PRD_업무말투변환기.md`의 `## 2. 완료 체크리스트`에 `[x]` 체크표시를 남깁니다.
3. **단계별 구현 순서 추적**:
   - 각 개발 단계가 완료되면 `PRD_업무말투변환기.md`의 `## 8. 단계별 구현 순서` 항목에 `[x]` 체크표시를 반영하여 진행 상태를 최신으로 유지합니다.

---

## 7. 계획서(Plan).md 문서의 저장 위치

- 모든 계획서(플랜) 마크다운 문서는 **프로젝트 루트 아래 `plan/` 폴더**(`biztalk_antigravity/plan/`)를 생성하여 작성 및 보관합니다.
- 복잡하거나 다중 파일에 영향을 주는 작업 전 수립하는 구현 계획 문서는 이 폴더 내에 체계적으로 기록합니다.


---

## 7. 계획서(Plan).md 문서의 저장 위치
* 계획서(플랜).md 문서는 모두 현재 프로젝트 루트 아래에 plan 폴더를 생성하여 작성한다.
