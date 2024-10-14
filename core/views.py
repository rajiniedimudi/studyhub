from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
import smtplib
from email.mime.text import MIMEText
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, views
from django.contrib.auth.models import User
from django.utils import timezone
from django.views import View
from django.views.generic import TemplateView
from .models import Profile
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
import json
import requests
from django.conf import settings


class HomeView(TemplateView):
    template_name = 'home.html'


class Userform(View):
    template_name = "user-form.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    def post(self, request, *args, **kwargs):
        print(request.POST, 'req')
        username = request.POST.get('name')
        email = request.POST.get('email')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        are = request.POST.get('are-you')
        sleep_hours = request.POST.get('sleep-hours')
        sleep_quality = request.POST.get('sleep-quality')
        exercise_frequency = request.POST.get('exercise-frequency')
        exercise_duration = request.POST.get('exercise-duration')
        diet_type = request.POST.get('diet-type')
        diet_type_other = request.POST.get('diet-type-other')
        work_schedule = request.POST.get('work-schedule')
        work_load = request.POST.get('workload')
        social_support = request.POST.get('social-support')
        coping_mechanisms = request.POST.getlist('coping-mechanisms')
        other_coping_mechanisms = request.POST.get('other-coping-mechanisms-text')
        stress_level = request.POST.get('stress-level')
        emotional_state = request.POST.get('emotional-state')
        other_emotional_state = request.POST.get('other-emotional-state-text')
        
        query = f'''Give tips with 5 points by analyzing my stress level. Please provide the following tips in a continuous format,
                without breaks between the topic headings and their content. Am a {are} and {gender}. I sleep {sleep_hours} and sleep quality is {sleep_quality}.
                I excerice {exercise_duration} in {exercise_frequency}. My diet is {diet_type} - {diet_type_other}.
                I work {work_schedule} with {work_load}. My social support network is {social_support}. 
                My coping mechanisms or stress management techniques is {coping_mechanisms}, any other coping mechanisms is {other_coping_mechanisms}.
                My stress level is {stress_level} and emotional state is {emotional_state}, , any other emotional state is {other_emotional_state}.'''

        result = {"result": chatgpt(query)}
        print(result,'result')

        return JsonResponse(result)

        
class SignupView(View):
    template_name = 'signup.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    def post(self, request, *args, **kwargs):
        name = self.request.POST.get('name')
        user_type = self.request.POST.get('user_type')
        email = self.request.POST.get('email')
        password = self.request.POST.get('password')
        
        try:
            # saving student user
            user = User.objects.create(first_name=name, username=email, email=email)
            user.set_password(password)
            user.save()
            student = Profile.objects.create(user=user,user_type=user_type)
            student.save()

            # authenticate student user
            auth_user = authenticate(request, username=email, password=password)
            if auth_user:
                login(request, auth_user)
                return redirect('home')
        except:
            messages.info(self.request, 'User already exists ')
            logout(self.request)
            return redirect('home')
           

class SigninView(View):
    template_name = 'signin.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    def post(self, request, *args, **kwargs):
        email = self.request.POST.get('email')
        password = self.request.POST.get('password')
        user = User.objects.filter(username=email)
        if user.exists():
            if Profile.objects.filter(user=user.last()).exists():
                auth_user = authenticate(username=email, password=password)
                if auth_user:
                    login(self.request, auth_user)
                    messages.info(request, "User Logged In ")
                    return redirect('home')
                else:
                    logout(self.request)
                    messages.info(request, "User and Password not matched !!")
            else:
                messages.info(request, "User is a Teacher !!")
        else:
            messages.info(request, "User not Exists !!")

        return HttpResponseRedirect(self.request.path_info)
    

class ProfileUpdateView(LoginRequiredMixin, View):
    template_name = 'user_profile.html'
    login_url = '/sign_in/'

    def get(self, request, *args, **kwargs):
        user_id = self.kwargs['pk']
        user = User.objects.filter(id=user_id)
        match_user = str(user.last().username) == str(self.request.user)
        if match_user:
            context = {'user': user.last(), 'first_name': user.last().first_name}
            if user.exists():
                user_type = Profile.objects.get(user=user.last()).user_type
                context.update({'user_type': user_type})  
            return render(request, self.template_name, context=context)
        else:
            return redirect('home')
        

    def post(self, request, *args, **kwargs):
        post_data = self.request.POST
        user_id = post_data.get('user')
        name = post_data.get('name')
        password = post_data.get('password')
        user = User.objects.filter(username=user_id)
        get_user = user.last()
        auth_user_pwd = authenticate(username=user_id, password=password)
        if user.exists() and auth_user_pwd:
            get_user.first_name = name
            get_user.save()
            messages.success(request, "PROFILE UPDATED")
        else:
            messages.warning(request, "USER NOT MATCHED !!")

        return HttpResponseRedirect(self.request.path_info)
    

