"""Beta Browser Use integration."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pagepilot.beta.service import Agent, BetaAgentError, find_pagepilot_terminal_binary

if TYPE_CHECKING:
	from pagepilot.browser import BrowserProfile, BrowserSession
	from pagepilot.browser import BrowserSession as Browser
	from pagepilot.llm.anthropic.chat import ChatAnthropic
	from pagepilot.llm.azure.chat import ChatAzureOpenAI
	from pagepilot.llm.pagepilot.chat import ChatPagePilot
	from pagepilot.llm.google.chat import ChatGoogle
	from pagepilot.llm.groq.chat import ChatGroq
	from pagepilot.llm.litellm.chat import ChatLiteLLM
	from pagepilot.llm.mistral.chat import ChatMistral
	from pagepilot.llm.oci_raw.chat import ChatOCIRaw
	from pagepilot.llm.ollama.chat import ChatOllama
	from pagepilot.llm.openai.chat import ChatOpenAI
	from pagepilot.llm.vercel.chat import ChatVercel

_LAZY_IMPORTS = {
	'Browser': ('pagepilot.browser', 'BrowserSession'),
	'BrowserProfile': ('pagepilot.browser', 'BrowserProfile'),
	'BrowserSession': ('pagepilot.browser', 'BrowserSession'),
	'ChatOpenAI': ('pagepilot.llm.openai.chat', 'ChatOpenAI'),
	'ChatGoogle': ('pagepilot.llm.google.chat', 'ChatGoogle'),
	'ChatAnthropic': ('pagepilot.llm.anthropic.chat', 'ChatAnthropic'),
	'ChatPagePilot': ('pagepilot.llm.pagepilot.chat', 'ChatPagePilot'),
	'ChatGroq': ('pagepilot.llm.groq.chat', 'ChatGroq'),
	'ChatLiteLLM': ('pagepilot.llm.litellm.chat', 'ChatLiteLLM'),
	'ChatMistral': ('pagepilot.llm.mistral.chat', 'ChatMistral'),
	'ChatAzureOpenAI': ('pagepilot.llm.azure.chat', 'ChatAzureOpenAI'),
	'ChatOCIRaw': ('pagepilot.llm.oci_raw.chat', 'ChatOCIRaw'),
	'ChatOllama': ('pagepilot.llm.ollama.chat', 'ChatOllama'),
	'ChatVercel': ('pagepilot.llm.vercel.chat', 'ChatVercel'),
}


def __getattr__(name: str):
	if name in _LAZY_IMPORTS:
		module_path, attr_name = _LAZY_IMPORTS[name]
		from importlib import import_module

		module = import_module(module_path)
		attr = getattr(module, attr_name)
		globals()[name] = attr
		return attr
	raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


__all__ = [
	'Agent',
	'BetaAgentError',
	'Browser',
	'BrowserProfile',
	'BrowserSession',
	'ChatAnthropic',
	'ChatAzureOpenAI',
	'ChatPagePilot',
	'ChatGoogle',
	'ChatGroq',
	'ChatLiteLLM',
	'ChatMistral',
	'ChatOCIRaw',
	'ChatOllama',
	'ChatOpenAI',
	'ChatVercel',
	'find_pagepilot_terminal_binary',
]
