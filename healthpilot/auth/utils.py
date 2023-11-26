# from django.core.mail import send_mail
# from django.conf import settings
# import uuid

# def send_activation_email(email, activation_token):
#     activation_url = 'http://localhost:8000/verification/' + activation_token
#     message = f'Please click the following link to activate your account: {activation_url}'
#     email_from = settings.EMAIL_HOST_USER
#     send_mail('Account activation', message, email_from, [email], fail_silently=False)


# def generate_token():
#     return str(uuid.uuid4())