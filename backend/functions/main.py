from firebase_functions import https_fn
from firebase_admin import initialize_app

initialize_app()


@https_fn.on_request()
def hello_world(request: https_fn.Request) -> https_fn.Response:
    return https_fn.Response("التبيق جاهز للعمل", status=200)