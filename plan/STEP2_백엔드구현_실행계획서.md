# STEP 2. 백엔드 구현 실행계획서

> **작성일**: 2026-11-14  
> **프로젝트**: 업무 말투 변환기 (`biztalk_antigravity`)  
> **관련 문서**: [PRD_업무말투변환기.md](file:///C:/vibecoding/biztalk_antigravity/PRD_업무말투변환기.md), [AGENTS.md](file:///C:/vibecoding/biztalk_antigravity/AGENTS.md), [STEP1_환경준비_실행계획서.md](file:///C:/vibecoding/biztalk_antigravity/plan/STEP1_환경준비_실행계획서.md)  
> **저장 경로**: `plan/STEP2_백엔드구현_실행계획서.md`

---

## 1. 개요 및 목적

본 문서는 **업무 말투 변환기** 프로젝트의 핵심 백엔드 API 시스템을 구축하는 **STEP 2. 백엔드 구현**의 상세 계획서입니다.
FastAPI 웹 프레임워크와 Upstage의 최신 플래그십 LLM인 **Solar-Pro4 (`solar-pro4`)**, 그리고 LangChain을 연동하여 4대 수신 대상(`boss`, `colleague`, `client`, `team`)에 맞춤형 비즈니스 어조로 텍스트를 실시간 변환하는 RESTful API를 구현하고 로컬에서 완벽히 검증하는 것을 목표로 합니다.

---

## 2. 완료 기준 (Definition of Done)

아래 항목들이 모두 정상 동작하고 검증되었을 때 STEP 2를 완료 처리합니다.

- [x] **1. Pydantic 데이터 모델 (`backend/models/schemas.py`)**
  - `ConvertRequest`: `text`(1자 이상), `target_audience`(boss, colleague, client, team) 유효성 검증
  - `ConvertResponse`: `converted_text`, `target_audience`, `original_text` 규격 정의
- [x] **2. 프롬프트 템플릿 (`backend/prompts/templates.py`)**
  - 4대 대상별 맞춤형 시스템 프롬프트(격식/협조/서비스/실무 어조) 딕셔너리 구축
- [x] **3. LLM 변환 서비스 (`backend/services/tone_converter.py`)**
  - `langchain-upstage`의 `ChatUpstage(model="solar-pro4")` 연동
  - LCEL (`ChatPromptTemplate | ChatUpstage | StrOutputParser`) 체인 파이프라인 구현
  - 예외 처리 및 비즈니스 변환 로직 캡슐화
- [x] **4. API 라우터 (`backend/routers/convert.py`)**
  - `POST /api/convert` 엔드포인트 구현 (정상 응답 200, 422 유효성 검증, 500 LLM 예외 처리)
- [x] **5. FastAPI 메인 앱 (`backend/main.py`)**
  - CORS 미들웨어 (`allow_origins=["*"]`) 설정
  - Health Check (`GET /health` -> `{"status": "ok"}`) 구현
  - 정적 파일 서비스 마운트 (향후 프론트엔드 `index.html` 연동 대비)
  - API 라우터 등록 (`/api`)
- [x] **6. 로컬 서버 기동 및 API 검증**
  - Uvicorn 서버 정상 기동 확인
  - Swagger UI (`http://localhost:8000/docs`) 접속 확인
  - `GET /health` 및 `POST /api/convert` 4종 호출 테스트 통과

---

## 3. 사전 기술 조사 결과 (원칙 2: 조사 먼저, 구현 나중)

### 3.1 Upstage Solar-Pro4 모델 규격 (Context7 공식 문서 기반)
- **공식 모델 식별자**: `solar-pro4` (최신 릴리스: `solar-pro4-260806`)
- **특징**: 에이전트 및 비즈니스/문서 특화 최신 플래그십 모델
- **LangChain 연동 방식**:
  ```python
  from langchain_upstage import ChatUpstage
  from langchain_core.prompts import ChatPromptTemplate
  from langchain_core.output_parsers import StrOutputParser

  # UPSTAGE_API_KEY는 .env 파일에서 자동 로드
  chat = ChatUpstage(model="solar-pro4", temperature=0.3)
  ```

### 3.2 패키지 버전
- `fastapi 0.162.7`
- `uvicorn 0.54.0`
- `langchain 1.5.0`
- `langchain-core 1.8.0`
- `langchain-upstage 0.7.7`
- `pydantic 2.14.3`
- `python-dotenv 1.2.4`

---

## 4. 파일별 세부 구현 설계

### 4.1 `backend/models/schemas.py`
```python
from pydantic import BaseModel, Field
from typing import Literal

TargetAudience = Literal["boss", "colleague", "client", "team"]

class ConvertRequest(BaseModel):
    text: str = Field(..., min_length=1, description="변환할 원문 내용")
    target_audience: TargetAudience = Field(..., description="수신 대상 (boss, colleague, client, team)")

class ConvertResponse(BaseModel):
    converted_text: str = Field(..., description="비즈니스 어조로 변환된 텍스트")
    target_audience: str = Field(..., description="적용된 수신 대상 코드")
    original_text: str = Field(..., description="입력된 원문 내용")
```

### 4.2 `backend/prompts/templates.py`
4대 대상별 비즈니스 어조 정의:
1. **`boss` (상사 / 임원)**:
   - 어조: 정중하고 공손한 최고 수준의 경어체, 결론부터 제시하는 두괄식 보고형
2. **`colleague` (타팀 동료)**:
   - 어조: 상호 존중과 협조를 구하는 정중하고 친절한 비즈니스 어조
3. **`client` (고객 / 외부)**:
   - 어조: 극존칭, 서비스 마인드가 담긴 신뢰감과 감사의 표현
4. **`team` (팀 내 동료)**:
   - 어조: 격식은 낮추되 명확하고 간결한 실무 협업 어조

> [!NOTE]
> AI가 부가적인 설명(예: "네, 변환해 드렸습니다" 등)을 붙이지 않고, **오직 변환된 비즈니스 메시지 본문만 출력**하도록 시스템 프롬프트 제약 조건을 엄격히 설정합니다.

### 4.3 `backend/services/tone_converter.py`
- `.env` 환경 변수 로드 (`dotenv.load_dotenv()`)
- `ChatUpstage(model="solar-pro4")` 싱글톤 또는 팩토리 패턴 구성
- LCEL 체인: `ChatPromptTemplate` → `ChatUpstage` → `StrOutputParser`
- `async def convert_text(text: str, target: str) -> str` 비동기 변환 함수 제공

### 4.4 `backend/routers/convert.py`
- `APIRouter(tags=["tone-conversion"])`
- `POST /convert`:
  - Request Body: `ConvertRequest`
  - Response: `ConvertResponse`
  - 에러 처리: LLM 호출 실패 시 `HTTPException(status_code=500, detail="...")` 반환

### 4.5 `backend/main.py`
- FastAPI 앱 인스턴스 초기화 (`title="업무 말투 변환기 API"`, `version="1.0.0"`)
- CORS 미들웨어 등록
- `GET /health` 엔드포인트: `{"status": "ok"}`
- `api_router` 등록 (`prefix="/api"`)
- 정적 파일 마운트 (향후 `frontend/` 디렉토리를 `/`로 서빙할 수 있도록 사전 구성)

---

## 5. 단계별 실행 절차

```text
[1] schemas.py 작성  ───>  [2] templates.py 작성  ───>  [3] tone_converter.py 작성
                                                                    │
[6] 종합 검증        <───  [5] main.py 연동       <───  [4] routers/convert.py 작성
 (Health, Convert API)
```

1. **Step 2-1**: `backend/models/schemas.py` 작성
2. **Step 2-2**: `backend/prompts/templates.py` 작성
3. **Step 2-3**: `backend/services/tone_converter.py` 작성 및 Upstage 연동 테스트
4. **Step 2-4**: `backend/routers/convert.py` 작성
5. **Step 2-5**: `backend/main.py` 작성 (CORS, 라우터, Health Check)
6. **Step 2-6**: Uvicorn 구동 및 종합 검증 스크립트 실행

---

## 6. 검증 계획 (Verification Plan)

### 6.1 단위 기능 검증
가상환경 Python을 사용하여 변환 서비스 직접 호출 검증:
```powershell
.\.venv\Scripts\python.exe -c "import asyncio; from backend.services.tone_converter import convert_text; print(asyncio.run(convert_text('내일까지 보고서 제출 어려움', 'boss')))"
```

### 6.2 서버 API 통합 검증
1. 백그라운드에서 FastAPI 서버 기동:
   ```powershell
   .\.venv\Scripts\uvicorn.exe backend.main:app --port 8000
   ```
2. `GET /health` 엔드포인트 호출 검증:
   - 기대값: `HTTP 200`, `{"status": "ok"}`
3. `POST /api/convert` 4대 대상별 호출 검증:
   - 대상: `boss`, `colleague`, `client`, `team`
   - 기대값: `HTTP 200`, 올바른 응답 JSON 규격
4. `POST /api/convert` 예외 케이스 검증:
   - 빈 문자열 or 누락된 필드 -> `HTTP 422 Validation Error` 확인

---

## 7. 완료 후 문서 동기화 계획

검증 완료 즉시 [문서 항상 최신화 원칙]에 따라 업데이트:
1. `PRD_업무말투변환기.md`:
   - `## 2. 완료 체크리스트` 백엔드 항목 8종 모두 `[x]` 체크
   - `## 8. 단계별 구현 순서`의 `STEP 2. 백엔드 구현`을 `[x]`로 체크
2. `AGENTS.md`:
   - `## 4. 단계별 작업 절차`의 `STEP 2`를 `[x]`로 체크
3. 본 계획서 (`plan/STEP2_백엔드구현_실행계획서.md`):
   - DoD 항목 전체 완료 체크 (`[x]`)
