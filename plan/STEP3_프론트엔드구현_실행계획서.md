# STEP 3. 프론트엔드 구현 실행계획서

> **작성일**: 2026-11-14  
> **프로젝트**: 업무 말투 변환기 (`biztalk_antigravity`)  
> **관련 문서**: [PRD_업무말투변환기.md](file:///C:/vibecoding/biztalk_antigravity/PRD_업무말투변환기.md), [AGENTS.md](file:///C:/vibecoding/biztalk_antigravity/AGENTS.md)  
> **저장 경로**: `plan/STEP3_프론트엔드구현_실행계획서.md`

---

## 1. 개요 및 목적

본 문서는 **업무 말투 변환기**의 사용자 접점인 웹 프론트엔드 인터페이스를 구축하는 **STEP 3. 프론트엔드 구현**의 상세 계획서입니다.
외부 프레임워크(React/Vue 등) 없이 순수 **HTML5, CSS3, Vanilla JavaScript(ES6+)** 만을 사용하여 가볍고 빠른 Single Page Interface(SPI)를 제작합니다.
사용자가 하고 싶은 말을 입력하고 4대 수신 대상(`boss`, `colleague`, `client`, `team`)을 선택한 후, 백엔드 API (`POST /api/convert`)와 비동기 통신하여 변환 결과를 실시간으로 확인하고 원클릭 복사할 수 있는 직관적인 UI/UX를 완성합니다.

---

## 2. 완료 기준 (Definition of Done)

[PRD_업무말투변환기.md](file:///C:/vibecoding/biztalk_antigravity/PRD_업무말투변환기.md#L96-L104)의 프론트엔드 체크리스트를 기반으로 완료 기준을 정의합니다:

- [x] **1. 시맨틱 HTML 구조 (`frontend/index.html`)**
  - 원문 텍스트 입력창 (`textarea`, 최소 1자 이상 입력 안내)
  - 4대 수신 대상 선택 버튼 그룹 (`boss`, `colleague`, `client`, `team`)
  - [말투 변환하기] 실행 버튼
  - 처리 중 로딩 인디케이터 (스피너 및 처리 상태 안내)
  - 변환 결과 출력 영역 (읽기 전용 `textarea` 또는 카드)
  - [복사하기 📋] 원클릭 클립보드 복사 버튼
- [x] **2. 신뢰감 있는 비즈니스 UI/UX 스타일링 (`frontend/css/style.css`)**
  - 프론트엔드 디자인 원칙 준수 (흔한 템플릿 탈피, 정돈되고 세련된 비즈니스 툴 룩앤필)
  - 명확한 시각적 위계 (헤더, 대상 선택 바, 입력/출력 듀얼 패널)
  - 활성화된 수신 대상 버튼의 명확한 시각 피드백 (`.active`)
  - 로딩 애니메이션 및 버튼 비활성화(`disabled`) 상태 처리
  - 모바일 및 태블릿 반응형 레이아웃 대응
- [x] **3. 비동기 상호작용 및 이벤트 처리 (`frontend/js/app.js`)**
  - 수신 대상 버튼 단일 선택 토글 로직
  - `fetch('/api/convert')` 비동기 API 통신 연동
  - 로딩 상태 토글 (버튼 텍스트 변경, 스피너 노출, 중복 클릭 방지)
  - `navigator.clipboard.writeText()` 기반 클립보드 복사 및 성공 피드백(토스트/버튼 변경)
  - 입력값 검증 (빈 문자열 체크) 및 사용자 친화적 에러 알림
- [x] **4. 백엔드 연동 및 브라우저 실기동 검증**
  - `http://localhost:8000/` 접속 시 메인 웹 화면 정상 렌더링 확인
  - 4개 수신 대상별 실제 변환 동작 및 복사 기능 검증

---

## 3. UI/UX 디자인 방향성 (.agents/skills/frontend-design)

- **디자인 톤앤매너**:
  - 금융/엔터프라이즈 SaaS(Linear, Slack, Notion 등)를 연상시키는 단정하고 신뢰감 있는 슬레이트/네이비 톤
  - 배경: 은은하고 차분한 라이트 그레이 (`#f8fafc`)
  - 포인트 컬러: 프로페셔널한 비즈니스 딥 블루/인디고 (`#2563eb`, `#1e40af`)
  - 폰트: 깔끔한 시스템 산세리프 폰트 스택 (`Pretendard`, `-apple-system`, `BlinkMacSystemFont`, `Segoe UI`)
- **컴포넌트 레이아웃**:
  - 상단: 서비스 헤더 (타이틀 및 간단한 슬로건)
  - 중앙 상단: 4대 수신 대상 탭형 셀렉터 (아이콘 + 직관적인 레이블)
  - 중앙 본문: 좌우 2분할(데스크톱) 또는 상하 2분할(모바일)의 입력(Input) 및 결과(Output) 카드
  - 하단: 액션 버튼 그룹 (변환하기, 복사하기) 및 상태 알림 토스트

---

## 4. 파일별 세부 구현 설계

### 4.1 `frontend/index.html`
- 시맨틱 마크업 (`<header>`, `<main>`, `<section>`, `<footer>`)
- 4대 대상 선택자 버튼 (`data-target="boss"`, `data-target="colleague"`, `data-target="client"`, `data-target="team"`)
- 원문 입력창 (`#inputText`, `placeholder="상사나 동료에게 보낼 내용을 편하게 작성하세요. (예: 내일까지 보고서 제출 어려울 것 같음)"`)
- 변환 실행 버튼 (`#convertBtn`)
- 결과 영역 (`#outputText`, 읽기 전용)
- 복사 버튼 (`#copyBtn`)
- 복사 완료 피드백 토스트 (`#toast`)

### 4.2 `frontend/css/style.css`
- Modern CSS Reset & CSS Variables 정의
- Flexbox 및 Grid 기반 반응형 카드 레이아웃
- 수신 대상 버튼의 호버 및 액티브 애니메이션 트랜지션
- 스피너 애니메이션 (`@keyframes spin`)
- 복사 성공 토스트 애니메이션 (페이드인/아웃)

### 4.3 `frontend/js/app.js`
- 상태 관리 (현재 선택된 대상: 기본값 `boss`)
- 이벤트 리스너 등록:
  - 대상 버튼 클릭 시 `.active` 클래스 토글
  - 변환 버튼 클릭 시 `convertTone()` 비동기 함수 실행
  - 복사 버튼 클릭 시 `copyResult()` 함수 실행
  - 단축키 지원 (`Ctrl + Enter` 또는 `Cmd + Enter` 입력 시 바로 변환 실행)
- 에러 핸들링 및 로딩 상태 제어 함수 (`setLoading(isLoading)`)

---

## 5. 단계별 실행 절차

```text
[1] index.html 작성  ───>  [2] style.css 작성  ───>  [3] app.js 작성
                                                             │
[5] 문서 최신화      <───  [4] 브라우저 실기동 종합 검증 <───┘
```

1. **Step 3-1**: `frontend/index.html` 마크업 구조 작성
2. **Step 3-2**: `frontend/css/style.css` 비즈니스 UI 스타일링 작성
3. **Step 3-3**: `frontend/js/app.js` 비동기 API 통신 및 인터랙션 스크립트 작성
4. **Step 3-4**: 브라우저 실기동 검증 (`http://localhost:8000/` 접속하여 실제 텍스트 변환, 대상 변경, 복사 기능 전수 테스트)
5. **Step 3-5**: [PRD_업무말투변환기.md](file:///C:/vibecoding/biztalk_antigravity/PRD_업무말투변환기.md) 및 [AGENTS.md](file:///C:/vibecoding/biztalk_antigravity/AGENTS.md) 체크리스트 최신화

---

## 6. 완료 후 문서 최신화 계획

검증 완료 즉시 [문서 항상 최신화 원칙]에 따라 다음 문서를 업데이트합니다:
1. `PRD_업무말투변환기.md`:
   - `## 2. 완료 체크리스트` 프론트엔드 항목 6종 모두 `[x]` 체크
   - `## 8. 단계별 구현 순서`의 `STEP 3. 프론트엔드 구현`을 `[x]`로 체크
2. `AGENTS.md`:
   - `## 4. 단계별 작업 절차`의 `STEP 3`을 `[x]`로 체크
3. 본 계획서 (`plan/STEP3_프론트엔드구현_실행계획서.md`):
   - DoD 항목 전체 완료 체크 (`[x]`)
