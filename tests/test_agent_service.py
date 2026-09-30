"""
Tests for PagePilot Agent Execution Service.
"""

import asyncio
import pytest
from pagepilot.agent.service import create_llm_instance, execute_task_stream


def test_create_llm_unsupported_provider():
    with pytest.raises(ValueError) as excinfo:
        create_llm_instance(provider="unsupported_xyz", model_name="test-model")
    assert "Unsupported LLM provider" in str(excinfo.value)


@pytest.mark.asyncio
async def test_execute_task_stream_simulated_fallback():
    collected_steps = []
    stop_event = asyncio.Event()

    async def step_cb(step_data):
        collected_steps.append(step_data)

    settings = {
        "provider": "google",
        "model": "gemini-2.5-flash",
        "maxSteps": 5
    }

    result = await execute_task_stream(
        task="Find top trending repositories on GitHub",
        settings=settings,
        step_callback=step_cb,
        stop_event=stop_event
    )

    assert result["status"] == "success"
    assert "summary" in result
    assert len(collected_steps) > 0
    assert collected_steps[0]["type"] == "step"
    assert "thought" in collected_steps[0]
