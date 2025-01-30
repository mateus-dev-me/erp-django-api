from rest_framework.exceptions import APIException

class MissingFieldException(APIException):
    status_code = 400
    default_detail = "Um ou mais campos obrigatórios estão ausentes."
    default_code = "missing_field"
