from typing import List, Optional, Dict

from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

from langgraph.graph import StateGraph, START, END

from src.settings import settings
from src.langchain.tools import update_user_name_tool, get_user_name_tool
from src.template.prompts import INTENT_CLASSIFIER_BASE_TEMPLATE
from src.database.models import AgentState


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
                MessagesPlaceholder(variable_name="messages"),
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
            history_messages_key="messages",
        )

        graph = StateGraph(state_schema=AgentState)
        graph.add_node("process", self._process_message)

        graph.add_edge(START, "process")
        graph.add_edge("process", END)
        
        self.graph = graph.compile()

    async def _process_message(self, state: AgentState) -> AgentState:
        input_text: str = state.input
        incoming_messages: List = state.messages or []
        thread_id: str = str(state.thread_id or "default")

        memory = self._memories.setdefault(thread_id, InMemoryChatMessageHistory())
        if incoming_messages:
            print(incoming_messages)
            memory.clear()
            for msg in incoming_messages:
                memory.add_message(msg)

        print(memory)

        response = await self.agent_with_history.ainvoke(
            {"input": input_text, "thread_id": thread_id},
            config={"configurable": {"session_id": thread_id}},
        )

        output = response.get("output") if isinstance(response, dict) else str(response)
        updated_messages: List = list(memory.messages)

        return AgentState(
            input=input_text,
            messages=updated_messages,
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
        initial_state = AgentState(
            input=input_text,
            messages=chat_history or [],
            thread_id=thread_id,
        )
        result_state = await self.graph.ainvoke(initial_state)
        # Si el resultado es un dict, convertilo a AgentState
        if isinstance(result_state, dict):
            result_state = AgentState(**result_state)
        return result_state
