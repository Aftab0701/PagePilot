import os
from typing import TYPE_CHECKING

from pagepilot.logging_config import setup_logging

# Only set up logging if not in MCP mode or if explicitly requested
if os.environ.get('PAGEPILOT_SETUP_LOGGING', 'true').lower() != 'false':
	from pagepilot.config import CONFIG

	# Get log file paths from config/environment
	debug_log_file = getattr(CONFIG, 'PAGEPILOT_DEBUG_LOG_FILE', None)
	info_log_file = getattr(CONFIG, 'PAGEPILOT_INFO_LOG_FILE', None)

	# Set up logging with file handlers if specified
	logger = setup_logging(debug_log_file=debug_log_file, info_log_file=info_log_file)
else:
	import logging

	logger = logging.getLogger('pagepilot')

# Monkeypatch BaseSubprocessTransport.__del__ to handle closed event loops gracefully
from asyncio import base_subprocess

_original_del = base_subprocess.BaseSubprocessTransport.__del__


def _patched_del(self):
	"""Patched __del__ that handles closed event loops without throwing noisy red-herring errors like RuntimeError: Event loop is closed"""
	try:
		# Check if the event loop is closed before calling the original
		if hasattr(self, '_loop') and self._loop and self._loop.is_closed():
			# Event loop is closed, skip cleanup that requires the loop
			return
		_original_del(self)
	except RuntimeError as e:
		if 'Event loop is closed' in str(e):
			# Silently ignore this specific error
			pass
		else:
			raise


base_subprocess.BaseSubprocessTransport.__del__ = _patched_del


# Type stubs for lazy imports - fixes linter warnings
if TYPE_CHECKING:
	from pagepilot.agent.prompts import SystemPrompt
	from pagepilot.agent.service import Agent
	from pagepilot.agent.views import ActionModel, ActionResult, AgentHistoryList
	from pagepilot.browser import BrowserProfile, BrowserSession
	from pagepilot.browser import BrowserSession as Browser
	from pagepilot.dom.service import DomService
	from pagepilot.llm import models
	from pagepilot.llm.anthropic.chat import ChatAnthropic
	from pagepilot.llm.aws.chat_anthropic import ChatAnthropicBedrock
	from pagepilot.llm.aws.chat_bedrock import ChatAWSBedrock
	from pagepilot.llm.azure.chat import ChatAzureOpenAI
	from pagepilot.llm.pagepilot.chat import ChatPagePilot
	from pagepilot.llm.cerebras.chat import ChatCerebras
	from pagepilot.llm.deepseek.chat import ChatDeepSeek
	from pagepilot.llm.google.chat import ChatGoogle
	from pagepilot.llm.groq.chat import ChatGroq
	from pagepilot.llm.litellm.chat import ChatLiteLLM
	from pagepilot.llm.mistral.chat import ChatMistral
	from pagepilot.llm.oci_raw.chat import ChatOCIRaw
	from pagepilot.llm.ollama.chat import ChatOllama
	from pagepilot.llm.openai.chat import ChatOpenAI
	from pagepilot.llm.openrouter.chat import ChatOpenRouter
	from pagepilot.llm.orcarouter.chat import ChatOrcaRouter
	from pagepilot.llm.vercel.chat import ChatVercel
	from pagepilot.sandbox import sandbox
	from pagepilot.tools.service import Controller, Tools

	# Lazy imports mapping - only import when actually accessed
