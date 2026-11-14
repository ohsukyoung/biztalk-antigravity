import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from backend.routers import convert

# 기본 경로 설정
BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

app = FastAPI(
    title="업무 말투 변환기 (BizTalk Antigravity) API",
    description="일상 언어를 상황과 수신자에 맞는 비즈니스 언어로 자동 변환해주는 서비스 API입니다.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# 1. CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 배포 환경 시 필요에 따라 특정 도메인으로 제한 가능
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Health Check 엔드포인트
@app.get("/health", tags=["시스템 점검"])
async def health_check():
    """서버 상태 점검 (Health Check)"""
    return {"status": "ok"}

# 3. 비즈니스 API 라우터 등록
app.include_router(convert.router, prefix="/api")

# 4. 프론트엔드 정적 파일 서빙 (Single Page Routing)
if FRONTEND_DIR.exists():
    # css, js 디렉토리가 있으면 정적 마운트
    css_dir = FRONTEND_DIR / "css"
    js_dir = FRONTEND_DIR / "js"
    if css_dir.exists():
        app.mount("/css", StaticFiles(directory=str(css_dir)), name="css")
    if js_dir.exists():
        app.mount("/js", StaticFiles(directory=str(js_dir)), name="js")

    @app.get("/", include_in_schema=False)
    async def serve_index():
        """루트 경로 접속 시 frontend/index.html 서빙"""
        index_file = FRONTEND_DIR / "index.html"
        if index_file.exists():
            return FileResponse(index_file)
        return {
            "message": "업무 말투 변환기 백엔드 서버가 정상 동작 중입니다.",
            "docs": "/docs",
            "health": "/health"
        }
