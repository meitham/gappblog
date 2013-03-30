from django import http


def home(request):
    return http.HttpResponse("Welcome to the new shiny blog.")
