from social_django.middleware import SocialAuthExceptionMiddleware
from social_core.exceptions import AuthCanceled, AuthMissingParameter
from django.urls import reverse

class CustomSocialAuthExceptionMiddleware(SocialAuthExceptionMiddleware):
    def get_message(self, request, exception):
        msg = None
        if (isinstance(exception, AuthCanceled)):
            msg = "User canceled the auth process. Please, try again and fullfil the auth workflow."
        elif (isinstance(exception, AuthMissingParameter)):
            msg = None
        else:
            msg = "Auth failed. Please, uninstall the app from your account and start over."
        return msg
    def get_redirect_uri(self, request, exception):
        if(isinstance(exception, AuthMissingParameter)):
            return reverse('social:begin', args=['github'])
        return super().get_redirect_uri(request, exception)