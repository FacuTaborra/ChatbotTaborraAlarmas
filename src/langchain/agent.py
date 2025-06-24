from typing import List, Optional, Dict

from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

from langgraph.graph import StateGraph, END

from src.settings import settings
from src.langchain.tools import update_user_name_tool, get_user_name_tool
from src.template.prompts import INTENT_CLASSIFIER_BASE_TEMPLATE
from src.database.models import ChatState


class ChatAgent:
    """Agente de chat con herramientas y memoria por sesión (thread_id)."""

    def __init__(self) -> None:
        self.llm = ChatOpenAI(
            model_name=settings.MODEL,
            temperature=0.3,
            openai_api_key=settings.API_KEY,
        )

        self.tools = [update_user_name_tool, get_user_name_tool]

        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", INTENT_CLASSIFIER_BASE_TEMPLATE),
                MessagesPlaceholder(variable_name="chat_history"),
                ("user", "{input}"),
                ("user", "thread_id: {thread_id}"),
                ("placeholder", "{agent_scratchpad}"),
            ]
        )

        self.agent_chain = create_tool_calling_agent(
            llm=self.llm, tools=self.tools, prompt=self.prompt
        )
        self.agent_executor = AgentExecutor(
            agent=self.agent_chain, tools=self.tools, verbose=False
        )

        self._memories: Dict[str, InMemoryChatMessageHistory] = {}

        self.agent_with_history = RunnableWithMessageHistory(
            self.agent_executor,
            get_session_history=lambda session_id: self._memories.setdefault(
                session_id, InMemoryChatMessageHistory()
            ),
            input_messages_key="input",
            history_messages_key="chat_history",
        )

        graph = StateGraph(state_schema=ChatState)
        graph.add_node("process", self._process_message)
        graph.add_edge("process", END)
        graph.set_entry_point("process")
        self.graph = graph.compile()

    async def _process_message(self, state: ChatState) -> ChatState:
        """
        Nodo único del grafo: recibe un ChatState, actualiza la memoria
        (si viene chat_history externo) y obtiene la respuesta del agente.
        """
        input_text: str = state.input
        incoming_history: List = state.chat_history or []
        thread_id: str = str(state.thread_id or "default")

        # -- Volcar historial externo (si viene) a la memoria de la sesión --
        memory = self._memories.setdefault(thread_id, InMemoryChatMessageHistory())
        if incoming_history:
            # Vaciar y re-cargar para sincronizar con datos externos
            memory.clear()
            for msg in incoming_history:
                print(msg)
                memory.add_message(msg)

        # -- Invocar al agente con memoria persistente ----------------------
        response = await self.agent_with_history.ainvoke(
            {"input": input_text, "thread_id": thread_id},
            config={"configurable": {"session_id": thread_id}},
        )

        output = response.get("output") if isinstance(response, dict) else str(response)

        # -- Extraer historial actualizado ----------------------------------
        updated_history: List = list(memory.messages)

        return ChatState(
            input=input_text,
            chat_history=updated_history,
            response=output,
            thread_id=thread_id,
        )

    async def run(self, input_text: str, chat_history: Optional[List] = None, thread_id: Optional[int] = None,):
        """
        Punto de entrada para código externo (por ejemplo, un bot de WhatsApp).

        Params
        ------
        input_text : str
            Mensaje recibido del usuario.
        chat_history : list[BaseMessage] | None
            Historial previo (HumanMessage / AIMessage). Si proviene del backend
            se sincroniza con la memoria antes de procesar el mensaje.
        thread_id : int | str | None
            Identificador único de la conversación.  Distintas sesiones de
            usuario deben usar valores distintos para no mezclar contextos.
        """
        print(chat_history)
        initial_state = ChatState(
            input=input_text,
            chat_history=chat_history or [],
            thread_id=thread_id,
        )
        result_state: ChatState = await self.graph.ainvoke(initial_state)
        return result_state
