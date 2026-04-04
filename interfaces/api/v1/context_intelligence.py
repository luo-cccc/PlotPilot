"""FastAPI 路由 - 场景导演分析"""
import logging

from fastapi import APIRouter, Depends, HTTPException, status

from application.dtos.scene_director_dto import (
    SceneDirectorAnalyzeRequest,
    SceneDirectorAnalyzeResponse,
)
from application.services.scene_director_service import SceneDirectorService
from interfaces.api.dependencies import get_scene_director_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/novels", tags=["context-intelligence"])


@router.post("/{novel_id}/scene-director/analyze", response_model=SceneDirectorAnalyzeResponse)
async def analyze_scene(
    novel_id: str,
    body: SceneDirectorAnalyzeRequest,
    svc: SceneDirectorService = Depends(get_scene_director_service),
):
    """分析章节大纲，提取场景信息

    Args:
        novel_id: 小说 ID（预留：可按小说过滤词表；Phase 1 仅记录日志）
        body: 分析请求体
        svc: 场景导演服务

    Returns:
        SceneDirectorAnalyzeResponse: 分析结果
    """
    logger.debug("scene-director analyze novel_id=%s chapter=%s", novel_id, body.chapter_number)
    try:
        r = await svc.analyze(body.chapter_number, body.outline)
    except Exception as e:
        logger.exception("scene-director failed for novel_id=%s", novel_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to analyze scene"
        ) from e
    return SceneDirectorAnalyzeResponse(**r.model_dump())
