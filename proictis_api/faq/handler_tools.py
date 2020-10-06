import os
import dialogflow_v2 as dialogflow
from config import Config
from google.protobuf.json_format import MessageToDict

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = Config.GOOGLE_APPLICATION_CREDENTIALS


def detect_intent_texts(project_id: str, session_id: str, text: str, language_code: str) -> dict:
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.types.TextInput(
        text=text, language_code=language_code)

    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(
        session=session, query_input=query_input)

    query_result = MessageToDict(response.query_result)

    return query_result
