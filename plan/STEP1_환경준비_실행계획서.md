# STEP 1. 환경 준비 실행계획서

> **작성일**: 2026-11-14  
> **프로젝트**: 업무 말투 변환기 (`biztalk_antigravity`)  
> **관련 문서**: [PRD_업무말투변환기.md](file:///C:/vibecoding/biztalk_antigravity/PRD_업무말투변환기.md), [AGENTS.md](file:///C:/vibecoding/biztalk_antigravity/AGENTS.md)  
> **저장 경로**: `plan/STEP1_환경준비_실행계획서.md`

---

## 1. 개요 및 목적

본 문서는 **업무 말투 변환기** 프로젝트의 첫 번째 단계인 **STEP 1. 환경 준비**의 세부 실행 계획 및 작업 진행 상태를 정의합니다.
프로젝트의 로컬 개발 기반을 안전하고 격리된 상태로 구성하며, Upstage Solar-Pro4 연동을 위한 의존성 라이브러리를 최신 규격에 맞춰 준비하는 것을 목표로 합니다.

---

## 2. 완료 기준 (Definition of Done)

아래 6개 항목이 모두 충족되면 STEP 1이 완료된 것으로 판단합니다.

- [x] **1. GitHub 레포지토리 연결 확인**: 원격 저장소(`biztalk_antigravity`) 및 `main` 브랜치 연동 상태 확인
- [x] **2. 목표 디렉토리 구조 생성**: `backend/` 하위 모듈 및 `frontend/` 하위 정적 리소스 디렉토리 구성
- [x] **3. `.gitignore` 작성**: `.env`, `.venv/`, `__pycache__/` 등 보안 및 불필요 파일 제외 처리
- [x] **4. `.env` 보안 환경 변수 확인**: Upstage API 키가 정의된 `.env` 파일 배치 및 유출 방지 격리
- [x] **5. `backend/requirements.txt` 작성**: Context7 및 공식 문서를 바탕으로 최신 안정 버전 의존성 명시
- [x] **6. 가상환경 생성 및 의존성 설치/검증**:
  - [x] Python 3.12 기반 `.venv` 가상환경 폴더 생성
  - [x] 가상환경 내 `pip install -r backend/requirements.txt` 실행
  - [x] 주요 패키지(`fastapi`, `langchain_upstage` 등) 정상 로드 검증

---

## 3. 세부 작업 절차 및 현황

### 3.1 GitHub 레포지토리 확인 (완료)
- **상태**: ✅ 완료
- **내용**: `git status` 확인 결과, `origin/main` 브랜치에 정상 연결되어 있음을 확인.

### 3.2 디렉토리 구조 생성 (완료)
- **상태**: ✅ 완료
- **생성된 구조**:
  ```text
  biztalk_antigravity/
  ├── backend/
  │   ├── models/        # Pydantic 데이터 스키마
  │   ├── prompts/       # 4대 대상별 프롬프트 템플릿
  │   ├── routers/       # FastAPI 라우터 (/api/convert)
  │   └── services/      # LangChain + Solar-Pro4 비즈니스 로직
  ├── frontend/
  │   ├── css/           # 스타일시트
  │   └── js/            # 프론트엔드 비동기 통신 로직
  └── plan/              # 실행 계획서 및 분석 문서 보관
  ```

### 3.3 `.gitignore` 설정 (완료)
- **상태**: ✅ 완료
- **적용 내용**:
  ```gitignore
  .env
  .venv/
  __pycache__/
  *.pyc
  .DS_Store
  node_modules/
  ```

### 3.4 `.env` 보안 격리 (완료)
- **상태**: ✅ 완료
- **보안 수칙**:
  - `UPSTAGE_API_KEY`가 포함된 `.env` 파일은 터미널 화면에 내용을 절대 출력하거나 열람하지 않음
  - Git 트래킹 대상에서 완전 제외 확인

### 3.5 `backend/requirements.txt` 작성 (완료)
- **상태**: ✅ 완료
- **선정 근거**: Context7 MCP 도구를 통한 최신 Upstage 연동 문서 확인 및 PyPI 최신 안정 릴리스 버전 반영
- **패키지 명세**:
  ```text
  fastapi>=0.115.0
  uvicorn>=0.34.0
  langchain>=1.5.0
  langchain-upstage>=0.7.7
  python-dotenv>=1.0.1
  pydantic>=2.10.0
  ```

### 3.6 가상환경 구성 및 패키지 설치 (완료)
- **가상환경 생성**: ✅ `.venv` 폴더 생성 완료 (Python 3.12.10)
- **패키지 설치**: ✅ `pip install -r backend/requirements.txt` 성공 완료
- **검증 결과**: ✅ `fastapi`, `uvicorn`, `pydantic`, `dotenv`, `langchain`, `langchain_upstage.ChatUpstage` 정상 임포트 검증 완료 (Exit code: 0)


---

## 4. 검증 계획 (Verification Plan)

패키지 설치 완료 후, 아래 명령어로 환경이 완벽히 준비되었는지 검증합니다:

1. **가상환경 내 파이썬 및 pip 경로 확인**:
   ```powershell
   .\.venv\Scripts\python.exe -c "import sys; print(sys.executable)"
   ```
2. **핵심 라이브러리 정상 임포트 확인**:
   ```powershell
   .\.venv\Scripts\python.exe -c "import fastapi, uvicorn, pydantic, dotenv, langchain; from langchain_upstage import ChatUpstage; print('All Dependencies Loaded Successfully!')"
   ```

---

## 5. 완료 후 문서 최신화 계획

검증이 성공하면 [PRD 및 AGENTS.md 항상 최신화 원칙]에 따라 다음 문서를 업데이트합니다:
1. `PRD_업무말투변환기.md`: `## 8. 단계별 구현 순서`의 `STEP 1. 환경 준비`를 `[x]`로 체크
2. `PRD_업무말투변환기.md`: `## 2. 완료 체크리스트` 중 해당 항목 체크
3. `AGENTS.md`: `## 4. 단계별 작업 절차`의 `STEP 1`을 `[x]`로 체크
