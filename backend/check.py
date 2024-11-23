from langchain_community.chat_models import GigaChat
from gigachat.exceptions import ResponseError


# def check_gigachat_model_exists(api_key: str, model: str) -> bool:
#     try:
#         # Attempt to initialize the GigaChat model
#         gigachat = GigaChat(model=model, credentials=api_key, verify_ssl_certs=False)
#         available_models = gigachat.get_models()
#         model_ids = [model.id_ for model in available_models.data]
#         return model in model_ids
#     except ResponseError:
#         return False


def check_gigachat_model_exists(api_key: str, model: str) -> bool:
    try:
        # Attempt to initialize the GigaChat model
        gigachat = GigaChat(model=model, credentials=api_key, verify_ssl_certs=False)
        gigachat.
        return True
    except ResponseError:
        return False


api_key = "your_gigachat_api_key"
model_exists = check_gigachat_model_exists(api_key, model="GigaChat-Pro")
print(f"GigaChat model exists: {model_exists}")
