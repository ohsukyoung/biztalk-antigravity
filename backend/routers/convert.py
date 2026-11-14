import logging
from fastapi import APIRouter, HTTPException, status
from backend.models.schemas import ConvertRequest, ConvertResponse
from backend.services.tone_converter import convert_tone

logger = logging.getLogger(__name__)

router = APIRouter(prefix="", tags=["말투 변환 API"])


@router.post(
    "/convert",
    response_model=ConvertResponse,
    status_code=status.HTTP_200_OK,
    summary="업무 말투 자동 변환",
    description="입력된 원문을 4대 수신 대상(상사, 타팀 동료, 고객, 팀원)에 맞춘 비즈니스 어조로 변환합니다."
)
async def convert_text_endpoint(payload: ConvertRequest) -> ConvertResponse:
    try:
        converted = await convert_tone(
            text=payload.text,
            target_audience=payload.target_audience
        )
        return ConvertResponse(
            converted_text=converted,
            target_audience=payload.target_audience,
            original_text=payload.text
        )
    except Exception as e:
        logger.error(f"말투 변환 처리 실패: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"LLM API 호출 중 오류가 발생했습니다: {str(e)}"
        )
