import numpy as np
import pytest

from engines.stt.vad.base import BaseVAD, SpeechSegment


class TestSpeechSegment:
    def test_default_values(self):
        samples = np.array([0.1, 0.2, 0.3], dtype=np.float32)
        seg = SpeechSegment(samples=samples, start=0)
        assert len(seg.samples) == 3
        assert seg.start == 0
        assert seg.sample_rate == 16000

    def test_start_sec(self):
        samples = np.array([0.1, 0.2], dtype=np.float32)
        seg = SpeechSegment(samples=samples, start=16000, sample_rate=16000)
        assert seg.start_sec == 1.0

    def test_start_sec_zero(self):
        samples = np.array([0.1], dtype=np.float32)
        seg = SpeechSegment(samples=samples, start=0)
        assert seg.start_sec == 0.0

    def test_duration_sec(self):
        samples = np.zeros(8000, dtype=np.float32)
        seg = SpeechSegment(samples=samples, start=0, sample_rate=16000)
        assert seg.duration_sec == 0.5

    def test_duration_sec_empty(self):
        samples = np.array([], dtype=np.float32)
        seg = SpeechSegment(samples=samples, start=0)
        assert seg.duration_sec == 0.0

    def test_custom_sample_rate(self):
        samples = np.zeros(48000, dtype=np.float32)
        seg = SpeechSegment(samples=samples, start=48000, sample_rate=48000)
        assert seg.start_sec == 1.0
        assert seg.duration_sec == 1.0


class TestBaseVAD:
    def test_cannot_instantiate_abstract(self):
        with pytest.raises(TypeError):
            BaseVAD()

    def test_concrete_can_instantiate(self):
        class Impl(BaseVAD):
            engine_name = "Test"

            def accept_waveform(self, samples):
                pass

            def empty(self):
                return True

            @property
            def front(self):
                raise IndexError()

            def pop(self):
                pass

            def flush(self):
                pass

            @property
            def is_speech_detected(self):
                return False

        impl = Impl()
        assert impl.engine_name == "Test"
        assert impl.empty() is True
        assert impl.is_speech_detected is False
