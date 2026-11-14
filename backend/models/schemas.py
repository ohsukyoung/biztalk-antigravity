from typing import Literal
from pydantic import BaseModel, Field

TargetAudience = Literal["boss", "colleague", "client", "team"]


class ConvertRequest(BaseModel):
    """말투 변환 요청 스키마"""
    text: str = Field(
        ...,
        min_length=1,
        description="변환할 원문 내용 (최소 1자 이상)",
        examples=["내일까지 보고서 제출 어려울 것 같음"]
    )
    target_audience: TargetAudience = Field(
        ...,
        description="수신 대상 (boss: 상사/임원, colleague: 타팀 동료, client: 고객/외부, team: 팀 내 동료)",
        examples=["boss"]
    )


class ConvertResponse(BaseModel):
    """말투 변환 응답 스키마"""
    converted_text: str = Field(
        ...,
        description="비즈니스 어조로 변환된 최종 텍스트"
    )
    target_audience: str = Field(
        ...,
        description="적용된 수신 대상 코드"
    )
    original_text: str = Field(
        ...,
        description="사용자가 입력한 원문 내용"
    )
