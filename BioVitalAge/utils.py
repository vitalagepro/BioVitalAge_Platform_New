import time
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request as GoogleRequest
from googleapiclient.discovery import build
from social_django.utils import load_strategy
from social_django.models import UserSocialAuth
import logging
from django.contrib.auth.models import AnonymousUser



# Set up logging
logger = logging.getLogger(__name__)

def get_gmail_emails_for_user(user):
    try:
        # Verifica che l'utente sia valido
        if not user or isinstance(user, AnonymousUser):
            logger.warning("Tentativo di recuperare email da utente non autenticato o anonimo.")
            return []

        # Recupera social auth
        user_social = UserSocialAuth.objects.get(user=user, provider="google-oauth2")
        extra_data = user_social.extra_data

        # Costruisci le credenziali
        credentials = Credentials(
            token=extra_data.get("access_token"),
            refresh_token=extra_data.get("refresh_token"),
            token_uri="https://oauth2.googleapis.com/token",
            client_id=extra_data.get("client_id"),
            client_secret=extra_data.get("client_secret"),
            scopes=["https://www.googleapis.com/auth/gmail.readonly"],
        )

        # Refresh se necessario
        if extra_data.get('auth_time', 0) + 3600 < int(time.time()):
            strategy = load_strategy()
            user_social.refresh_token(strategy)
            credentials.token = user_social.extra_data['access_token']

        if not credentials.valid:
            credentials.refresh(GoogleRequest())
            user_social.extra_data["access_token"] = credentials.token
            user_social.save()

        # Costruisci il servizio Gmail
        service = build("gmail", "v1", credentials=credentials, static_discovery=False)
        results = service.users().messages().list(userId="me", maxResults=5, q="is:unread").execute()
        messages = results.get("messages", [])

        emails = []
        for msg in messages:
            msg_data = service.users().messages().get(userId="me", id=msg["id"], format="metadata").execute()
            headers = msg_data.get("payload", {}).get("headers", [])
            message_id = msg["id"]
            emails.append({
                "subject": next((h["value"] for h in headers if h["name"] == "Subject"), "No Subject"),
                "from": next((h["value"] for h in headers if h["name"] == "From"), "No Sender"),
                "date": next((h["value"] for h in headers if h["name"] == "Date"), "No Date"),
                "link": f"https://mail.google.com/mail/u/0/#all/{message_id}",  # 👈 URL diretto
            })

        return emails

    except UserSocialAuth.DoesNotExist:
        logger.warning(f"⚠️ Nessun account Gmail collegato per l'utente: {user}")
    except Exception as e:
        logger.exception("Errore durante il recupero delle email:", exc_info=True)

    return []