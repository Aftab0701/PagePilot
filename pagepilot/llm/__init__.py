"""
We have switched all of our code from langchain to openai.types.chat.chat_completion_message_param.

For easier transition we have
"""

from typing import TYPE_CHECKING

# Lightweight imports that are commonly used
from pagepilot.llm.base import BaseChatModel
from pagepilot.llm.messages import (
	AssistantMessage,
	BaseMessage,
	SystemMessage,
	UserMessage,
)
from pagepilot.llm.messages import (
	ContentPartImageParam as ContentImage,
)
from pagepilot.llm.messages import (
	ContentPartRefusalParam as ContentRefusal,
)
from pagepilot.llm.messages import (
	ContentPartTextParam as ContentText,
)

# Type stubs for lazy imports
if TYPE_CHECKING:
	from pagepilot.llm.anthropic.chat import ChatAnthropic
	from pagepilot.llm.aws.chat_anthropic import ChatAnthropicBedrock
	from pagepilot.llm.aws.chat_bedrock import ChatAWSBedrock
	from pagepilot.llm.azure.chat import ChatAzureOpenAI
	from pagepilot.llm.pagepilot.chat import ChatPagePilot
	from pagepilot.llm.cerebras.chat import ChatCerebras
	from pagepilot.llm.deepseek.chat import ChatDeepSeek
	from pagepilot.llm.google.chat import ChatGoogle
	from pagepilot.llm.groq.chat import ChatGroq
	from pagepilot.llm.mistral.chat import ChatMistral
	from pagepilot.llm.oci_raw.chat import ChatOCIRaw
	from pagepilot.llm.ollama.chat import ChatOllama
	from pagepilot.llm.openai.chat import ChatOpenAI
	from pagepilot.llm.openrouter.chat import ChatOpenRouter
	from pagepilot.llm.orcarouter.chat import ChatOrcaRouter
	from pagepilot.llm.vercel.chat import ChatVercel

	# Type stubs for model instances - enables IDE autocomplete
	openai_gpt_4o: ChatOpenAI
	openai_gpt_4o_mini: ChatOpenAI
	openai_gpt_4_1_mini: ChatOpenAI
	openai_o1: ChatOpenAI
	openai_o1_mini: ChatOpenAI
	openai_o1_pro: ChatOpenAI
	openai_o3: ChatOpenAI
	openai_o3_mini: ChatOpenAI
	openai_o3_pro: ChatOpenAI
	openai_o4_mini: ChatOpenAI
	openai_gpt_5: ChatOpenAI
	openai_gpt_5_mini: ChatOpenAI
	openai_gpt_5_nano: ChatOpenAI

	azure_gpt_4o: ChatAzureOpenAI
	azure_gpt_4o_mini: ChatAzureOpenAI
	azure_gpt_4_1_mini: ChatAzureOpenAI
	azure_o1: ChatAzureOpenAI
	azure_o1_mini: ChatAzureOpenAI
	azure_o1_pro: ChatAzureOpenAI
	azure_o3: ChatAzureOpenAI
	azure_o3_mini: ChatAzureOpenAI
	azure_o3_pro: ChatAzureOpenAI
	azure_gpt_5: ChatAzureOpenAI
	azure_gpt_5_mini: ChatAzureOpenAI

	google_gemini_2_0_flash: ChatGoogle
	google_gemini_2_0_pro: ChatGoogle
	google_gemini_2_5_pro: ChatGoogle
	google_gemini_2_5_flash: ChatGoogle
	google_gemini_2_5_flash_lite: ChatGoogle

# Models are imported on-demand via __getattr__

# Lazy imports mapping for heavy chat models
_LAZY_IMPORTS = {
	'ChatAnthropic': ('pagepilot.llm.anthropic.chat', 'ChatAnthropic'),
	'ChatAnthropicBedrock': ('pagepilot.llm.aws.chat_anthropic', 'ChatAnthropicBedrock'),
	'ChatAWSBedrock': ('pagepilot.llm.aws.chat_bedrock', 'ChatAWSBedrock'),
	'ChatAzureOpenAI': ('pagepilot.llm.azure.chat', 'ChatAzureOpenAI'),
	'ChatPagePilot': ('pagepilot.llm.pagepilot.chat', 'ChatPagePilot'),
	'ChatCerebras': ('pagepilot.llm.cerebras.chat', 'ChatCerebras'),
	'ChatDeepSeek': ('pagepilot.llm.deepseek.chat', 'ChatDeepSeek'),
	'ChatGoogle': ('pagepilot.llm.google.chat', 'ChatGoogle'),
	'ChatGroq': ('pagepilot.llm.groq.chat', 'ChatGroq'),
	'ChatMistral': ('pagepilot.llm.mistral.chat', 'ChatMistral'),
	'ChatOCIRaw': ('pagepilot.llm.oci_raw.chat', 'ChatOCIRaw'),
	'ChatOllama': ('pagepilot.llm.ollama.chat', 'ChatOllama'),
	'ChatOpenAI': ('pagepilot.llm.openai.chat', 'ChatOpenAI'),
	'ChatOpenRouter': ('pagepilot.llm.openrouter.chat', 'ChatOpenRouter'),
	'ChatOrcaRouter': ('pagepilot.llm.orcarouter.chat', 'ChatOrcaRouter'),
	'ChatVercel': ('pagepilot.llm.vercel.chat', 'ChatVercel'),
}

# Cache for model instances - only created when accessed
_model_cache: dict[str, 'BaseChatModel'] = {}


def __getattr__(name: str):
	"""Lazy import mechanism for heavy chat model imports and model instances."""
	if name in _LAZY_IMPORTS:
		module_path, attr_name = _LAZY_IMPORTS[name]
		try:
			from importlib import import_module

			module = import_module(module_path)
			attr = getattr(module, attr_name)
			return attr
		except ImportError as e:
			raise ImportError(f'Failed to import {name} from {module_path}: {e}') from e

	# Check cache first for model instances
	if name in _model_cache:
		return _model_cache[name]

	# Try to get model instances from models module on-demand
	try:
		from pagepilot.llm.models import __getattr__ as models_getattr

		attr = models_getattr(name)
		# Cache in our clean cache dict
		_model_cache[name] = attr
		return attr
	except (AttributeError, ImportError):
		pass

	raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


__all__ = [
	# Message types -> for easier transition from langchain
	'BaseMessage',
	'UserMessage',
	'SystemMessage',
	'AssistantMessage',
	# Content parts with better names
	'ContentText',
	'ContentRefusal',
	'ContentImage',
	# Chat models
	'BaseChatModel',
	'ChatOpenAI',
	'ChatPagePilot',
	'ChatDeepSeek',
	'ChatGoogle',
	'ChatAnthropic',
	'ChatAnthropicBedrock',
	'ChatAWSBedrock',
	'ChatGroq',
	'ChatMistral',
	'ChatAzureOpenAI',
	'ChatOCIRaw',
	'ChatOllama',
	'ChatOpenRouter',
	'ChatOrcaRouter',
	'ChatVercel',
	'ChatCerebras',
]
