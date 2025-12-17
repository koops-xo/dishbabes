from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import DishRotation, WashHistory
from datetime import date

def dishwasher(request):
    rotation, created = DishRotation.objects.get_or_create(id=1)

    # Ensure rotation reflects the current date (auto-rollover)
    rotation.auto_rollover()

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "done":
            # record that today's person washed, then advance one day
            WashHistory.objects.create(person=rotation.today(), date=date.today())
            rotation.rotate_by(1)
            messages.success(request, "Marked as washed — rotation updated.")
            return redirect("dishwasher")

        if action == "override":
            person = request.POST.get("person")
            if person in DishRotation.PEOPLE:
                rotation.set_today(person)
                messages.info(request, f"Override set — {person} is assigned for today.")
            else:
                messages.error(request, "Invalid person selected.")
            return redirect("dishwasher")

    history = WashHistory.objects.all()[:10]  # last 10 entries
    context = {
        "today": rotation.today(),
        "tomorrow": rotation.tomorrow(),
        "history": history,
    }
    return render(request, "dishwasher.html", context)

def home(request):
    people = ["Koops", "Remo"]

    return render(request, "dishwasher/home.html", {
        "people": people,
        "today": today,
        "tomorrow": tomorrow,
    })
