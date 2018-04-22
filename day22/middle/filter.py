from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse
class Ip(MiddlewareMixin):
    def process_request(self, request):
        ip = request.META['REMOTE_ADDR']
        list = ip.split('.')
        if int(list[3]) > 20:
            return HttpResponse('hehe')

    def process_response(self, request, response):
        print(1)
        return response