class MyPasswordResetView(View):
    template_name = "reset_password.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        post_data = self.request.POST
        associated_users = User.objects.filter(username=post_data['email'])
        current_site = get_current_site(self.request)
        if associated_users.exists():
            user = associated_users.last()
            subject = "Password Reset Requested"
            email_template_name = "reset_password_email.txt"
            c = {
                "email": user.email,
                'domain': current_site.domain,
                'site_name': 'Study HUB',
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "user": user,
                'token': default_token_generator.make_token(user),
                'protocol': 'http',
            }
            email = render_to_string(email_template_name, c)
            try:
                mail_info = MIMEText(email)
                mail_info['Subject'] = subject
                mail_info['From'] = settings.DEFAULT_FROM_EMAIL
                mail_info['To'] = user.email
                smtp_server = settings.EMAIL_HOST
                smtp_port = settings.EMAIL_PORT
                with smtplib.SMTP(smtp_server, smtp_port) as server:
                    server.starttls()
                    server.login(settings.DEFAULT_FROM_EMAIL, settings.EMAIL_HOST_PASSWORD)
                    server.send_message(mail_info)
                messages.info(self.request, f'Reset Password Mail Sent to {user.username}')
                return redirect('home')
            except Exception as e:
                print(e, 'error')
                return HttpResponse('Invalid header found.')
        else: 
            messages.info(self.request, 'User not exists !!')

        return HttpResponseRedirect(self.request.path_info)


class PasswordResetConfirmView(View):
    template_name='password_reset_form.html'

    def get(self, request, *args, **kwargs):
        return render(self.request, self.template_name)
    
    def post(self, request, *args, **kwargs):
        post_data = self.request.POST
        if 'new_password' in post_data and 'confirm_password' in post_data:
            password_new = post_data.get('new_password')
            password_confirm = post_data.get('confirm_password')
            if password_new == password_confirm:
                try:
                    # Decode UID to get the user ID
                    uid = urlsafe_base64_decode(kwargs['uidb64']).decode()
                    # Retrieve user by user ID
                    user = User.objects.get(pk=uid)
                except:
                    user = None
                if user:
                    user.set_password(password_confirm)
                    user.save()
                    messages.info(self.request, 'Sucessfully password saved')
                    return redirect('home') 
            else:
                    messages.info(self.request, 'Password not matched !!') 
                    
        else:
            messages.info(self.request, 'Please enter new and confirm password !!') 

        return HttpResponseRedirect(self.request.path_info) 
    

class ChangePasswordView(View):
    template_name='change_password.html'

    def get(self, request, *args, **kwargs):
        user_id = self.request.user
        user = get_object_or_404(User, username=user_id)
        context = {'user': user}
        return render(self.request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        post_data = self.request.POST
        if 'new_password' in post_data and 'confirm_password' in post_data:
            password_new = post_data.get('new_password')
            password_confirm = post_data.get('confirm_password')
            if password_new == password_confirm:
                try:
                    # Retrieve user by user ID
                    user = User.objects.get(pk=kwargs['id'])
                except:
                    user = None
                if user:
                    user.set_password(password_confirm)
                    user.save()
                    messages.info(self.request, 'Sucessfully password saved')
                    return redirect('home') 
            else:
                    messages.info(self.request, 'Password not matched !!') 
                    
        else:
            messages.info(self.request, 'Please enter new and confirm password !!') 

        return HttpResponseRedirect(self.request.path_info)
    

def chatgpt(topic):
    api_key = settings.API_KEY  # GPT 3
    # Send prompt GPT 3
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a good helpfull assistant to explain."},
            {"role": "user", "content": str(topic)}
            ]
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    response_json = response.json()
    print(response_json)
    try:
        response_content = response_json['choices'][0]['message']['content']
        # print(response_content, 'response_content')
    except Exception as e:
        print('Exception ERROR ====> ', e)
        response_content = "Something went wrong!"
        
    return response_content
        