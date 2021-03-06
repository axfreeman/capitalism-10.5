from django.contrib.auth.models import User
from django import template
from economy.models.states import User, Project, TimeStamp
from ..global_constants import *
from django.contrib import messages

register = template.Library()

#! supplies list of stages for the dropdown menu
@register.inclusion_tag('partials/stages.html',takes_context=True)
def control_states(context):
      new_context={}
      try:
            user=context.request.user
      except Exception as error:
            logger.error(f"The user could not be found because {error}")
            raise Exception ("Giving Up")
      try:
            current_step=user.current_step
            current_stage=STEPS[current_step].stage_name
      except Exception as error: 
            logger.error(f"Corrupt initial state encountered due to {error}")
            messages.error(context['request'],f"Corrupt initial state encountered due to {error}")
            current_step=DEMAND
            current_stage=M_C
      new_context['active_stage']=current_stage
      new_context['stages']=STAGES
      context=new_context
      return context

@register.inclusion_tag('partials/current_step.html',takes_context=True)
def current_step(context):
      try:
            user=context.request.user
            step=user.current_step
      except Exception as error:
            logger.error(f"Could not find the current step because of {error}")
            step="unknown"
      context={}
      context['step']=step
      return context

@register.inclusion_tag('partials/project_list.html')
def project_list():
      project_list=Project.objects.all()
      context={}
      context['projects']= project_list
      return context

@register.inclusion_tag('partials/step_list.html', takes_context=True)
def step_list(context):
      try:
            user=context.request.user
            if user.is_superuser:
                  return {} #! Superuser can only administer. Template should not try to render this
            simulation=user.current_simulation
            current_time_stamp=simulation.current_time_stamp
            project_number=simulation.project_number
            logger.info(f"Calculating step list for user {user} with simulation {simulation} and time stamp {current_time_stamp} and project {project_number}")
            step_list=TimeStamp.objects.filter(simulation=simulation)
      except Exception as error:
            logger.error(f"Could not find the step list because of {error}")
            request = context['request']
            messages.error(request,f"There is a problem in the database: {error}")
            step_list=None
      context['states']= step_list
      return context
