from django.db.models import Q
from django.shortcuts import render , redirect, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from .models import Links
from .forms import LinkForm
from django.views import View
from django.contrib.auth.hashers import check_password
from django.contrib import messages
import json
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from sawo import createTemplate, getContext, verifyToken
from core.settings import API_KEY
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage

# For sawolabs authentication
createTemplate("templates/partials")


class Home(View):
    template = "home.html"

    def get(self, request):
        return render(request, self.template)

# --- The main dashboard view ---
class Dashboard(View):
    @method_decorator(login_required)
    def get(self, request):
        imagilinks = Links.objects.filter(author = request.user)
        context = {
            'links': imagilinks
        }
        return render(self.request, 'dashboard.html', context)


class LoginRedirect(View):
    def get(self, request):
        return redirect('/login')


class Login(View):
    template = "login.html"
    def get(self, request):
        user = self.request.user

        if user.is_authenticated:
            return redirect("/dashboard")

        config = {
            "auth_key": API_KEY,
            "identifier": "email",
            "to": "receive"
        }
        context = {"sawo":config}
        return render(request, self.template, context)


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('/')


# --- Validating payload recieved by Sawolabs api ---
class ReceivePayload(View):
    def post(self, request):
        payload = json.loads(request.body)["payload"]
            
        if verifyToken(payload):
            response = {
                "user_id": payload["user_id"],
                "created_on": payload["created_on"],
                "email": payload["identifier"],
                "identifier_type": payload["identifier_type"],
                "verification_token": payload["verification_token"],
                "customFieldInputValues": payload["customFieldInputValues"]
            }

            email = payload["identifier"]
            user_id = payload["user_id"]

            try:
                user = User.objects.get(username = email)
                login(request,user)
                return redirect("/dashboard")
            except User.DoesNotExist:
                user = User.objects.create_user(username=email,password = user_id)
                login(request,user)
                return redirect('/dashboard')

        else:
            response ={
                "error": "Verification failed."
            }
            return JsonResponse(response)


# ---- Saving the uploaded image ----
class Saveimagedata(View):
    template = "upload.html"
    @method_decorator(login_required)
    def get(self, request):
        return render(request, self.template)


    def post(self, request):
        if request.method == "POST":
            image = request.FILES['file'] if 'file' in request.FILES else None

            if image:
                fs = FileSystemStorage()
                file = fs.save(image.name, image)
                url = fs.url(file)
                return JsonResponse({"fileurl": url })
            return JsonResponse({"error": "Oops! Some error occured." })


# --- View for creating link ---
class Create(View):
    template = "create.html"
    @method_decorator(login_required)
    def get(self, request):

        if not request.GET.get("img"):
            return redirect('/upload')

        context = {}
        context['form'] = LinkForm()

        image_link = request.GET.get("img")
        context["form"].fields["seo_image"].initial = request.GET.get("img")
        context["form"].fields["author"].initial = request.user

        context['image_link'] = image_link
        context['author'] = request.user

        return render(request, self.template, context)

    def post(self, request):
        context = {}
        context['form'] = LinkForm()
        form = LinkForm(request.POST)
        if form.is_valid():
            shortened_object = form.save()
            new_url = request.build_absolute_uri('/preview/') + shortened_object.short_url
            return redirect(new_url)

        context['errors'] = "Please take different custom name , this is already taken."
        return render(request, self.template, context)


# --- Main view for generated links preview ---
class Preview(View):
    template = "preview.html"
    @method_decorator(login_required)
    def get(self, request, link_id):
        link = get_object_or_404(Links, short_url = link_id)

        url = request.build_absolute_uri('/u/') + link_id

        context = {
            "imagilink": url,
            "title": link.seo_title,
            "image": link.seo_image,
            "description": link.seo_description,
            "target_url": link.target_url
        }
        return render(request, self.template, context)


# --- View for deleting the generated links ---
class Delete(View):
    def post(self, request):
        l_id = json.loads(request.body.decode("utf-8"))["link"] 
        link = get_object_or_404(Links, short_url = l_id)
        try:
            link.delete()
            return JsonResponse({"success": "Link is successfully deleted!" })
        except:
            return JsonResponse({"error": "Oops! Some error occured."})


# --- View for redirecting the generated urls ---
class TargetForwardView(View):
    template = "output.html"
    def get(self, request, link_id):
        link = get_object_or_404(Links, short_url = link_id)

        context = {
            "title": link.seo_title,
            "image": link.seo_image,
            "description": link.seo_description,
            "target_url": link.target_url
        }
        return render(request, self.template, context)