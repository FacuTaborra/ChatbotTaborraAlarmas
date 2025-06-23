from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import StateGraph, END
from src.settings import settings
from src.template.prompts import INTENT_CLASSIFIER_BASE_TEMPLATE, PROMPT_SUMMARY
from langchain.text_splitter import RecursiveCharacterTextSplitter
from src.utils.helpers import trim_chat_history
from src.database.models import ChatState

MAX_TOKENS_MODEL = 16385 
TOKENS_RESERVA = 1000

class ChatChain:
    def __init__(self, api_key: str = None, model_name: str = None):
        self.api_key = settings.API_KEY or api_key
        self.model_name = settings.MODEL or model_name
        self.llm = ChatOpenAI(
            model_name=self.model_name,
            temperature=0.3,
            openai_api_key=self.api_key
        )
        self.prompt = ChatPromptTemplate.from_messages([
            ('system', INTENT_CLASSIFIER_BASE_TEMPLATE),
            MessagesPlaceholder(variable_name="chat_history"),
            ('user', "{input}")
        ])
        self.summarize_prompt = ChatPromptTemplate.from_messages([
            ('system', PROMPT_SUMMARY),
            MessagesPlaceholder(variable_name="chat_history"),
        ])
        self.summarizer = self.summarize_prompt | self.llm

        # LangGraph: Definir el grafo de estados usando ChatState
        self.graph = StateGraph(state_schema=ChatState)
        self.graph.add_node("process", self.process_message)
        self.graph.add_edge("process", END)
        self.graph.set_entry_point("process")
        self.graph = self.graph.compile()

    def summarize_history(self, chat_history):
        if not chat_history:
            return []
        summary = self.summarizer.invoke({"chat_history": chat_history})
        print(f'summary {summary.content}')
        summary_content = summary.content if getattr(summary, "content", None) else "Resumen no disponible."
        return [HumanMessage(content=summary_content)]
    
    def filter_and_summarize_history(self, chat_history, n=6):
        """
        Resume los mensajes viejos y mantiene los últimos n mensajes completos.
        """
        if len(chat_history) <= n:
            print("todavia no filtra")
            return trim_chat_history(chat_history, max_tokens=MAX_TOKENS_MODEL - TOKENS_RESERVA, model_name=self.model_name)

        old_messages = chat_history[:-n]
        recent_messages = chat_history[-n:]

        old_messages_trimmed = trim_chat_history(old_messages, max_tokens=MAX_TOKENS_MODEL // 2, model_name=self.model_name)
        summary = self.summarize_history(old_messages_trimmed) if old_messages_trimmed else []

        tokens_usados = sum(len(m.content) for m in summary)  # Esto es una aproximación, puedes usar tiktoken si quieres precisión
        max_tokens_recientes = MAX_TOKENS_MODEL - TOKENS_RESERVA - tokens_usados
        recent_messages_trimmed = trim_chat_history(recent_messages, max_tokens=max_tokens_recientes, model_name=self.model_name)

        # Solo resumimos si hay mensajes viejos
        print(f'recent_messages {recent_messages_trimmed}')
        # El historial para el prompt es: [resumen] + [últimos n mensajes]
        return summary + recent_messages_trimmed

    def create_chain(self):
        chain = self.prompt | self.llm
        return chain

    def process_message(self, state: ChatState) -> ChatState:
        """
        Nodo de procesamiento principal para LangGraph.
        """
        input_text = state.input
        chat_history = state.chat_history.copy()  # Evitar modificar el original
        thread_id = state.thread_id
        chat_history_to_use = self.filter_and_summarize_history(chat_history)
        chain = self.create_chain()
        try:
            response = chain.invoke({
                "input": input_text,
                "chat_history": chat_history_to_use,
            })
        except Exception as e:
            print(f'Error al ejecutar: {e}')
            return ChatState(
                input=input_text,
                chat_history=chat_history,
                thread_id=thread_id
            )
        # Actualiza el historial (esto lo deberías guardar en tu base de datos usando thread_id)

        chat_history.append(HumanMessage(content=input_text))
        chat_history.append(AIMessage(content=response.content))
        return ChatState(
            input=input_text,
            chat_history=chat_history,
            response=response.content,
            thread_id=thread_id
        )

    def run(self, input_text: str, chat_history: list = [], thread_id: int = None):
        """
        Ejecuta el flujo conversacional usando LangGraph.
        thread_id identifica la conversación.
        """
        print(f'entrada: {input_text}')
        state = ChatState(
            input=input_text,
            chat_history=chat_history,
            thread_id=thread_id
        )
        result = self.graph.invoke(state)
        # Puedes retornar el dict si lo necesitas para compatibilidad
        return result.model_dump() if hasattr(result, "model_dump") else result