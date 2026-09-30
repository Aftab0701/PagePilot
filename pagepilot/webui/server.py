"""
PagePilot FastAPI WebUI Server
Serves the modern PagePilot static assets and provides the real-time agent WebSocket endpoint.
"""

import asyncio
import json
import logging
from pathlib import Path
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from pagepilot.agent.service import execute_task_stream

logger = logging.getLogger("pagepilot.server")
BASE_DIR = Path(__file__).parent.resolve()
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(title="PagePilot", version="0.1.0")

# Mount static assets
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/")
async def root():
    """Serves the main PagePilot user interface."""
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok", "app": "pagepilot", "version": "0.1.0"}


@app.websocket("/ws/agent")
async def agent_websocket(websocket: WebSocket):
    """
    WebSocket endpoint for real-time bidirectional communication with the BrowserUse agent.
    """
    await websocket.accept()
    logger.info("WebSocket client connected to /ws/agent")

    stop_event = asyncio.Event()
    agent_task = None

    async def send_step_update(step_data: dict):
        try:
            await websocket.send_text(json.dumps(step_data))
        except Exception as e:
            logger.error(f"Error sending step update: {e}")

    try:
        while True:
            raw_data = await websocket.receive_text()
            data = json.loads(raw_data)
            action = data.get("action")

            if action == "start":
                stop_event.clear()
                task_prompt = data.get("task", "")
                settings = data.get("settings", {})

                async def run_wrapper():
                    try:
                        result = await execute_task_stream(
                            task=task_prompt,
                            settings=settings,
                            step_callback=send_step_update,
                            stop_event=stop_event
                        )
                        await websocket.send_text(json.dumps({
                            "type": "done",
                            "summary": result.get("summary", "Task completed."),
                            "steps": result.get("steps", 0)
                        }))
                    except Exception as err:
                        logger.error(f"Error during agent task execution: {err}", exc_info=True)
                        await websocket.send_text(json.dumps({
                            "type": "error",
                            "message": str(err)
                        }))

                agent_task = asyncio.create_task(run_wrapper())

            elif action == "stop":
                stop_event.set()
                if agent_task and not agent_task.done():
                    agent_task.cancel()
                await websocket.send_text(json.dumps({
                    "type": "error",
                    "message": "Task stopped by user."
                }))

    except WebSocketDisconnect:
        logger.info("WebSocket client disconnected")
        stop_event.set()
        if agent_task and not agent_task.done():
            agent_task.cancel()
    except Exception as e:
        logger.error(f"WebSocket unhandled error: {e}")
