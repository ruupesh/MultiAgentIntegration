from fastapi import APIRouter, Depends, HTTPException

from app.core.security import get_current_user
from app.models.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import process_chat_message
from app.services.session_service import session_service
from app.utils.logging import logger

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user: dict = Depends(get_current_user),
) -> ChatResponse:
    """
    Conversation endpoint.

    Receives a user message, processes it (Phase 2), and returns an assistant response.
    Requires a Bearer token in the Authorization header.
    """
    try:
        session_id = request.session_id
        user_id = request.user_id

        session = await session_service.get_session(
            app_name="orchestrator_api", user_id=user_id, session_id=session_id
        )
        logger.info("Session retrieved", session=session)
        if not session:
            # Get or create session
            session = await session_service.create_session(
                app_name="orchestrator_api",
                user_id=user_id,
                session_id=session_id,
                state={
                    "auth_token": current_user.get("token"),
                    "conversation_history": [],
                },
            )
        logger.info("Session created", session=session)
        response = await process_chat_message(request, session)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/chat/session/{session_id}")
async def get_session_info(
    session_id: str,
    current_user: dict = Depends(get_current_user),
) -> dict:
    """Return the session info for a session."""
    try:
        session = await session_service.get_session(
            app_name="orchestrator_api",
            user_id=current_user.get("user_id"),
            session_id=session_id,
        )
        return {
            "session": session,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
