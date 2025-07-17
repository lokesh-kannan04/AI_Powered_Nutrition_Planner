from django.http import JsonResponse
from django.contrib.sessions.backends.db import SessionStore
import json

def custom_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        try:
            data = json.loads(request.body)  # Get session key from request
            session_key = data.get('session_key')

            if not session_key:
                return JsonResponse({'error': 'Session key required'}, status=401)

            session = SessionStore(session_key=session_key)

            if not session.exists(session_key):
                return JsonResponse({'error': 'Invalid session, please log in'}, status=401)

            request.session = session  # Attach session to request object
            return view_func(request, *args, **kwargs)  # Call original view

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

    return wrapper
