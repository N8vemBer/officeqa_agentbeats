import asyncio
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.types import (
    Message,
    Part,
    TaskState,
    TaskStatus,
    TaskStatusUpdateEvent,
    TextPart,
)
from uuid import uuid4


SYSTEM_PROMPT = """You are a financial document QA agent for U.S. Treasury Bulletins (1939-2025).

Return EXACTLY one final answer inside:

<FINAL_ANSWER>...</FINAL_ANSWER>
"""


class Executor(AgentExecutor):

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:

        question = ""
        for part in context.message.parts:
            if isinstance(part.root, TextPart):
                question = part.root.text

        answer = "<FINAL_ANSWER>unknown</FINAL_ANSWER>"

        await event_queue.enqueue_event(
    TaskStatusUpdateEvent(
        taskId=context.task_id,
        contextId=context.context_id,
        status=TaskStatus(
            state=TaskState.completed,
            message=Message(
                messageId=uuid4().hex,
                role="agent",
                parts=[Part(root=TextPart(kind="text", text=answer))],
            ),
        ),
        final=True,
    )
)
                ),
                final=True,
            )
        )
