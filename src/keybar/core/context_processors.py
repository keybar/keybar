from operator import attrgetter

from allauth.socialaccount import providers


def socialaccount(request):
    ctx = {'providers': sorted(providers.registry.get_list(), key=attrgetter('name'))}
    return {'socialaccount': ctx}
