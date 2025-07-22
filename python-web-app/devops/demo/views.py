from django.shortcuts import render, HttpResponse


def demo(request):
    content = """
    <h1>We did it!</h1>

    """
    return HttpResponse(content)