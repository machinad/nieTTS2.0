import pytest
from pathlib import Path
from engines.tts.base import TTSResult, BaseTTS


class TestTTSResult:
    def test_default_values(self):
        result = TTSResult(success=True)
        assert result.success is True
        assert result.path is None
        assert result.voice == ""
        assert result.text == ""
        assert result.error is None

    def test_is_success_true(self):
        result = TTSResult(success=True)
        assert result.is_success is True

    def test_is_success_false(self):
        result = TTSResult(success=False)
        assert result.is_success is False

    def test_full_result(self):
        result = TTSResult(
            success=True,
            path=Path("/tmp/test.wav"),
            voice="zh-CN-XiaoxiaoNeural",
            text="你好",
        )
        assert result.path == Path("/tmp/test.wav")
        assert result.voice == "zh-CN-XiaoxiaoNeural"
        assert result.text == "你好"

    def test_error_result(self):
        result = TTSResult(success=False, text="test", error="API error")
        assert result.success is False
        assert result.error == "API error"
        assert result.is_success is False


class TestBaseTTS:
    def test_cannot_instantiate_abstract(self):
        with pytest.raises(TypeError):
            BaseTTS(Path("/tmp"))

    def test_concrete_can_instantiate(self):
        class Impl(BaseTTS):
            engine_name = "Test"
            async def synthesize(self, text, voice, **kwargs):
                return TTSResult(success=True)
            def is_available(self):
                return True

        impl = Impl(Path("/tmp"))
        assert impl.engine_name == "Test"
        assert impl.is_available() is True

    def test_make_path_creates_unique_paths(self, temp_dir):
        class Impl(BaseTTS):
            engine_name = "Test"
            async def synthesize(self, text, voice, **kwargs):
                return TTSResult(success=True)
            def is_available(self):
                return True

        impl = Impl(temp_dir)
        p1 = impl._make_path(".wav")
        p2 = impl._make_path(".wav")
        assert p1 != p2
        assert p1.suffix == ".wav"
        assert p2.suffix == ".wav"
        assert p1.parent == temp_dir
        assert p2.parent == temp_dir

    def test_make_path_custom_suffix(self, temp_dir):
        class Impl(BaseTTS):
            engine_name = "Test"
            async def synthesize(self, text, voice, **kwargs):
                return TTSResult(success=True)
            def is_available(self):
                return True

        impl = Impl(temp_dir)
        p = impl._make_path(".mp3")
        assert p.suffix == ".mp3"
        assert p.parent == temp_dir

    @pytest.mark.asyncio
    async def test_close_is_noop_by_default(self, temp_dir):
        class Impl(BaseTTS):
            engine_name = "Test"
            async def synthesize(self, text, voice, **kwargs):
                return TTSResult(success=True)
            def is_available(self):
                return True

        impl = Impl(temp_dir)
        # Should not raise
        await impl.close()
