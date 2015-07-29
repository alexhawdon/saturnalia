from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from models import NewsItem
from functions import make_category_list

def news_item_detail(request, article_id):
    article = NewsItem.objects.get(id=article_id)
    category_list = make_category_list()
    return render_to_response('news_item_detail.html',
                       {'article': article,
                        'category_list': category_list},
                       context_instance=RequestContext(request))

def news_items(request, page=1, category="all"):
    if category == "all":
        news_items = NewsItem.objects.all()
        pagination_prefix="/news/page/"
    else:
        news_items = NewsItem.objects.filter(category__name__iexact=category.replace('-', ' '))
        pagination_prefix="/news/tag/"+category+"/page/"
    
    news_paginator = Paginator(news_items, 5)
    
    try:
        page = news_paginator.page(page)
    except (EmptyPage, InvalidPage):
        page = news_paginator.page(news_paginator.num_pages)
        
    pages = news_paginator.num_pages - 1
        
    category_list = make_category_list()
    
    return render_to_response('news_items.html',
                              {'page': page,
                               'page_range': news_paginator.page_range,
                               'pages': pages,
                               'category_list': category_list,
                               'pagination_prefix': pagination_prefix},
                               context_instance=RequestContext(request))
