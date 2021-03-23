from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from tensorflow import keras
from tensorflow.keras.preprocessing import image
import numpy as np
import os
from werkzeug.utils import secure_filename
from .forms import ImageUploadForm
import joblib

# Create your views here.

model = keras.models.load_model("accounts\model\model.h5", compile=False)
yield_model = joblib.load("accounts/model/new_model.sav")


def IndexView(request):
    return render(request, "index.html")


@login_required
def yieldPrediction(request):
    ip = request.META.get("REMOTE_ADDR")
    print(ip)
    if request.method == "POST":
        # area = request.POST.get("area")
        item = int(request.POST.get("selection"))
        average_temp = float(request.POST.get("at"))
        average_rainfall = float(request.POST.get("ar"))
        pesticides = float(request.POST.get("pt"))
        predicts_list = [42, item, average_rainfall, pesticides, average_temp]
        print(predicts_list)
        yield_predicts = yield_model.predict([predicts_list])

        # items = [
        #     "Maize",
        #     "Potatoes",
        #     "Rice",
        #     "Sorghum",
        #     "Soybeans",
        #     "Wheat",
        #     "Cassava",
        #     "Sweet potatoes",
        #     "Plantains",
        #     "Yams",
        # ]
        print(yield_predicts)
        return render(
            request, "yield_prediction.html", {"predicts": float(yield_predicts)}
        )
    return render(request, "yield_prediction.html")


@login_required
def DashboardView(request):
    return render(request, "dashboard.html", {"username": request.user})


def model_predict(img_path, model):
    img = image.load_img(img_path, grayscale=False, target_size=(64, 64))
    # show_img = image.load_img(img_path, grayscale=False, target_size=(64, 64))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = np.array(x, "float32")
    x /= 255
    preds = model.predict(x)
    return preds


def handle_uploaded_file(f, img_path):
    with open(img_path, "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)


@login_required
def diseaseDetection(request):
    form = ImageUploadForm(request.POST, request.FILES)
    if request.method == "POST" and "file" in request.FILES:
        f = request.FILES["file"]
        img_path = "images/" + str(request.user.id) + "test.jpg"
        handle_uploaded_file(f, img_path)
        # img_path = 'images/predict.jpg'
        # basepath = os.path.dirname(__file__)
        # file_path = os.path.join(basepath, "uploads", secure_filename(f.name))
        # f.save(file_path)
        preds = model_predict(img_path, model)
        print(preds[0])
        disease_class = [
            "Pepper__bell___Bacterial_spot",
            "Pepper__bell___healthy",
            "Potato___Early_blight",
            "Potato___Late_blight",
            "Potato___healthy",
            "Tomato_Bacterial_spot",
            "Tomato_Early_blight",
            "Tomato_Late_blight",
            "Tomato_Leaf_Mold",
            "Tomato_Septoria_leaf_spot",
            "Tomato_Spider_mites_Two_spotted_spider_mite",
            "Tomato__Target_Spot",
            "Tomato__Tomato_YellowLeaf__Curl_Virus",
            "Tomato__Tomato_mosaic_virus",
            "Tomato_healthy",
        ]
        a = preds[0]
        ind = np.argmax(a)
        print("Prediction:", disease_class[ind])
        result = disease_class[ind]
        return render(request, "disease_detection.html", {"pre_op": result})

    return render(request, "disease_detection.html")


def RegistrationView(request):
    if request.method == "POST":
        username = request.POST.get("susername")
        email = request.POST.get("email")
        password = request.POST.get("spassword")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        if User.objects.filter(username=username).exists():
            return HttpResponse(
                "<script>alert('username already available'); window.location.href = '/registration';</script>"
            )
        # if User.objects.exclude(pk=instance.pk).filter(username=username).exists():
        #     raise forms.ValidationError(u'Username "%s" is already in use.' % username)
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )
            user.save()
            return redirect("login")

    return render(
        request,
        "registration/registration.html",
    )


def LoginView(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, "dashboard.html", {"username": username})
            else:
                return HttpResponse("disable")
        else:
            return HttpResponse(
                "<script>alert('invalid login'); window.location.href = '/login';</script>"
            )
    else:
        pass

    return render(request, "registration/login.html")


def LogoutView(request):
    return render(request, "registration/logout.html")
