from typing import Dict

from rest_framework_simplejwt.tokens import (
    RefreshToken,
)

from accounts.models import User


def get_token(user: User) -> Dict:
    """Generate JWT tokens for the authenticated user."""
    token = RefreshToken.for_user(user)
    return {
        'refresh': str(token),
        'access_token': str(token.access_token),
    }
