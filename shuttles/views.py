from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from dashboard.supporting_func import *
from shuttles.models import Shuttle
from dashboard.supporting_func import getUser
from django.contrib import messages
from shuttles.forms import *
from django.views.generic import ListView


class ShuttleListView(ListView):
    template_name = "home/shuttles/all-shuttles.html"
    model = Shuttle
    context_object_name = "all_shuttles"
    page = "shuttles"
    single_shuttle = None

    # def get_queryset(self):
    #     self.user = getUser(self.request.user)
    #     driver_id = self.kwargs.get("driver_id")
    #     all_drivers = Driver.objects.filter(organization=self.user.organization)
    #     single_driver = None

    #     if driver_id:
    #         if driver_id.isdigit():
    #             single_driver = Driver.objects.filter(
    #                 id=driver_id, organization=self.user.organization
    #             ).first()

    #             if single_driver:
    #                 self.single_driver = single_driver
    #                 return all_drivers

    #         messages.error(
    #             self.request,
    #             "Driver doesn't exist with this id OR you don't have access",
    #         )

    #     self.single_driver = single_driver
    #     return all_drivers

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page"] = "shuttles"
        return context

    # def get(self, *args, **kwargs):
    #     print(args, kwargs, self.single_driver)
    #     return super(DriverListView, self).get(*args, **kwargs)


from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin
from django.urls import reverse


class ShuttleDetailView(DetailView):
    model = Shuttle
    form_class = ShuttleForm
    context_object_name = "single_shuttle"
    template_name = "home/shuttles/all-shuttles.html"
    page = "shuttles"
    temp_obj = True

    def get_object(self):
        queryset = self.get_queryset()
        shuttle_id = self.kwargs.get("pk")
        if not shuttle_id:
            return None
        shuttle = queryset.filter(id=shuttle_id).first()
        if not shuttle:
            messages.error(
                self.request,
                "Shuttle doesn't exist with this id OR you don't have access",
            )
            self.temp_obj = False
        return shuttle

    def get_queryset(self):
        user = getUser(self.request.user)
        return self.model.objects.filter(organization=user.organization)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context["all_shuttles"] = self.get_queryset()
        context["page"] = "shuttles"
        return context

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        if not self.temp_obj:
            return redirect("shuttles:all")
        return super(ShuttleDetailView, self).get(request, args, kwargs)


def get_pre_context(organization, form_title, shuttle_id):
    queryset = Shuttle.objects.filter(organization=organization)
    shuttle = queryset.filter(id=shuttle_id).first() if shuttle_id else None
    return {
        "page": "shuttles",
        "all_shuttles": queryset,
        "shuttle": shuttle,
        "form_title": form_title,
    }


@login_required
def edit_shuttle(request, shuttle_id):
    if not shuttle_id.isdigit():
        messages.error(request, "Given shuttle id is invalid")
        return redirect("shuttles:all")
    user = getUser(request.user)
    context = get_pre_context(user.organization, "Update shuttle details", shuttle_id)
    shuttle = context["shuttle"]
    if shuttle:
        if request.method == "POST":
            shuttle_form = ShuttleForm(request.POST, instance=shuttle)
            if shuttle_form.is_valid():
                shuttle_form.save()
                messages.success(
                    request, "Shuttle details has been updated successfully!"
                )
                return redirect("shuttles:select-shuttle", pk=shuttle.id)
        else:
            shuttle_form = ShuttleForm(instance=shuttle)
        context["shuttle_form"] = shuttle_form
        return render(request, "home/shuttles/all-shuttles.html", context)
    else:
        messages.error(
            request, "Shuttle doesn't exist with this id OR you don't have access"
        )
        return redirect("shuttles:all")


@login_required
def add_shuttle(request):
    user = getUser(request.user)
    context = get_pre_context(user.organization, "Add new shuttle", None)
    if request.method == "POST":
        shuttle_form = ShuttleForm(request.POST)
        if shuttle_form.is_valid():
            data = shuttle_form.cleaned_data
            new_shuttle = Shuttle(organization=user.organization, **data)
            new_shuttle.save()
            messages.success(request, "Shuttle has been added successfully")
            return redirect("shuttles:all")
    else:
        shuttle_form = ShuttleForm()
    context["shuttle_form"] = shuttle_form
    return render(request, "home/shuttles/all-shuttles.html", context)


@login_required
def delete_shuttle(request, shuttle_id):
    if not shuttle_id.isdigit():
        messages.error(request, "Given shuttle id is invalid")
        return redirect("shuttles:all")
    user = getUser(request.user)
    context = get_pre_context(user.organization, "Add new shuttle", shuttle_id)
    if context["shuttle"]:
        context["shuttle"].delete()
        messages.success(request, "Shuttle has been deleted successfully!")
    return redirect("shuttles:all")
