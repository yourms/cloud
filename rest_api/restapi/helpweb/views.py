from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from django_request_mapping import request_mapping
from android_rest.models import Product, User
from helpweb.models import *
from django.views import View


# Create your views here.

def search_result(request, search_list):
    page = request.GET.get('page', '1')
    paginator = Paginator(search_list, 30)
    page_obj = paginator.get_page(page)
    context = {'board': page_obj,
               'question_list': page_obj,
               'page': page}
    return render(request, 'searchpage.html', context)


@request_mapping("")
class MyView(View):

    @request_mapping("/", method="get")
    def home(self, request):
        try:
            if request.session['sessionid'] is not None:
                return render(request, 'alreadylogin.html')
            else:
                pass
        except:
            return render(request, 'login.html')

    @request_mapping("/login", method="get")
    def login(self, request):
        try:
            if request.session['sessionid'] is not None:
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
                id = request.session["sessionid"]
                datalist = Product.objects.distinct().all()
                page = request.GET.get('page', '1')
                paginator = Paginator(datalist, 30)
                page_obj = paginator.get_page(page)
                all_product = Product.objects.filter().count()
                snack = Product.objects.filter(main='과자').count()
                desert = Product.objects.filter(main='디저트').count()
                noodles = Product.objects.filter(main='면류').count()
                unclassion = Product.objects.filter(main='미분류').count()
                room_temperature_hmr = Product.objects.filter(main='상온HMR').count()
                household_goods = Product.objects.filter(main='생활용품').count()
                lee_beauty = Product.objects.filter(main='이/미용').count()
                sauce = Product.objects.filter(main='소스').count()
                dairy_product = Product.objects.filter(main='유제품').count()
                beverage = Product.objects.filter(main='음료').count()
                coffee = Product.objects.filter(main='커피차').count()
                canned_snacks = Product.objects.filter(main='통조림/안주').count()
                home_clean = Product.objects.filter(main='홈클린').count()
                context = {
                    'id': id,
                    'boards': page_obj,
                    'question_list': page_obj,
                    'page': page,
                    'all_product': all_product,
                    'snack': snack,
                    'desert': desert,
                    'noodles': noodles,
                    'unclassion': unclassion,
                    'room_temperature_hmr': room_temperature_hmr,
                    'household_goods': household_goods,
                    'lee_beauty': lee_beauty,
                    'sauce': sauce,
                    'dairy_product': dairy_product,
                    'beverage': beverage,
                    'coffee': coffee,
                    'canned_snacks': canned_snacks,
                    'home_clean': home_clean
                }
                return render(request, 'homepage.html', context)
        except:
            return render(request, "loginfail.html")

    @request_mapping("/userinfo", method="get")
    def userinfo(self, request):
        datalists = User.objects.distinct().all()
        pages = request.GET.get('page', '1')
        paginators = Paginator(datalists, 10)
        page_objs = paginators.get_page(pages)
        context = {
            'name': page_objs,
            'name_list': page_objs,
            'name_page': pages,
        }
        return render(request, 'userinfo.html', context)

    @request_mapping("/search", method="get")
    def search(self, request):
        datalist = Product.objects.distinct().all()
        page = request.GET.get('page', '1')
        search = request.GET.get('search', '')
        if search:
            datalist = datalist.filter(
                Q(name__icontains=search) |  # 제목 검색
                Q(main__icontains=search) |  # 내용 검색
                Q(sub1__icontains=search)
            )
        paginator = Paginator(datalist, 30)  # 페이지당 10개씩 보여주기
        page_obj = paginator.get_page(page)
        context = {
            'board': page_obj,
            'question_list': page_obj,
            'page': page
        }
        return render(request, 'searchpage.html', context)
        # try:
        #     if search_type == '이름':
        #         search_list = datalist.filter(Q(name_icontans=search))
        #         page = request.GET.get('page', '1')
        #         paginator = Paginator(search_list, 30)
        #         page_obj = paginator.get_page(page)
        #         context = {'board': page_obj,
        #                    'question_list': page_obj,
        #                    'page': page}
        #
        #         return render(request, 'searchpage.html', context)
        #
        #     elif search_type == '대분류':
        #         search_list = datalist.filter(Q(main_icontans=search))
        #         page = request.GET.get('page', '1')
        #         paginator = Paginator(search_list, 30)
        #         page_obj = paginator.get_page(page)
        #         context = {'board': page_obj,
        #                    'question_list': page_obj,
        #                    'page': page}
        #
        #         return render(request, 'searchpage.html', context)
        #
        #     elif search_type == '소분류':
        #         search_list = datalist.filter(Q(sub1_icontans=search))
        #         page = request.GET.get('page', '1')
        #         paginator = Paginator(search_list, 30)
        #         page_obj = paginator.get_page(page)
        #         context = {'board': page_obj,
        #                    'question_list': page_obj,
        #                    'page': page}
        #
        #         return render(request, 'searchpage.html', context)
        # except:
        #     raise

    @request_mapping("/testpage", method="get")
    def testpage(self, request):
        try:
            if request.session['sessionid'] is not None:
                return render(request, 'testpage.html')
        except:
            return render(request, 'login.html')

    @request_mapping("/logout", method="get")
    def logout(self, request):
        try:
            if request.session['sessionid'] is not None:
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
                Manager(idweb=id, passwordweb=password, emailweb=email, phoneweb=phone1 + phone2 + phone3,
                        addressweb=address).save()
                request.session['sessionid'] = id
                return redirect('/')
            else:
                return render(request, 'registerfail.html')

    @request_mapping("/notepad", method="get")
    def notepad(self, request):
        try:
            if request.session['sessionid'] is not None:
                return render(request, 'notepad.html')
        except:
            return render(request, 'login.html')

    @request_mapping("/notewriteimpl", method="post")
    def notewriteimpl(self, request):
        id = request.session["sessionid"]
        if id is not None:
            writer = Manager.objects.get(id=id)
            info1 = request.POST["info1"]
            info2 = request.POST["info2"]
            info3 = request.POST["info3"]
            Notepadmdl(writer=writer, info1=info1, info2=info2, info3=info3).save()
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
