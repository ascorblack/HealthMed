from rest_framework.response import Response


def gen_response(status_code: int = 200,
                 error: str | list | dict = "",
                 error_type: str = "",
                 details: str | list = "",
                 ) -> Response:
    response_json: dict[str, int | str | list | dict] = {
        "status": status_code
    }
    match status_code:
        case 200:
            response_json.update({
                "details": details
            })

        case 500:
            response_json.update({
                "error": error,
                "error_type": error_type
            })

        case _:
            response_json.update({
                "error": "",
                "error_type": "UNKNOWN_STATUS_CODE",
            })

    return Response(response_json, status=status_code)

