from django.http import HttpResponse

HOME_PAGE_HTML = '<html><title>To-Do lists</title></html>'

def home_page(request):
    return HttpResponse(HOME_PAGE_HTML)
