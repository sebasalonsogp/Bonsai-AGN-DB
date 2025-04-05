import pytest
import asyncio
from typing import Generator

# Configure pytest for asyncio
@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """
    Create an instance of the default event loop for each test case.
    This is needed for pytest-asyncio to work properly.
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

# Add more global fixtures here as needed 