
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.http import url_has_allowed_host_and_scheme

User = get_user_model()


def register(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")
        role = request.POST.get("role", "Customer")

        if not username or not email or not password or not confirm_password:
            messages.error(request, "Please fill in all fields.")

        elif role not in ["Customer", "Vendor"]:
            messages.error(request, "Please select a valid account type.")

        elif password != confirm_password:
            messages.error(request, "Passwords do not match.")

        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")

        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")

        else:
            User.objects.create_user(
                username=username,
                email=email,
                password=password,
                role=role
            )

            messages.success(
                request,
                "Account created successfully! Please log in."
            )
            return redirect("login")

    return render(request, "accounts/register.html")


def website_login(request):
    if request.user.is_authenticated:
        return redirect("home")

    next_url = request.POST.get("next") or request.GET.get("next", "")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)

            messages.success(request, "Login successful!")

            if next_url and url_has_allowed_host_and_scheme(
                next_url,
                allowed_hosts={request.get_host()}
            ):
                return redirect(next_url)

            return redirect("home")

        messages.error(request, "Invalid username or password.")

    return render(
        request,
        "accounts/login.html",
        {"next": next_url}
    )


@login_required
def website_logout(request):
    if request.method == "POST":
        logout(request)
        messages.success(request, "You have logged out.")

    return redirect("home")


@login_required
def profile(request):
    return render(request, "accounts/profile.html", {
        "profile_user": request.user
    })


@login_required
def edit_profile(request):
    user = request.user

    if request.method == "POST":
        full_name = request.POST.get("full_name", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        address = request.POST.get("address", "").strip()

        if not email:
            messages.error(request, "Email is required.")
            return redirect("edit_profile")

        if User.objects.filter(email=email).exclude(pk=user.pk).exists():
            messages.error(request, "This email is already in use.")
            return redirect("edit_profile")

        user.full_name = full_name
        user.email = email
        user.phone = phone
        user.address = address

        if "profile_picture" in request.FILES:
            user.profile_picture = request.FILES["profile_picture"]

        user.save()

        messages.success(request, "Profile updated successfully!")
        return redirect("profile")

    return render(request, "accounts/edit_profile.html", {
        "profile_user": user
    })
