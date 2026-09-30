from openai.types.chat import ChatCompletionMessageParam

from pagepilot.llm.messages import BaseMessage
from pagepilot.llm.openai.serializer import OpenAIMessageSerializer


class OrcaRouterMessageSerializer:
	"""
	Serializer for converting between custom message types and OrcaRouter message formats.

	OrcaRouter exposes an OpenAI-compatible API, so we can reuse the OpenAI serializer.
	"""

	@staticmethod
	def serialize_messages(messages: list[BaseMessage]) -> list[ChatCompletionMessageParam]:
		"""
		Serialize a list of pagepilot messages to OrcaRouter-compatible messages.

		Args:
		    messages: List of pagepilot messages

		Returns:
		    List of OrcaRouter-compatible messages (identical to OpenAI format)
		"""
		# OrcaRouter uses the same message format as OpenAI
		return OpenAIMessageSerializer.serialize_messages(messages)
