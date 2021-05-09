import json

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from result.utils import process_message


class PrivacyView(TemplateView):
    template_name = "privacy.html"


class TermsView(TemplateView):
    template_name = "terms.html"


@csrf_exempt
def receive_message(request):
    if request.method == 'POST':
        print("===================== its a separator for see view-wise logs in heroku cli")
        process_message(json.loads(request.body.decode("utf-8")))
        return HttpResponse('Message Processed')

    # if get request
    if request.GET.get("hub.verify_token") == settings.FB_VERIFY_TOKEN:
        return HttpResponse(request.GET.get("hub.challenge"))
    return HttpResponse('Hmm, why are you here?')