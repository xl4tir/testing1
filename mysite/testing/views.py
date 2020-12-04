from django.shortcuts import render
from .models import AllTests, Tests, Answers, Tests_complete, Answers_complete, Test_complete
from django.http import Http404, HttpResponseRedirect,HttpResponse
import datetime
import random
from django.urls import reverse, reverse_lazy
import random
import string
from django.contrib.auth.views import LoginView, LogoutView
from .forms import AuthUserForm, RegisterUserForm
from django.contrib.auth.models import User
from django.views.generic import CreateView



class MyprojectLoginView(LoginView):

    template_name = 'testing/login.html'
    form_class = AuthUserForm
    success_url = reverse_lazy('testing:profile')
    def get_success_url(self):
        return self.success_url

class RegisterUserView(CreateView):
    model = User
    template_name = 'testing/register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('testing:login')
    success_msg = "Користувач успішно створений"

class MyProjectLogout(LogoutView):
    next_page = reverse_lazy('testing:login')

def profile(request):
    latest_complete_list = Test_complete.objects.filter(author = request.user)
    latest_created_list = AllTests.objects.filter(author = request.user)

    return  render(request, "testing/profile.html", {"latest_complete_list":latest_complete_list, 'latest_created_list':latest_created_list})

def index(request):
    latest_popular_list = AllTests.objects.order_by('-number_passed')[:5]
    return  render(request, "testing/index.html", {'latest_popular_list':latest_popular_list})

def test(request):
    latest_tests_list = AllTests.objects.order_by('-id')[:100]
    return  render(request, "testing/test.html", {'latest_tests_list':latest_tests_list})

def about_test(request, testcode):
    try:
        test = AllTests.objects.get(testcode = testcode)
        questions = Tests.objects.filter(testcode = testcode);
        answers = Answers.objects.filter(testcode = testcode);
        token = random_string_generator()+"-"+str(testcode)

    except:
        raise Http404("Тест не знайдено!")

    return  render(request, "testing/about_test.html", {'test':test,'questions':questions,'answers':answers ,'token':token})

def create(request):
    if request.user.is_authenticated is not True:
        return HttpResponseRedirect(reverse('testing:login'))
    else:
        return render(request, 'testing/create.html')

def create_page(request):
    if request.user.is_authenticated is not True:
        return HttpResponseRedirect(reverse('testing:home'))
    else:

        i = 0
        alltest = AllTests.objects.order_by('id')
        if alltest:
            while(i<1):
                code = random.randint(111111, 999999)
                for a in alltest:
                    if code == a.testcode:
                        i = i - 1
                    else:
                        i = i + 1
        else:
            code = 111111

        a = AllTests.objects.create(testname = request.POST['name'], author=request.user, date = datetime.datetime.now(), testcode = code )
        a.refresh_from_db()
        return HttpResponseRedirect(reverse('testing:builder', args = (code,)))


def builder(request, code):
    author = str(AllTests.objects.get(testcode = code).author)
    user = str(request.user)

    if request.user.is_authenticated is not True:
        return HttpResponseRedirect(reverse('testing:home'))

    else:
        if author == user:
            test = AllTests.objects.get(testcode = code)
            questions = Tests.objects.filter(testcode = code)
            answers = Answers.objects.filter(testcode = code)

            return render(request, 'testing/builder.html', {'test':test, 'questions':questions, 'answers':answers})
        else:
            return HttpResponseRedirect(reverse('testing:home'))

def add_ques(request, code):
    if request.user.is_authenticated is not True:
        return HttpResponseRedirect(reverse('testing:home'))
    else:
        test = AllTests.objects.get(testcode = code)
        q = ['1','2','3','4','5','6']
        return render(request, 'testing/add_ques.html', {'test':test , 'q':q})

def detele_test(request, code):
    test = AllTests.objects.get(testcode = code)
    test.delete()
    return HttpResponseRedirect(reverse('testing:profile'))

def delete_ques(request, code, ques_num):
    a = Tests.objects.get(testcode = code, ques_num = ques_num)
    a.delete()
    b = Tests.objects.filter(testcode = code)
    i=1;
    for ques in b:
        id = ques.id
        c = Tests.objects.filter(testcode = code, id = id ).update(ques_num = i)
        d = Answers.objects.filter(testcode = code, test_id = id)
        for ans in d:
            e = Answers.objects.filter(testcode = code, test_id = id).update(ques_num = i)
        i=i+1

    return HttpResponseRedirect(reverse('testing:builder', args = (code,)))


def edit_ques(request, code, ques_num):
    if request.user.is_authenticated is not True:
        return HttpResponseRedirect(reverse('testing:home'))
    else:
        test = AllTests.objects.get(testcode = code)
        q = [1,2,3,4,5,6]
        ques =  Tests.objects.get(testcode = code, ques_num = ques_num)
        ans = Answers.objects.filter(testcode = code, ques_num = ques_num)

        return render(request, 'testing/edit_ques.html', {'test':test , 'ques':ques, 'q':q, 'ans':ans, 'ques_num':ques_num})

def editing_ques(request, code, ques_num):
    if request.user.is_authenticated is not True:
        return HttpResponseRedirect(reverse('testing:home'))
    else:
        ans = ['1','2','3','4','5','6']
        i=0
        k=0
        for cout in ans:
            znach = 'checkans' + cout
            if znach in request.POST:
                k=k+1
            else:
                i=i+1

        if i == 6 or k == 6:

            return HttpResponseRedirect(reverse('testing:edit_ques', kwargs = {'code':code, "ques_num":ques_num}))
        else:
            Tests.objects.filter(testcode = code, ques_num = ques_num).update(ques = request.POST['ques'])
            cout = ['1','2','3','4','5','6']
            for i in range(1,7):
                znach = 'checkans' + cout[i-1]
                if znach in request.POST:
                    ans_value=request.POST[znach]
                else:
                    ans_value="off"
                Answers.objects.filter(testcode = code, ques_num = ques_num, ans_num = i).update(ans = request.POST['ans' + cout[i-1]], ans_value = ans_value)


            return HttpResponseRedirect(reverse('testing:builder', args = (code,)))

