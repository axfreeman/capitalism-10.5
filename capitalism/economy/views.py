from .forms import SimulationCreateForm, SimulationSelectForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms
from django.shortcuts import render
from economy.actions.initialize import initialize_projects
from economy.actions.initialize import initialize
from .models.states import Project, TimeStamp, User, Simulation_Parameter
from economy.models.report import Trace
from .models.commodity import Commodity
from .models.owners import Industry, SocialClass, StockOwner
from .models.stocks import IndustryStock, SocialStock, Stock
from django.http import HttpResponse
from django.template import loader
from django.views.generic import ListView,UpdateView, DeleteView, CreateView
from .global_constants import *
from .forms import SignUpForm
from django.contrib.auth import authenticate,login
from django.http.response import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages

def get_economy_view_context(request):#TODO change name - this function now not only creates the context but also displays it, so the naming is wrong
    current_time_stamp=request.user.current_time_stamp
    industry_stocks = IndustryStock.objects.filter(time_stamp_FK=current_time_stamp)
    industries=Industry.objects.filter(time_stamp_FK=current_time_stamp)
    productive_stocks=industry_stocks.filter(usage_type=PRODUCTION).order_by("commodity_FK__display_order")
    industry_headers=productive_stocks.filter(industry_FK=industries.first()).order_by("commodity_FK__display_order") #!all industries have same choice of productive stocks, even if usage is zero
    social_classes=SocialClass.objects.filter(time_stamp_FK=current_time_stamp)
    social_stocks=SocialStock.objects.filter(time_stamp_FK=current_time_stamp)
    commodities=Commodity.objects.filter(time_stamp_FK=current_time_stamp)

    context={}
    context["productive_stocks"]=productive_stocks
    context["industries"]=industries
    context["industry_headers"]=industry_headers
    context["social_classes"]=social_classes
    context["social_stocks"]=social_stocks
    context["commodities"]= commodities
    template = loader.get_template('economy.html')
    return HttpResponse(template.render(context, request))


def sandbox(request):
    table_query = Commodity.objects.all()
  
    template = loader.get_template('sandbox.html')
    context = {
        'table_query': table_query,
    }
    logger.error("Test!!")
    return HttpResponse(template.render(context, request))

class ProjectView(ListView):
    model=Project
    template_name='project_list.html'

class TimeStampView(ListView):
    model=TimeStamp
    template_name='timestamp_list.html'    
 
class EconomyView(ListView):
    model=IndustryStock
    template_name='economy.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) #! Necessary?
        context = get_economy_view_context(context)
        return context

class IndustryView(ListView):
    model=Industry
    template_name='industry_list.html'    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs=Industry.objects.filter(time_stamp_FK=self.request.user.current_time_stamp)
        context['industry_list']=qs
        return context    

class CommodityView(ListView):
    model=Commodity
    template_name='commodity_list.html'    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs=Commodity.objects.filter(time_stamp_FK=self.request.user.current_time_stamp)
        context['commodity_list']=qs
        return context    

class SocialClassView(ListView):
    template_name='socialclass_list.html'
    model=SocialClass
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs=SocialClass.objects.filter(time_stamp_FK=self.request.user.current_time_stamp)
        context['social_class_list']=qs
        return context

class AllOwnersView(ListView):
    model=StockOwner
    template_name='stockowner_list.html'    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stock_list=StockOwner.objects.order_by("time_stamp_FK.simulation_FK.project_number","time_stamp_FK.time_stamp")
        context['stock_list']= stock_list
        return context


class SocialStockView(ListView):
    model=SocialStock
    template_name='socialstock_list.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stock_list=SocialStock.objects.filter(time_stamp_FK=self.request.user.current_time_stamp)
        context['stock_list']= stock_list
        return context    

class IndustryStockView(ListView):
    model=IndustryStock
    template_name='industrystock_list.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stock_list=IndustryStock.objects.filter(time_stamp_FK=self.request.user.current_time_stamp)
        context['stock_list']= stock_list
        return context
        
class AllStocksView(ListView):
    model=Stock
    template_name='stock_list.html'

class TraceView(ListView):
    model=Trace
    template_name='trace_list.html'    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs=Trace.objects.filter(user=self.request.user).order_by('real_time')
        context['trace_list']=qs
        return context    

def landingPage(request):
    user=request.user
    logger.info(f"User {user} has landed on the home page")
    return render(request, 'landing.html')

