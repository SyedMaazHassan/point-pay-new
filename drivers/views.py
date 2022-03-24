from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from dashboard.supporting_func import *
from drivers.models import Driver
from dashboard.supporting_func import getUser
from django.contrib import messages
from drivers.forms import *
from django.views.generic import ListView


class DriverListView(ListView):
    template_name = "home/drivers/all-drivers.html"
    model = Driver
    context_object_name = "all_drivers"
    page = "drivers"
    single_driver = None

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
        context["page"] = "drivers"
        return context

    # def get(self, *args, **kwargs):
    #     print(args, kwargs, self.single_driver)
    #     return super(DriverListView, self).get(*args, **kwargs)


from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin
from django.urls import reverse


class DriverDetailView(DetailView):
    model = Driver
    form_class = DriverForm
    context_object_name = "single_driver"
    template_name = "home/drivers/all-drivers.html"
    page = "drivers"
    temp_obj = True

    def get_object(self):
        queryset = self.get_queryset()
        driver_id = self.kwargs.get("pk")
        if not driver_id:
            return None
        driver = queryset.filter(id=driver_id).first()
        if not driver:
            messages.error(
                self.request,
                "Driver doesn't exist with this id OR you don't have access",
            )
            self.temp_obj = False
        return driver

    def get_queryset(self):
        user = getUser(self.request.user)
        return self.model.objects.filter(organization=user.organization)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context["all_drivers"] = self.get_queryset()
        context["page"] = "drivers"
        return context

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        if not self.temp_obj:
            return redirect("drivers:all")
        return super(DriverDetailView, self).get(request, args, kwargs)


def get_pre_context(organization, form_title, driver_id):
    queryset = Driver.objects.filter(organization=organization)
    driver = queryset.filter(id=driver_id).first() if driver_id else None
    return {
        "page": "drivers",
        "all_drivers": queryset,
        "driver": driver,
        "form_title": form_title,
    }


@login_required
def edit_driver(request, driver_id):
    if not driver_id.isdigit():
        messages.error(request, "Given driver id is invalid")
        return redirect("drivers:all")
    user = getUser(request.user)
    context = get_pre_context(user.organization, "Update driver details", driver_id)
    driver = context["driver"]
    if driver:
        if request.method == "POST":
            driver_form = DriverForm(request.POST, request.FILES, instance=driver)
            if driver_form.is_valid():
                driver_form.save()
                messages.success(
                    request, "Driver details has been updated successfully!"
                )
                return redirect("drivers:select-driver", pk=driver.id)
        else:
            driver_form = DriverForm(instance=driver)
        context["driver_form"] = driver_form
        return render(request, "home/drivers/all-drivers.html", context)
    else:
        messages.error(
            request, "Driver doesn't exist with this id OR you don't have access"
        )
        return redirect("drivers:all")


@login_required
def add_driver(request):
    user = getUser(request.user)
    context = get_pre_context(user.organization, "Add new driver", None)
    if request.method == "POST":
        driver_form = DriverForm(request.POST, request.FILES)
        if driver_form.is_valid():
            data = driver_form.cleaned_data
            new_driver = Driver(organization=user.organization, **data)
            new_driver.save()
            messages.success(request, "Driver has been added successfully")
            return redirect("drivers:all")
    else:
        driver_form = DriverForm()
    context["driver_form"] = driver_form
    return render(request, "home/drivers/all-drivers.html", context)


@login_required
def delete_driver(request, driver_id):
    if not driver_id.isdigit():
        messages.error(request, "Given driver id is invalid")
        return redirect("drivers:all")
    user = getUser(request.user)
    context = get_pre_context(user.organization, "Add new driver", driver_id)
    if context["driver"]:
        context["driver"].delete()
        messages.success(request, "Driver has been deleted successfully!")
    return redirect("drivers:all")
