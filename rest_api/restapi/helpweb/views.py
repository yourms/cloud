from django.shortcuts import render, redirect
from django_request_mapping import request_mapping
from helpweb.models import *
from django.views import View

# Create your views here.

@request_mapping("")
class MyView(View):

    @request_mapping("/", method="get")
    def home(self,request):
        try:
            if request.session['sessionid'] !=None:
                return render(request,'alreadylogin.html')
            else:
                pass
        except:
            return render(request,'login.html')

    @request_mapping("/login", method="get")
    def login(self, request):
        try:
            if request.session['sessionid'] != None:
                return render(request, 'alreadylogin.html')
            else:
                pass
        except:
            return render(request, 'login.html')

    @request_mapping("/loginimpl", method="post")
    def loginimpl(self, request):
        idweb = request.POST["id"]
        passwordweb = request.POST["password"]
        try:
            mgr = Manager.objects.get(idweb=idweb)
            if mgr.passwordweb == passwordweb:
                request.session["sessionid"] = mgr.idweb
                # context = {'obj':mgr}
                return redirect("/index")
            else:
                return render(request, 'loginfail.html')
        except:
            return render(request, 'loginfail.html')

    @request_mapping("/index", method="get")
    def index(self, request):
        try:
            if request.session['sessionid'] != None:
                return render(request, 'index.html')
        except:
            return render(request, 'accessfail.html')

    @request_mapping("/logout", method="get")
    def logout(self, request):
        try:
            if request.session['sessionid'] != None:
                del request.session['sessionid']
                return redirect('/')
            else:
                pass
        except:
            return redirect('/')

    @request_mapping("/register", method="get")
    def register(self, request):
        return render(request, 'register.html')

    @request_mapping("/registerimpl", method="post")
    def registerimpl(self, request):
        id = request.POST["id"]
        password = request.POST["password"]
        passwordchk = request.POST["passwordchk"]
        email = request.POST["email"]
        phone1 = request.POST["phone1"]
        phone2 = request.POST["phone2"]
        phone3 = request.POST["phone3"]
        address = request.POST["address"]

        try:
            Manager.objects.get(id=id)
            return render(request, 'registerfail.html')
        except:
            if password == passwordchk:
                Manager(idweb=id, passwordweb=password, emailweb=email, phoneweb=phone1+phone2+phone3, addressweb=address).save();
                request.session['sessionid'] = id;
                return redirect('/')
            else:
                return render(request, 'registerfail.html')