# domain/novel/entities/novel.py
from enum import Enum
from typing import List
from domain.shared.base_entity import BaseEntity
from domain.novel.value_objects.novel_id import NovelId
from domain.novel.entities.chapter import Chapter, ChapterStatus
from domain.shared.exceptions import InvalidOperationError


class NovelStage(str, Enum):
    """小说阶段"""
    PLANNING = "planning"
    WRITING = "writing"
    REVIEWING = "reviewing"
    COMPLETED = "completed"


class Novel(BaseEntity):
    """小说聚合根"""

    def __init__(
        self,
        id: NovelId,
        title: str,
        author: str,
        target_chapters: int,
        stage: NovelStage = NovelStage.PLANNING
    ):
        super().__init__(id.value)
        self.novel_id = id  # 存储 NovelId 对象
        self.title = title
        self.author = author
        self.target_chapters = target_chapters
        self.stage = stage
        self.chapters: List[Chapter] = []

    def add_chapter(self, chapter: Chapter) -> None:
        """添加章节（必须连续）"""
        expected_number = len(self.chapters) + 1
        if chapter.number != expected_number:
            raise InvalidOperationError(
                f"Chapter number must be {expected_number}, got {chapter.number}"
            )
        self.chapters.append(chapter)

    @property
    def completed_chapters(self) -> int:
        """已完成章节数"""
        return len([c for c in self.chapters if c.status == ChapterStatus.COMPLETED])

    def get_total_word_count(self):
        """获取总字数"""
        from domain.novel.value_objects.word_count import WordCount
        total = WordCount(0)
        for chapter in self.chapters:
            total = total + chapter.word_count
        return total
