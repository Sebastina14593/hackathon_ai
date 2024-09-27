from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_models import GigaChat
from langchain.chains import create_retrieval_chain
from langchain_community.embeddings.gigachat import GigaChatEmbeddings
from langchain_community.vectorstores import LanceDB
from langchain.schema import Document
import lancedb
import pandas as pd

auth = 'ZTRiNzRjNzgtYzIwNC00YzdlLWFmZTUtMDY2M2I5MWYxNTlmOjYyNjk2OTU4LWI0MjAtNDQxOS05ZTc3LWFjNzA5Y2EwZmI0OQ=='

file_path = 'messanger/knowledgebase/AIData БЗ Даниил.xlsx'  # Ваш путь к файлу
content_columns = ['Вопросы', 'Ответы']  # Столбцы, которые пойдут в контент
metadata_column = 'Тематики'  # Столбец, который будет в метаданных


# Функция для построчной загрузки данных из .xlsx файла
def load_docs_from_xlsx(file_path, content_columns, metadata_column):
    # Считываем Excel файл в DataFrame
    df = pd.read_excel(file_path)

    docs = []

    # Проходимся по каждой строке DataFrame
    for _, row in df.iterrows():
        # Извлекаем содержимое для документа (например, несколько столбцов)
        content = "\n".join([f"{col}: {row[col]}" for col in content_columns])

        # Извлекаем метаданные (один столбец)
        metadata = {metadata_column: row[metadata_column]}

        # Создаем документ с контентом и метаданными
        doc = Document(
            page_content=content,
            metadata=metadata
        )
        docs.append(doc)

    return docs


def create_vector_store(docs, embedding):
    return LanceDB.from_documents(docs, embedding=embedding)


def create_document_chain(auth):
    llm = GigaChat(credentials=auth, model='GigaChat-Pro', verify_ssl_certs=False, profanity_check=False)
    prompt = ChatPromptTemplate.from_template(
        '''Ответь на вопрос пользователя. Используй при этом только информацию из контекста. Если в контексте нет информации для ответа, сообщи об этом пользователю. Контекст: {context} Вопрос: {input} Ответ:''')
    return create_stuff_documents_chain(llm=llm, prompt=prompt)


def database(embedding):
    docs = load_docs_from_xlsx(file_path, content_columns, metadata_column)
    url = 'data/aidata'
    db = lancedb.connect(url)
    # Используем LanceDB для хранения документов с метаданными
    LanceDB.from_documents(docs, embedding=embedding, connection=db)


# Функция для получения ответа и списка метаданных
def get_answer_and_metadata(question, embedding, llm):
    url = 'data/aidata'
    db = lancedb.connect(url)
    vector_store = LanceDB(db, embedding, 'data/aidata')
    # Создаем извлекающий компонент
    embedding_retriever = vector_store.as_retriever(search_kwargs={"k": 10})

    # Создаем цепочку документов и цепочку извлечения
    document_chain = create_document_chain(auth)
    retrieval_chain = create_retrieval_chain(embedding_retriever, document_chain)
    # Выполняем запрос к цепочке и получаем отобранные документы
    results = embedding_retriever.get_relevant_documents(question)

    # Список для хранения метаданных
    metadata_list = [doc.metadata[metadata_column] for doc in results if metadata_column in doc.metadata]

    # Вызываем саму цепочку для получения ответа
    resp = retrieval_chain.invoke({'input': question})

    return resp["answer"], metadata_list

def gigachat_response(user_question):
    embedding = GigaChatEmbeddings(credentials=auth, verify_ssl_certs=False)
    llm = GigaChat(credentials=auth, model='GigaChat-Pro', verify_ssl_certs=False, profanity_check=False)
    database(embedding)
    #Получаем ответ и метаданные
    answer, metadata_values = get_answer_and_metadata(user_question, embedding, llm)
    return answer