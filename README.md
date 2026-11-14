# 💼 업무 말투 변환기 (BizTalk Antigravity)

> 일상 구어나 거친 초안을 입력하면, 메시지를 받는 상대방의 맥락과 격식에 맞춘 자연스러운 비즈니스 언어로 자동 변환해주는 AI 웹 서비스입니다.

---

## 🌟 주요 기능

- **4대 수신 대상별 맞춤형 어조 변환**:
  - 👔 **상사 / 임원 (`boss`)**: 결론 중심의 두괄식 정중 경어체
  - 🤝 **타팀 동료 (`colleague`)**: 상호 존중과 업무 협조를 구하는 정중한 비즈니스 어조
  - 🌐 **고객 / 외부 (`client`)**: 감사와 신뢰를 주는 서비스 극존칭 어조
  - 👥 **팀 내 동료 (`team`)**: 군더더기 없이 명확하고 간결한 실무 협업 어조
- **원클릭 클립보드 복사**: 변환된 결과를 클릭 한 번으로 메신저나 이메일에 바로 붙여넣기
- **단축키 지원**: `Ctrl + Enter` (또는 `Cmd + Enter`)로 빠른 변환 실행
- **반응형 웹 디자인**: PC와 모바일 디바이스 모두에 최적화된 엔터프라이즈 SaaS 스타일 UI

---

## 🛠️ 기술 스택

| 영역 | 기술 | 설명 |
| :--- | :--- | :--- |
| **프론트엔드** | HTML5, CSS3, Vanilla JavaScript (ES6+) | 가볍고 빠른 단일 페이지 인터페이스 |
| **백엔드** | Python 3.12+, FastAPI, Uvicorn, Pydantic | 비동기 고성능 RESTful API 서버 |
| **AI / LLM** | Upstage Solar-Pro4 (`solar-pro4`), LangChain (1.5+) | 한국어 비즈니스 문맥에 특화된 플래그십 LLM |
| **배포** | Vercel, GitHub | Serverless Function 및 CDN 통합 배포 |

---

## 📁 프로젝트 구조

```text
biztalk_antigravity/
├── backend/
│   ├── main.py                 # FastAPI 진입점, CORS, 정적 라우팅
│   ├── requirements.txt        # 의존성 패키지 명세
│   ├── models/
│   │   └── schemas.py          # Pydantic 요청/응답 스키마
│   ├── prompts/
│   │   └── templates.py        # 4대 대상별 프롬프트 템플릿
│   ├── routers/
│   │   └── convert.py          # /api/convert 라우터
│   └── services/
│       └── tone_converter.py   # LangChain + Solar-Pro4 비즈니스 로직
├── frontend/
│   ├── index.html              # 단일 페이지 메인 화면
│   ├── css/
│   │   └── style.css           # 비즈니스 스타일시트
│   └── js/
│       └── app.js              # 비동기 통신 및 인터랙션 스크립트
├── plan/                       # 각 단계별 실행계획서
├── vercel.json                 # Vercel 배포 라우팅 설정
├── .env                        # 환경 변수 (Git 제외)
├── .gitignore                  # Git 제외 목록
├── AGENTS.md                   # AI 코딩 에이전트 지침서
└── PRD_업무말투변환기.md             # 상세 요구사항 명세서
```

---

## 🚀 로컬 실행 방법

### 1. 가상환경 생성 및 의존성 설치
```powershell
# 가상환경 생성
python -m venv .venv

# 가상환경 활성화 (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# 패키지 설치
pip install -r backend/requirements.txt
```

### 2. 환경 변수(`.env`) 설정
프로젝트 루트에 `.env` 파일을 생성하고 Upstage API 키를 입력합니다:
```env
UPSTAGE_API_KEY=your_upstage_api_key_here
```
> [Upstage Console](https://console.upstage.ai/)에서 API 키를 발급받을 수 있습니다.

### 3. 서버 실행
```powershell
uvicorn backend.main:app --port 8000 --reload
```

- 웹 화면 접속: [http://localhost:8000/](http://localhost:8000/)
- 대화형 Swagger API 문서: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## ☁️ Vercel 배포 가이드

1. **GitHub 레포지토리 연결**:
   - Vercel 대시보드에서 `New Project` 클릭 후 해당 GitHub 레포지토리를 Import합니다.
2. **환경 변수(Environment Variables) 등록**:
   - Vercel 프로젝트 설정의 `Environment Variables` 항목에 아래 키를 추가합니다:
     - `UPSTAGE_API_KEY` : 발급받은 Upstage API 키 값
3. **Deploy 실행**:
   - `Deploy` 버튼을 누르면 `vercel.json` 설정에 따라 백엔드 Serverless Function과 정적 프론트엔드가 자동으로 배포됩니다.
