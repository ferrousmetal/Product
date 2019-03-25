from hashlib import md5
from PriceBook_update import settings
from show_update_list.models import Z_Category

def global_settings(request):
    category_list = Z_Category.objects.all()
    return locals()

def get_hash(str, salt=None):
    str = '!@#$%'+str+'&^**('
    if salt:
        str = str + salt
    sh = md5()
    sh.update(str.encode('utf-8'))
    return sh.hexdigest()


def quick_sort(qlist):
    if qlist == []:
        return []
    else:
        qfirst = qlist[0]
        qless = quick_sort([l for l in qlist[1:] if l < qfirst])
        qmore = quick_sort([m for m in qlist[1:] if m >= qfirst])
        return qless + [qfirst] + qmore


from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
def Page(queryset,page):
    paginator = Paginator(queryset, 5)  # Show 25 contacts per page
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    return contacts

def Page1(queryset,page):
    paginator = Paginator(queryset, 15)  # Show 25 contacts per page
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    return contacts