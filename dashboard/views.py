# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import date
from .models import DishRotation, WashHistory  # fixed typo

def dishwasher(request):
    # Always work with the singleton rotation
    rotation, created = DishRotation.objects.get_or_create(id=1)
    rotation.auto_rollover()  # keep rotation up-to-date

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "done":
            # Record today's wash and move rotation forward
            WashHistory.objects.create(person=rotation.today(), date=date.today())
            rotation.rotate_by(1)
            messages.success(request, "Marked as washed — rotation updated.")
            return redirect("dishwasher")

        elif action == "override":
            person = request.POST.get("person", "").strip()
            # normalize to match class constants
            if person in DishRotation.PEOPLE:
                rotation.set_today(person)
                messages.info(request, f"Override set — {person} is assigned for today.")
            else:
                messages.error(request, "Invalid person selected.")
            return redirect("dishwasher")

    # Show last 10 wash entries
    history = WashHistory.objects.all()[:10]

    context = {
        "today": rotation.today(),
        "tomorrow": rotation.tomorrow(),
        "history": history,
        "people": DishRotation.PEOPLE,
    }
    return render(request, "dishwasher.html", context)


def home(request):
    rotation, created = DishRotation.objects.get_or_create(id=1)
    rotation.auto_rollover()

    context = {
        "people": DishRotation.PEOPLE,
        "today": rotation.today(),
        "tomorrow": rotation.tomorrow(),
    }
    return render(request, "dishwasher/home.html", context)