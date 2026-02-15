import os
from typing import Optional
from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.apps import App, ResumabilityConfig
from google.adk.tools.function_tool import FunctionTool
from google.adk.agents.callback_context import CallbackContext

from app.agentic.prompts_library.orchestrator_agent import SYSTEM_PROMPT
from app.agentic.tools.custom_tools import check_prime, check_weather, find_file_path
from app.agentic.adapters.mcp_adapter import McpAdapter
from app.agentic.adapters.remote_a2a_adapter import RemoteA2aAdapter
from app.models.schemas.chat import ChatRequest
from app.utils.logging import logger

from dotenv import load_dotenv

load_dotenv()

AGENT_MODEL = os.getenv("AGENT_MODEL")


approval_find_file_path = FunctionTool(func=find_file_path, require_confirmation=True)
approval_check_prime = FunctionTool(func=check_prime, require_confirmation=True)


class RootAgent:

    def __init__(
        self, auth_token: Optional[str] = None, request: Optional[ChatRequest] = None
    ) -> None:
        self._auth_token = auth_token
        self._request = request
        self.mcp_adapter = McpAdapter(auth_token=self._auth_token)
        self.remote_a2a_adapter = RemoteA2aAdapter(auth_token=self._auth_token)
        self.root_agent = self.get_root_agent()

    def update_request_message(self, callback_context: CallbackContext):
        """Append the user's request to conversation_history in session state.

        Runs as before_agent_callback. Uses reassignment (not in-place append)
        so the State object correctly tracks the delta for persistence.
        """
        history = list(callback_context.state.get("conversation_history", []))
        if self._request and self._request.content.message:
            history.append(
                {
                    "role": "user",
                    "content": self._request.content.message,
                }
            )
        elif self._request and self._request.content.hitl_approval:
            history.append(
                {
                    "role": "user",
                    "content": f"[HITL Approval: {[item.model_dump() for item in self._request.content.hitl_approval]}]",
                }
            )
        callback_context.state["conversation_history"] = history

    def update_response_message(self, callback_context: CallbackContext):
        """Append the agent's response to conversation_history in session state.

        Runs as after_agent_callback. By this point the agent has already
        produced its response events, which are available in
        callback_context.session.events. We walk events in reverse to find
        the most recent agent response (text or HITL request) and persist it.
        """
        response_text = None
        hitl_requested = []

        for event in reversed(callback_context.session.events):
            # Skip user-authored events entirely
            if event.author == "user":
                continue
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if hasattr(part, "text") and part.text:
                        response_text = part.text
                    if (
                        hasattr(part, "function_call")
                        and part.function_call
                        and hasattr(part.function_call, "args")
                        and part.function_call.args
                        and "originalFunctionCall" in part.function_call.args
                    ):
                        hitl_requested.append(
                            {
                                "function_id": part.function_call.id,
                                "function_name": part.function_call.name,
                                "confirmed": part.function_call.args.get(
                                    "toolConfirmation", {}
                                ).get("confirmed", False),
                                "payload": part.function_call.args.get(
                                    "originalFunctionCall", {}
                                ).get("args"),
                                "hint": part.function_call.args.get(
                                    "toolConfirmation", {}
                                ).get("hint"),
                            }
                        )
                if response_text or hitl_requested:
                    break

        history = list(callback_context.state.get("conversation_history", []))
        if hitl_requested:
            history.append(
                {
                    "role": "assistant",
                    "content": None,
                    "hitl_requested": hitl_requested,
                }
            )
            callback_context.state["conversation_history"] = history
        elif response_text:
            history.append(
                {
                    "role": "assistant",
                    "content": response_text,
                }
            )
            callback_context.state["conversation_history"] = history

    def get_root_agent(self):
        logger.info("Building root agent with sub-agents and tools...")
        sub_agents_list = self.remote_a2a_adapter.get_remote_agents()
        mcp_toolset = self.mcp_adapter.get_mcp_tool_sets()
        tools_list = [approval_check_prime, check_weather, approval_find_file_path]
        tools_list.extend(mcp_toolset)
        root_agent = Agent(
            name="Supervisor",
            model=LiteLlm(model=AGENT_MODEL),
            description="An agent that either hands off tasks to specialized sub-agents or uses tools directly to accomplish the overall goal effectively.",
            instruction=SYSTEM_PROMPT,
            before_agent_callback=[self.update_request_message],
            after_agent_callback=[self.update_response_message],
        )
        if sub_agents_list:
            root_agent.sub_agents = sub_agents_list
            logger.info(
                "Added sub-agents to root agent.",
                number_of_sub_agents=len(sub_agents_list),
                sub_agents_list=[agent.name for agent in sub_agents_list],
            )
        else:
            logger.info("No sub-agents found to add to root agent.")
        if tools_list:
            root_agent.tools = tools_list
            logger.info(
                "Added tools to root agent.",
                number_of_tools=len(tools_list),
                tools_list=tools_list,
            )
        else:
            logger.info("No tools found to add to root agent.")
        return root_agent

    def get_root_app(self):
        logger.info("Building root app with updated agents and tools...")
        app = App(
            name="Supervisor",
            root_agent=self.root_agent,
            resumability_config=ResumabilityConfig(is_resumable=True),
        )
        return app
