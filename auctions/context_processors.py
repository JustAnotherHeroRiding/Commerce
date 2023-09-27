from .models import Watchlist


def watchlist_processor(request):
    if request.user.is_authenticated:
        watchlist = Watchlist.objects.filter(user=request.user).all().count()
        return {'wlistitems': watchlist}
    else:
        return {'wlistitems': 0}
