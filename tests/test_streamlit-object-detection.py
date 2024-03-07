"""Package related tests."""
from streamlit-object-detection import __version__


def test_streamlit-object-detection_version():
    """Checks correct package version."""
    assert __version__ == "0.1.0"