_LAZY_IMPORTS = {
	# Agent service (heavy due to dependencies)
	'Agent': ('pagepilot.agent.service', 'Agent'),
	# System prompt (moderate weight due to agent.views imports)
	'SystemPrompt': ('pagepilot.agent.prompts', 'SystemPrompt'),
	# Agent views (very heavy - over 1 second!)
	'ActionModel': ('pagepilot.agent.views', 'ActionModel'),
	'ActionResult': ('pagepilot.agent.views', 'ActionResult'),
	'AgentHistoryList': ('pagepilot.agent.views', 'AgentHistoryList'),
	'BrowserSession': ('pagepilot.browser', 'BrowserSession'),
	'Browser': ('pagepilot.browser', 'BrowserSession'),  # Alias for BrowserSession
	'BrowserProfile': ('pagepilot.browser', 'BrowserProfile'),
	# Tools (moderate weight)
	'Tools': ('pagepilot.tools.service', 'Tools'),
	'Controller': ('pagepilot.tools.service', 'Controller'),  # alias
	# DOM service (moderate weight)
	'DomService': ('pagepilot.dom.service', 'DomService'),
	# Chat models (very heavy imports)
	'ChatOpenAI': ('pagepilot.llm.openai.chat', 'ChatOpenAI'),
	'ChatGoogle': ('pagepilot.llm.google.chat', 'ChatGoogle'),
	'ChatAnthropic': ('pagepilot.llm.anthropic.chat', 'ChatAnthropic'),
	'ChatAnthropicBedrock': ('pagepilot.llm.aws.chat_anthropic', 'ChatAnthropicBedrock'),
	'ChatAWSBedrock': ('pagepilot.llm.aws.chat_bedrock', 'ChatAWSBedrock'),
	'ChatPagePilot': ('pagepilot.llm.pagepilot.chat', 'ChatPagePilot'),
	'ChatCerebras': ('pagepilot.llm.cerebras.chat', 'ChatCerebras'),
	'ChatDeepSeek': ('pagepilot.llm.deepseek.chat', 'ChatDeepSeek'),
	'ChatGroq': ('pagepilot.llm.groq.chat', 'ChatGroq'),
	'ChatLiteLLM': ('pagepilot.llm.litellm.chat', 'ChatLiteLLM'),
	'ChatMistral': ('pagepilot.llm.mistral.chat', 'ChatMistral'),
	'ChatAzureOpenAI': ('pagepilot.llm.azure.chat', 'ChatAzureOpenAI'),
	'ChatOCIRaw': ('pagepilot.llm.oci_raw.chat', 'ChatOCIRaw'),
	'ChatOllama': ('pagepilot.llm.ollama.chat', 'ChatOllama'),
	'ChatOpenRouter': ('pagepilot.llm.openrouter.chat', 'ChatOpenRouter'),
	'ChatOrcaRouter': ('pagepilot.llm.orcarouter.chat', 'ChatOrcaRouter'),
	'ChatVercel': ('pagepilot.llm.vercel.chat', 'ChatVercel'),
	# LLM models module
	'models': ('pagepilot.llm.models', None),
	# Sandbox execution
	'sandbox': ('pagepilot.sandbox', 'sandbox'),
}


def __getattr__(name: str):
	"""Lazy import mechanism - only import modules when they're actually accessed."""
	if name in _LAZY_IMPORTS:
		module_path, attr_name = _LAZY_IMPORTS[name]
		try:
			from importlib import import_module

			module = import_module(module_path)
			if attr_name is None:
				# For modules like 'models', return the module itself
				attr = module
			else:
				attr = getattr(module, attr_name)
			# Cache the imported attribute in the module's globals
			globals()[name] = attr
			return attr
		except ImportError as e:
			raise ImportError(f'Failed to import {name} from {module_path}: {e}') from e

	raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


__all__ = [
	'Agent',
	'BrowserSession',
	'Browser',  # Alias for BrowserSession
	'BrowserProfile',
	'Controller',
	'DomService',
	'SystemPrompt',
	'ActionResult',
	'ActionModel',
	'AgentHistoryList',
	# Chat models
	'ChatOpenAI',
	'ChatGoogle',
	'ChatAnthropic',
	'ChatAnthropicBedrock',
	'ChatAWSBedrock',
	'ChatPagePilot',
	'ChatCerebras',
	'ChatDeepSeek',
	'ChatGroq',
	'ChatLiteLLM',
	'ChatMistral',
	'ChatAzureOpenAI',
	'ChatOCIRaw',
	'ChatOllama',
	'ChatOpenRouter',
	'ChatOrcaRouter',
	'ChatVercel',
	'Tools',
	'Controller',
	# LLM models module
	'models',
	# Sandbox execution
	'sandbox',
]
