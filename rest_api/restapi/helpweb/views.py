from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from django_request_mapping import request_mapping

from android_rest.models import Product, User
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
                return redirect("/homepage")
            else:
                return render(request, 'loginfail.html')
        except:
            return render(request, 'loginfail.html')

    @request_mapping("/homepage", method="get")
    def homepage(self, request):
        try:
            if request.session['sessionid'] is not None:
                datalist = Product.objects.distinct().all()
                page = request.GET.get('page', '1')
                paginator = Paginator(datalist, 30)
                page_obj = paginator.get_page(page)
                datalists = User.objects.distinct().all()
                pages = request.GET.get('page', '1')
                paginators = Paginator(datalists, 10)
                page_objs = paginators.get_page(pages)
                context = {
                    'boards': page_obj,
                    'question_list': page_obj,
                    'page': page,
                    'name': page_objs,
                    'name_list': page_objs,
                    'name_page': pages}
                return render(request, 'homepage.html', context)
        except:
            return render(request, "loginfail.html")

    @request_mapping("/search", method="get")
    def search(self, request):
        datalist = Product.objects.distinct().all()
        search = request.GET.get('search','')
        if search:
            search_list = datalist.filter(
                Q(name_icontans=search) |
                Q(main_icontains=search) |
                Q(sub1_icontains=search)
            )
        page = request.GET.get('page', '1')
        paginator = Paginator(datalist, 30)
        page_obj = paginator.get_page(page)
        context = {'boards': page_obj,
                   'question_list': page_obj,
                   'page': page}
        return render(request, 'homepage.html', context)

    @request_mapping("/testpage", method="get")
    def testpage(self, request):
        try:
            if request.session['sessionid'] != None:
                return render(request, 'testpage.html')
        except:
            return render(request, 'login.html')

    @request_mapping("/logout", method="get")
    def logout(self, request):
        try:
            if request.session['sessionid'] != None:
                del request.session['sessionid']
                return redirect('/login')
            else:
                pass
        except:
            return redirect('/login')

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

    @request_mapping("/notepad", method="get")
    def notepad(self, request):
        try:
            if request.session['sessionid'] != None:
                return render(request, 'notepad.html')
        except:
            return render(request, 'login.html')

    @request_mapping("/notewriteimpl", method="post")
    def notewriteimpl(self, request):
        id = request.session["sessionid"]
        if id != None:
            writer = Manager.objects.get(id=id)
            info1 = request.POST["info1"]
            info2 = request.POST["info2"]
            info3 = request.POST["info3"]
            notepadmdl(writer=writer, info1=info1, info2=info2, info3=info3).save()
            return redirect('/homepage')
        else:
            return render(request, 'accessfail.html')

    @request_mapping("/tables", method="get")
    def tables(self, request):
        try:
            datalist = Product.objects.distinct().all()
            page = request.GET.get('page', '1')
            paginator = Paginator(datalist, 30)
            page_obj = paginator.get_page(page)
            context = {'boards': page_obj,
                       'question_list': page_obj,
                       'page': page}

            return render(request, 'homepage.html', context)
        except:
            return render(request, "loginfail.html")