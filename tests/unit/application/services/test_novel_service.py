"""NovelService 单元测试"""
import pytest
from unittest.mock import Mock
from domain.novel.entities.novel import Novel, NovelStage
from domain.novel.entities.chapter import Chapter
from domain.novel.value_objects.novel_id import NovelId
from domain.novel.value_objects.chapter_id import ChapterId
from domain.novel.value_objects.word_count import WordCount
from domain.novel.value_objects.chapter_content import ChapterContent
from application.services.novel_service import NovelService
from application.dtos.novel_dto import NovelDTO


class TestNovelService:
    """NovelService 单元测试"""

    @pytest.fixture
    def mock_repository(self):
        """创建 mock 仓储"""
        return Mock()

    @pytest.fixture
    def service(self, mock_repository):
        """创建服务实例"""
        return NovelService(mock_repository)

    def test_create_novel(self, service, mock_repository):
        """测试创建小说"""
        novel_dto = service.create_novel(
            novel_id="test-novel",
            title="测试小说",
            author="测试作者",
            target_chapters=10
        )

        assert novel_dto.id == "test-novel"
        assert novel_dto.title == "测试小说"
        assert novel_dto.author == "测试作者"
        assert novel_dto.target_chapters == 10
        assert novel_dto.stage == "planning"

        # 验证调用了 save
        mock_repository.save.assert_called_once()

    def test_get_novel(self, service, mock_repository):
        """测试获取小说"""
        # 准备 mock 数据
        novel = Novel(
            id=NovelId("test-novel"),
            title="测试小说",
            author="测试作者",
            target_chapters=10
        )
        mock_repository.get_by_id.return_value = novel

        novel_dto = service.get_novel("test-novel")

        assert novel_dto is not None
        assert novel_dto.id == "test-novel"
        assert novel_dto.title == "测试小说"

        mock_repository.get_by_id.assert_called_once_with(NovelId("test-novel"))

    def test_get_novel_not_found(self, service, mock_repository):
        """测试获取不存在的小说"""
        mock_repository.get_by_id.return_value = None

        novel_dto = service.get_novel("nonexistent")

        assert novel_dto is None

    def test_list_novels(self, service, mock_repository):
        """测试列出所有小说"""
        # 准备 mock 数据
        novel1 = Novel(
            id=NovelId("novel-1"),
            title="小说1",
            author="作者1",
            target_chapters=10
        )
        novel2 = Novel(
            id=NovelId("novel-2"),
            title="小说2",
            author="作者2",
            target_chapters=20
        )
        mock_repository.list_all.return_value = [novel1, novel2]

        novels = service.list_novels()

        assert len(novels) == 2
        assert novels[0].id == "novel-1"
        assert novels[1].id == "novel-2"

    def test_delete_novel(self, service, mock_repository):
        """测试删除小说"""
        service.delete_novel("test-novel")

        mock_repository.delete.assert_called_once_with(NovelId("test-novel"))

    def test_add_chapter(self, service, mock_repository):
        """测试添加章节"""
        # 准备 mock 数据
        novel = Novel(
            id=NovelId("test-novel"),
            title="测试小说",
            author="测试作者",
            target_chapters=10
        )
        mock_repository.get_by_id.return_value = novel

        novel_dto = service.add_chapter(
            novel_id="test-novel",
            chapter_id="chapter-1",
            number=1,
            title="第一章",
            content="章节内容"
        )

        assert len(novel_dto.chapters) == 1
        assert novel_dto.chapters[0].id == "chapter-1"
        assert novel_dto.chapters[0].title == "第一章"

        # 验证调用了 save
        mock_repository.save.assert_called_once()

    def test_add_chapter_novel_not_found(self, service, mock_repository):
        """测试向不存在的小说添加章节"""
        mock_repository.get_by_id.return_value = None

        with pytest.raises(ValueError, match="Novel not found"):
            service.add_chapter(
                novel_id="nonexistent",
                chapter_id="chapter-1",
                number=1,
                title="第一章",
                content="章节内容"
            )
