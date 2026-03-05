from django.shortcuts import render

# Create your views here.
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from .models import SubService
from .context import SERVICE_GROUPS, SERVICE_GROUP_SLUGS

def service_group_page(request, group_slug):
    if group_slug not in SERVICE_GROUP_SLUGS:
        raise Http404("Service not found")

    group = next(g for g in SERVICE_GROUPS if g["slug"] == group_slug)

    subservices = SubService.objects.filter(service_group=group_slug, active=True)

    # Wireframe: header + dynamic cards + FAQ/coverage sections (handled in template)
    return render(
        request,
        "services/service_group.html",
        {"group": group, "subservices": subservices},
    )

def subservice_detail(request, group_slug, subservice_slug):
    if group_slug not in SERVICE_GROUP_SLUGS:
        raise Http404("Service not found")

    subservice = get_object_or_404(
        SubService,
        service_group=group_slug,
        slug=subservice_slug,
        active=True,
    )

    # Wireframe: title + long description + Book Now CTA
    return render(
        request,
        "services/subservice_detail.html",
        {"subservice": subservice, "group_slug": group_slug},
    )
