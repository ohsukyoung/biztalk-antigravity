import os
import asyncio
import logging
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_upstage import ChatUpstage
from backend.prompts.templates import get_system_prompt

# .env 로드
load_dotenv()

logger = logging.getLogger(__name__)


def get_llm() -> ChatUpstage:
    """Upstage Solar-Pro4 LLM 인스턴스 반환"""
    api_key = os.getenv("UPSTAGE_API_KEY")
    if not api_key:
        raise ValueError(
            "UPSTAGE_API_KEY 환경 변수가 설정되지 않았습니다. .env 파일을 확인해 주세요."
        )
    return ChatUpstage(
        model="solar-pro4",
        temperature=0.3,
        api_key=api_key
    )


async def convert_tone(text: str, target_audience: str) -> str:
    """
    원문 텍스트와 수신 대상 코드를 받아 Upstage Solar-Pro4 모델을 통해
    비즈니스 어조로 변환된 최종 텍스트를 반환합니다.
    """
    system_prompt = get_system_prompt(target_audience)

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "{system_prompt}"),
        ("human", "다음 메시지를 변환해 주세요:\n\n{user_text}"),
    ])

    llm = get_llm()
    chain = prompt_template | llm | StrOutputParser()

    try:
        # 이벤트 루프 라이프사이클 이슈 방지를 위해 asyncio.to_thread로 안전하게 동기 호출 실행
        result = await asyncio.to_thread(
            chain.invoke,
            {
                "system_prompt": system_prompt,
                "user_text": text.strip(),
            }
        )

        # 앞뒤 따옴표나 불필요한 공백 제거
        cleaned = result.strip().strip('"\'')
        return cleaned

    except Exception as e:
        logger.error(f"Solar-Pro4 API 호출 중 오류 발생: {str(e)}", exc_info=True)
        raise RuntimeError(f"말투 변환 AI 모델 호출에 실패했습니다: {str(e)}") from e

