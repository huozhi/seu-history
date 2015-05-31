import json
from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from django.core.context_processors import csrf

from django.contrib import auth  


# Create your views here.
class Authenticate(View):
    def get(self, request):
        context = {}
        context.update(csrf(request))
        return render(request, 'index.html', context)

    def post(self, request):
        post = json.loads(request.body)
        try:
            username = post.get('username')
            password = post.get('password')
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:  
                auth.login(request, user)
                return JsonResponse({'login': True})
        except Exception, e:
            print e
        return JsonResponse({'login': False})

