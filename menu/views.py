from django.shortcuts import render


def main_page(request):
    context = {'title': 'Главная страница'}
    return render(request, 'menu/index.html', context=context)


def get_page(request, page_id):
    context = {'title': f'Это страница со ссылкой /{page_id}/'}
    return render(request, 'menu/index.html', context=context)
