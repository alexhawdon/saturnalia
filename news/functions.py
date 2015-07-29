def make_category_list():
    from models import NewsItem, NewsCategory
    cat_list = []
    for cat in NewsCategory.objects.all():
        name = cat.name
        url = cat.get_absolute_url()
        count = len(NewsItem.objects.filter(category=cat))
        cat_list.append({'name': name, 'url': url, 'count': count})
    return cat_list