def status_update(request):
    user=request.user
    logger.info(f"User {user} requested a status update")
    return render(request, 'status.html')

#! to display messages to people that just logged in
def newlyLanded(request):
    user=request.user
    logger.info(f"User {user} has landed on the new landing page")
    messages.info(request,"Hi, welcome to capitalism")
    messages.info(request, "To view the current state of the project, visit the Status Update Page")
    return render(request, 'landing.html')


#! See the [CSEStack](https://www.csestack.org/django-sign-up-registration-form/) solution
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  #! TODO Not sure if this is needed but seems to be recommended
            user.save()
            raw_password = form.cleaned_data.get('password1')
            # login user after signing up
            user = authenticate(username=user.username, password=raw_password)
            #! Create a standard parameter record for the new user. This will be the default
            simulation=Simulation_Parameter(user=user) #! Default everything else
            simulation.save()
            #! User must have a current time stamp even though the data is not initialized
            #! Because the relation is one to one.
            #! TODO a bit of a design flaw here...
            new_time_stamp=TimeStamp(simulation_FK=simulation, time_stamp=0, step="Initial", stage="Initial", user=user)
            new_time_stamp.save()
            new_time_stamp.comparator_time_stamp_FK=new_time_stamp
            new_time_stamp.save()
            user.current_time_stamp=new_time_stamp
            user.save()
            login(request, user)
            # Initialise the user's database
            initialize(request)           
            return HttpResponseRedirect(reverse("economy"))
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def initialize_and_redisplay(request):
    initialize(request)
    return HttpResponseRedirect(reverse("economy"))    

def disclaimers(request):
    return render(request, 'disclaimers.html')

def rebuild_project_table(request):
    initialize_projects(request)
    return render(request, 'dashboard.html')

class AdminDashboard(ListView):
    model=User
    template_name='admin-dashboard.html'    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs=User.objects.all()
        context={}
        context['users']=qs
        return context    

def userDashboard(request):
    return render(request,'user-dashboard.html')

class UserDetail(DeleteView):
    template_name='user_form.html'    
    model=User
    fields=["username"]
    success_url='admin-dashboard'

class SimulationCreateView(LoginRequiredMixin, CreateView):
    form_class=SimulationCreateForm
    queryset=Simulation_Parameter.objects.all()
    template_name='simulation_create.html'
    success_url=reverse_lazy('user-dashboard')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def form_valid(self, form):
        logger.info(f"Valid new simulation form submitted by user {self.request.user}")
        simulation_name=form.cleaned_data['name']
        user_project_choice=form.cleaned_data['project']
        logger.info(f"Trying to create a simulation called {simulation_name}")
        chosen_project_number=user_project_choice.number
        logger.info(f"Project number is {chosen_project_number}")
        simulation=form.save(commit=False)
        simulation.user=self.request.user
        simulation.project_number=chosen_project_number
        simulation.save()
        result=simulation.startup()
        if result!="success":
            messages.error(self.request,f"Could not create this simulation because {result}")
        else:
            simulation.save()
        return super(SimulationCreateView, self).form_valid(form)
 
    def form_invalid(self, form):
        logger.info(f"Invalid new simulation form submitted by user {self.request.user}")
        logger.info(f"The non-field errors were {form.non_field_errors}")
        return self.render_to_response( 
            self.get_context_data(form=form))


class SimulationSelectView(LoginRequiredMixin, CreateView):
    form_class=SimulationSelectForm
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def form_valid(self, form):
        logger.info(f"Valid change simulation form submitted by user {self.request.user}")
        simulation_choice=form.cleaned_data['simulations']
        logger.info(f"Trying to switch to the simulation called {simulation_choice}")
        user=self.request.user
        time_stamp=TimeStamp.objects.filter(simulation_FK=simulation_choice).last()
        #! TODO we have to make sure we really have got the latest time stamp
        #! which probably means it should be a field of the simulation_parameter object
        logger.info(f"The time stamp for this simulation is {time_stamp}")
        user.current_time_stamp=time_stamp
        user.save()
        return super(SimulationSelectView, self).form_valid(form)

    def form_invalid(self, form):
        logger.info(f"Invalid simulation select form submitted by user {self.request.user}")
        logger.info(f"The non-field errors were {form.non_field_errors}")
        return self.render_to_response( 
            self.get_context_data(form=form))

    queryset=Simulation_Parameter.objects.all()
    template_name='simulation_select.html'
    success_url=reverse_lazy('user-dashboard')

