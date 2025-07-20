from django.shortcuts import render, HttpResponse


def demo(request):
    content = """
    <h1>Likega ku dhufo iyo Subababa Iscriba</h1>

    """
    return HttpResponse(content)