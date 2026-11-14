# STEP 4. 배포 준비 및 검증 실행계획서

> **작성일**: 2026-11-14  
> **프로젝트**: 업무 말투 변환기 (`biztalk_antigravity`)  
> **관련 문서**: [PRD_업무말투변환기.md](file:///C:/vibecoding/biztalk_antigravity/PRD_업무말투변환기.md), [AGENTS.md](file:///C:/vibecoding/biztalk_antigravity/AGENTS.md)  
> **저장 경로**: `plan/STEP4_배포준비_실행계획서.md`

---

## 1. 개요 및 목적

본 문서는 로컬에서 구현 및 검증이 완료된 **업무 말투 변환기**를 실제 웹 환경에 배포하기 위한 **STEP 4. 배포 준비 및 검증**의 상세 실행 계획서입니다.
GitHub 원격 저장소(`origin/main`)에 변경 사항을 안전하게 반영하고, **Vercel** 플랫폼을 통해 프론트엔드 정적 파일과 FastAPI 백엔드를 통합 배포할 수 있도록 설정 파일(`vercel.json`)과 종합 가이드(`README.md`)를 작성합니다.

---

## 2. 완료 기준 (Definition of Done)

[PRD_업무말투변환기.md](file:///C:/vibecoding/biztalk_antigravity/PRD_업무말투변환기.md#L105-L111)의 배포 체크리스트를 기반으로 완료 기준을 수립합니다:

- [x] **1. Vercel 배포 설정 파일 (`vercel.json`) 작성**
  - Python FastAPI 백엔드 런타임 및 Frontend 정적 파일 라우팅 규칙 정의
- [x] **2. 프로젝트 종합 문서 (`README.md`) 작성**
  - 서비스 소개, 아키텍처, 실행 방법, 환경 변수 설정법 및 Vercel 배포 가이드 명시
- [ ] **3. GitHub 원격 저장소 푸시 (`git push origin main`)**
  - 보안 규칙에 따라 사용자 승인을 거쳐 로컬 커밋 내역을 원격 저장소로 동기화
- [ ] **4. Vercel 배포 및 환경 변수 등록 가이드 제공**
  - Vercel 대시보드에서 `UPSTAGE_API_KEY` 환경 변수를 안전하게 등록하는 절차 안내
- [ ] **5. 문서 동기화 최신화**
  - `PRD_업무말투변환기.md` 및 `AGENTS.md`의 배포 항목 체크 (`[x]`)

---

## 3. 사전 기술 조사 및 배포 아키텍처 (원칙 2 준수)

### 3.1 Vercel 배포 구조
Vercel은 Serverless Function 기반으로 Python을 지원하며, 정적 리소스(HTML/CSS/JS)를 글로벌 CDN(Edge Network)을 통해 고속 제공합니다.

- **FastAPI 백엔드**: Vercel의 `@vercel/python` 빌더를 통해 `backend/main.py`의 `app` 인스턴스를 Serverless Function으로 래핑
- **프론트엔드**: `frontend/` 디렉토리의 정적 파일들을 서빙
- **API 상대 경로 호환성**:
  - `frontend/js/app.js`에서 엔드포인트를 `/api/convert`로 호출하고 있으므로, 로컬과 Vercel 배포 환경 양쪽 모두에서 소스 코드 수정 없이 완벽히 동작합니다.

### 3.2 `vercel.json` 라우팅 전략
```json
{
  "builds": [
    {
      "src": "backend/main.py",
      "use": "@vercel/python"
    },
    {
      "src": "frontend/**",
      "use": "@vercel/static"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "backend/main.py"
    },
    {
      "src": "/health",
      "dest": "backend/main.py"
    },
    {
      "src": "/docs",
      "dest": "backend/main.py"
    },
    {
      "src": "/openapi.json",
      "dest": "backend/main.py"
    },
    {
      "src": "/css/(.*)",
      "dest": "frontend/css/$1"
    },
    {
      "src": "/js/(.*)",
      "dest": "frontend/js/$1"
    },
    {
      "src": "/(.*)",
      "dest": "frontend/index.html"
    }
  ]
}
```

---

## 4. 단계별 실행 절차

```text
[1] vercel.json 작성 ──> [2] README.md 작성 ──> [3] 커밋 및 Git Push 승인/실행
                                                         │
[5] 문서 최신화       <── [4] Vercel 배포 절차 안내  <──┘
```

1. **Step 4-1**: 프로젝트 루트에 `vercel.json` 생성
2. **Step 4-2**: 루트에 `README.md` 생성 (프로젝트 설명, 로컬 실행법, Vercel 배포 가이드)
3. **Step 4-3**: 변경 사항 커밋 후, 사용자에게 원격 푸시(`git push origin main`) 명시적 확인 요청 및 실행
4. **Step 4-4**: Vercel 대시보드 연결 및 `UPSTAGE_API_KEY` 환경 변수 설정 가이드 안내
5. **Step 4-5**: [PRD_업무말투변환기.md](file:///C:/vibecoding/biztalk_antigravity/PRD_업무말투변환기.md) 및 [AGENTS.md](file:///C:/vibecoding/biztalk_antigravity/AGENTS.md) 최신화

---

## 5. 보안 및 안전 관리 수칙

- **`.env` 절대 푸시 금지**: `.gitignore`에 등록되어 있는지 재차 확인하여 API 키가 GitHub에 공개되지 않도록 엄격히 격리합니다.
- **Git Push 사전 확인**: 글로벌 지침 §4-1에 따라 사용자의 명시적 동의 하에만 푸시 명령을 실행합니다.
