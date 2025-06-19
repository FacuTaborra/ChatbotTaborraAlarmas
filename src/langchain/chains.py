from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage
from src.settings import settings
from src.template.prompts import INTENT_CLASSIFIER_BASE_TEMPLATE

class ChatChain:
    def __init__(self, api_key: str = None, model_name: str = None):
        """
        Inicializa la cadena de chat con el modelo y la temperatura especificados.

        Args:
            model_name (str): Nombre del modelo de OpenAI.
            temperature (float): Temperatura para la generación de texto.
        """

        self.api_key = settings.API_KEY or api_key
        self.model_name = settings.MODEL or model_name
        self.llm = ChatOpenAI(
            model_name=self.model_name,
            temperature=0.3,
            openai_api_key=self.api_key
        )
        self.prompt = ChatPromptTemplate.from_messages([
            MessagesPlaceholder(variable_name="chat_history"),
            ('user', "{input}"),
            ('system', INTENT_CLASSIFIER_BASE_TEMPLATE)
        ])

    def create_chain(self):
        """
        Crea una cadena de chat utilizando el modelo y el prompt definidos.

        Returns:
            LangChain chain object
        """
        chain = self.prompt | self.llm
        return chain
    
    def run(self, input_text: str, chat_history: list = []):
        chain = self.create_chain()

        response = chain.invoke({
            "input": input_text,
            "chat_history": chat_history
        })
        
        chat_history.append(HumanMessage(content=input_text))
        chat_history.append(AIMessage(content=response.content))
        print(f"🤖 Chathistory: {chat_history}")

        return {"chat_history": chat_history, "response": response.content}