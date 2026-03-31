"""Novel 数据传输对象"""
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime


@dataclass
class ChapterDTO:
    """章节 DTO"""
    id: str
    number: int
    title: str
    content: str
    word_count: int


@dataclass
class NovelDTO:
    """小说 DTO

    用于在应用层和外部层之间传输数据。
    """
    id: str
    title: str
    author: str
    target_chapters: int
    stage: str
    chapters: List[ChapterDTO]
    total_word_count: int

    @classmethod
    def from_domain(cls, novel) -> 'NovelDTO':
        """从领域对象创建 DTO

        Args:
            novel: Novel 领域对象

        Returns:
            NovelDTO
        """
        from domain.novel.entities.novel import Novel

        chapters = [
            ChapterDTO(
                id=chapter.id,
                number=chapter.number,
                title=chapter.title,
                content=chapter.content,
                word_count=chapter.word_count.value
            )
            for chapter in novel.chapters
        ]

        return cls(
            id=novel.novel_id.value,
            title=novel.title,
            author=novel.author,
            target_chapters=novel.target_chapters,
            stage=novel.stage.value,
            chapters=chapters,
            total_word_count=novel.get_total_word_count().value
        )
