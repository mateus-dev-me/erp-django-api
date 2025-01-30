from rest_framework.exceptions import APIException


class AuthenticationError(Exception):
    """Base class for authentication-related errors."""

    def __init__(self, message: str):
        super().__init__(message)


class InvalidTokenError(AuthenticationError):
    """Raised when a token is invalid or expired."""

    def __init__(self, message: str = 'Token inválido ou expirado.'):
        super().__init__(message)


class UserNotFoundError(AuthenticationError):
    """Raised when a user is not found."""

    def __init__(self, message: str = 'Usuário não encontrado.'):
        super().__init__(message)


class InactiveUserError(AuthenticationError):
    """Raised when a user is inactive."""

    def __init__(self, message: str = 'Usuário desativado.'):
        super().__init__(message)


class UserAlreadyExistsException(APIException):
    status_code = 400
    default_detail = 'Este e-mail já está registrado na plataforma.'
    default_code = 'user_already_exists'


class InvalidAccountTypeException(APIException):
    status_code = 400
    default_detail = 'Tipo de usuário inválido.'
    default_code = 'invalid_account_type'


class EnterpriseNotFoundException(APIException):
    status_code = 404
    default_detail = 'A empresa especificada não existe.'
    default_code = 'enterprise_not_found'


class EnterpriseAlreadyExistsException(APIException):
    status_code = 400
    default_detail = 'Este cnpj já está cadastrado na plataforma.'
    default_code = 'enterprise_already_exists'


class EmployeeNotFoundException(APIException):
    status_code = 404
    default_detail = 'Este usuário não é um funcionário.'
    default_code = 'employee_not_found'
