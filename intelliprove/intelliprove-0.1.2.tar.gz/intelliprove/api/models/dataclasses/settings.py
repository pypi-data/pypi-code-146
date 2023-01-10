from dataclasses import dataclass
from urllib.parse import urljoin


@dataclass
class IntelliproveApiSettings:
    """Default settings"""
    base_url: str = 'https://engine-staging.intelliprove.be'  # URL to IntelliProve API
    version: str = 'v1'
    get_results_retry_count: int = 5  # Maximum number of times the get_results API call should be retried
    max_video_size_mb: int = 100  # Maximum file size of video that is uploaded

    # Connection timeouts
    upload_timeout: float = 120.0  # Maximum timeout (s) that an upload may take before raising TimeoutError
    send_timeout: float = 30.0  # Maximum timeout (s) sending an HTTP request may take before raising TimeoutError

    @property
    def full_url(self) -> str:
        return urljoin(self.base_url, self.version)