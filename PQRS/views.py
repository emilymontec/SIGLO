from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .models import PQRS


class PQRSCreateView(LoginRequiredMixin, CreateView):
    model = PQRS
    fields = ['type', 'message']
    success_url = reverse_lazy('mypqrs_list')

    def form_valid(self, form):
        form.instance.client = self.request.user
        return super().form_valid(form)


@login_required
def my_pqrs_list(request):
    items = PQRS.objects.filter(client=request.user).order_by('-id')
    return render(request, 'pqrs/my_pqrs_list.html', {'items': items})


@staff_member_required
def admin_pqrs_list(request):
    items = PQRS.objects.select_related("client").all().order_by("-id")
    return render(request, "pqrs/admin_pqrs_list.html", {"items": items})


@staff_member_required
def admin_pqrs_edit(request, pqrs_id):
    pq = get_object_or_404(PQRS, pk=pqrs_id)

    if request.method == "POST":
        data = request.POST
        pq.type = data.get("type") or pq.type
        pq.message = data.get("message") or pq.message
        pq.status = data.get("status") or pq.status
        pq.save()
        return redirect("admin_pqrs_list")

    context = {
        "pq": pq,
        "form": {
            "type": pq.type,
            "message": pq.message,
            "status": pq.status,
        },
    }
    return render(request, "pqrs/admin_pqrs_form.html", context)
