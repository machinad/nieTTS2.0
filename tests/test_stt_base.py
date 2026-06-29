import pytest

from engines.stt.base import BaseSTT, STTResult


class TestSTTResult:
    def test_default_values(self):
        result = STTResult(success=True)
        assert result.success is True
        assert result.text == ""
        assert result.language == ""
        assert result.emotion == ""
        assert result.error is None
        assert result.segments == []

    def test_is_success_true(self):
        result = STTResult(success=True)
        assert result.is_success is True

    def test_is_success_false(self):
        result = STTResult(success=False)
        assert result.is_success is False

    def test_full_result(self):
        result = STTResult(
            success=True,
            text="你好世界",
            language="zh",
            emotion="neutral",
            segments=[{"text": "你好", "start": 0.0, "end": 1.0}],
        )
        assert result.text == "你好世界"
        assert result.language == "zh"
        assert result.emotion == "neutral"
        assert len(result.segments) == 1

    def test_error_result(self):
        result = STTResult(success=False, error="Model not loaded")
        assert result.success is False
        assert result.error == "Model not loaded"
        assert result.is_success is False


class TestBaseSTT:
    def test_cannot_instantiate_abstract(self):
        with pytest.raises(TypeError):
            BaseSTT()

    def test_concrete_can_instantiate(self):
        class Impl(BaseSTT):
            engine_name = "Test"

            async def transcribe(self, samples, sample_rate):
                return STTResult(success=True)

            def is_available(self):
                return True

        impl = Impl()
        assert impl.engine_name == "Test"
        assert impl.is_available() is True

    @pytest.mark.asyncio
    async def test_close_is_noop_by_default(self):
        class Impl(BaseSTT):
            engine_name = "Test"

            async def transcribe(self, samples, sample_rate):
                return STTResult(success=True)

            def is_available(self):
                return True

        impl = Impl()
        # Should not raise
        await impl.close()
