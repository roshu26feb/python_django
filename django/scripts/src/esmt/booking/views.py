from django.shortcuts import render


def r2(request):
    return render(request, 'booking/r2.html', {})


def r3(request):
    return render(request, 'booking/r3.html', {})


def plato(request):
    return render(request, 'booking/plato.html', {})


def och(request):
    return render(request, 'booking/och.html', {})
