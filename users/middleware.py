from users.models import UserAuthToken, User


class AuthorizationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def get_user_from_token(self, token: str) -> User:
        _, token = token.split(' ') if token else (None, None)
        if not token or token == 'undefined':
            return None
        
        try:
            return UserAuthToken.objects.get(token=token).user
        except UserAuthToken.DoesNotExist:
            return None
    

    def __call__(self, request):
        if user := self.get_user_from_token(request.headers.get('Authorization')):
            request.user = user
   
        return self.get_response(request)