def adding_ques(request, code):
    if request.user.is_authenticated is not True:
        return HttpResponseRedirect(reverse('testing:home'))
    else:
        ans = ['1','2','3','4','5','6']
        i=0
        k=0
        for cout in ans:
            znach = 'checkans' + cout
            if znach in request.POST:
                k=k+1
            else:
                i=i+1

        if i == 6 or k == 6:
            return HttpResponseRedirect(reverse('testing:add_ques', args = (code,)))
        else:

            test = AllTests.objects.get(testcode = code)
            test_id = test.id
            q_ques =  Tests.objects.filter(testcode = code)
            i=1
            for q_q in q_ques:
                i=i+1

            if i>6:
                return HttpResponseRedirect(reverse('testing:builder', args = (code,)))

            a = Tests.objects.create(ques_num = i, testcode = code, ques = request.POST['ques'],test_id = test_id )
            a.refresh_from_db()
            ans = ['1','2','3','4','5','6']

            ques_test_id = Tests.objects.get(testcode = code, ques_num = i).id
            ans_num = 0
            for cout in ans:
                ans_num = ans_num + 1
                znach = 'checkans' + cout
                if znach in request.POST:
                    ans_value=request.POST[znach]
                else:
                    ans_value="off"

                b = Answers.objects.create(ques_num = i, testcode = code, ans = request.POST['ans'+ cout],test_id = ques_test_id,ans_value = ans_value,ans_num = ans_num )
                b.refresh_from_db()


            return HttpResponseRedirect(reverse('testing:builder', args = (code,)))


def testing(request, token):
    if request.user.is_authenticated is not True:
        return HttpResponseRedirect(reverse('testing:login'))
    else:
        i=31
        code=""
        while(i<37):
            code=code+token[i]
            i=i+1

        test = AllTests.objects.get(testcode = code)
        ques_complete = Tests_complete.objects.filter(token = token)
        i=1
        for q_ques in ques_complete:
            i=i+1


        ques = Tests.objects.filter(testcode = code)

        j=0
        for q_ques in ques:
            j=j+1

        if j==i-1:
            number_passed = AllTests.objects.get(testcode = code).number_passed + 1
            c = AllTests.objects.filter(testcode = code).update(number_passed = number_passed )
            d = Test_complete.objects.create(author = request.user, testcode=code, date = datetime.datetime.now(), token=token,test_id = test.id,testname = AllTests.objects.get(testcode = code).testname )
            return HttpResponseRedirect(reverse('testing:complete', args = (token,)))

        question = Tests.objects.get(testcode = code,  ques_num = i)

        answers = Answers.objects.filter(testcode = code, ques_num = i)
        q_true=0
        for q_ans in answers:
            if q_ans.ans_value == "on":
                q_true = q_true+1

        return render(request, 'testing/testing.html',{'code':code, 'test':test, 'question':question, 'answers':answers,'token':token,"q_true":q_true, 'j':j})



def random_string_generator(size=30, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))




def processing(request, token):
    if request.user.is_authenticated is not True:
        return HttpResponseRedirect(reverse('testing:home'))
    else:
        i=31
        code=""
        while(i<37):
            code=code+token[i]
            i=i+1

        test = AllTests.objects.get(testcode = code)
        test_id = test.id


        ques_complete = Tests_complete.objects.filter(token = token)
        i=1
        for q_ques in ques_complete:
            i=i+1

        answers = Answers.objects.filter(testcode = code, ques_num = i)

        for a in answers:

            if a.ans in request.POST:
                if a.ans_value == "on":
                    correct="true"
                else:
                    correct = "false"


                b = Answers_complete.objects.create(ques_num = i, ans = a.ans, testcode = code, token= token, test_id = test_id, correct = correct)
                b.refresh_from_db()
            else:
                continue

        a = Tests_complete.objects.create(ques_num = i, testcode = code, token = token, author = 'vlad',test_id = test_id )
        a.refresh_from_db()
        return HttpResponseRedirect(reverse('testing:testing', args = (token,)))



def complete(request, token):
    i=31
    code=""
    while(i<37):
        code=code+token[i]
        i=i+1

    answers = Answers.objects.filter(testcode = code)
    quess  = Tests.objects.filter(testcode = code)
    ans_complete = Answers_complete.objects.filter(token = token)
    ans_complete_correct = Answers_complete.objects.filter(token = token,correct = "true")
    ans_correct = Answers.objects.filter(testcode = code, ans_value = "on")
    q_ans_correct =0
    q_ans_complete_correct=0
    q_quess =0
    for a in ans_correct:
        q_ans_correct=q_ans_correct+1

    for a in ans_complete_correct:
        q_ans_complete_correct=q_ans_complete_correct+1

    for a in quess:
        q_quess = q_quess+1

    result = q_ans_complete_correct/q_ans_correct*100
    result = round(result,1)

    mark = round(q_ans_complete_correct * 12 / q_ans_correct)

    return render(request, 'testing/complete.html',{'q_ans_correct':q_ans_correct, 'q_ans_complete_correct':q_ans_complete_correct,
    'q_quess':q_quess, 'result':result, 'mark':mark, "quess":quess, "answers":answers, 'ans_complete':ans_complete})
