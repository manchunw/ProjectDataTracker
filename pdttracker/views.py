from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.template import RequestContext
from django.contrib.auth.models import User, Group
from pdttracker.models import *
from pdttracker.tables import *
from django_tables2 import RequestConfig
from .ReportHandler import get_yield, get_report
from .forms import *
import datetime
from django.core.urlresolvers import reverse
from pdttracker.projecthandler import *
from pdttracker.ActionLogHandler import add_action_log
from django.views.generic import View
from pdttracker.GroupHandler import *
from django.utils.decorators import method_decorator
from pdttracker.phasehandler import *
from pdttracker.ReportHandler import *
from pdttracker.iterationhandler import *
from django.db.models import F

def home(request):
    s = "Hello World!"
    return HttpResponse(s)

@csrf_protect
def auth_login(request):

    if request.method == 'POST':
        form = LoginForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    add_action_log(request, 'login')
                    next_page = request.GET.get("next")
                    if next_page:
                    	return HttpResponseRedirect(next_page)
                    else:
                        if in_group(user, "Administrator"):
                            return redirect(reverse(welcomeAdmin))
                        if in_group(user, "Manager"):
                            return redirect(reverse(project_view))
                        if in_group(user, "HR"):
                            return redirect(reverse(welcomeHR))
                        if in_group(user, "Developer"):
                            return redirect(reverse(project_view))
                else:
                    return HttpResponse("Your PDT account is disabled.")
            else:
                return render_to_response("login.html", {"title": "Login", "error_message": "Invalid username and/or password.", "form": form}, RequestContext(request))
        else:
            return render_to_response("login.html", {"title": "Login", "error_message": "Server transmission error. Try again.", "form": form}, RequestContext(request))
    else:
        form = LoginForm()

        return render(request, 'login.html', {"title": "Login", "form": form})

@login_required
def auth_logout(request):
    add_action_log(request, 'logout')
    logout(request)
    return HttpResponseRedirect("/login/")

@login_required
def table_view(request, table_name):
	tname = str(table_name)
	if tname == 'defect':
		return defect_view(request)
	elif tname == 'project':
		return project_view(request)
	elif tname == 'iteration':
		return iteration_view(request)
	elif tname == 'phase':
		return phase_view(request)
	elif tname == 'action_log':
		return action_log_view(request)
	elif tname == 'user':
		return user_view(request)
	elif tname == 'userinfo':
		return user_info_view(request)
	else:
		return currentTime(request)

@login_required
def currentTime(request):
    s = datetime.datetime.now()
    return render(request, 'view_time.html', {"time": str(s)})

@login_required
def selectMode(request, pk):
    project = Project.objects.get(pk=pk)
    add_action_log(request, 'enterproj', project)
    return render(request, 'selectMode.html', {"project": project})

@login_required
def developmentMode(request, pk):
    project = Project.objects.get(pk=pk)
    add_action_log(request, 'devmode', project)
    return render(request, 'developmentMode.html', {"project": project})

@login_required
def welcomeHR(request):
    ManagerList = Group.objects.get(name="Manager").user_set.all()
    DeveloperList = Group.objects.get(name="Developer").user_set.all()
    context={'ManagerList':ManagerList, 
              'DeveloperList':DeveloperList  }
    return render(request, 'welcomeHR.html', context)

@login_required
def welcomeAdmin(request):
    return render(request, 'welcomeAdmin.html', {})

@login_required
def project_view(request):
    if in_group(request.user, "Manager") or in_group(request.user, "Administrator"):
        table = ManagerProjectTable(get_project_list(request))
    else:
        table = DeveloperProjectTable(get_project_list(request))

#    table = ProjectTable(Project.objects.filter(in_charge_by=request.user))
    RequestConfig(request, paginate={"per_page": 10}).configure(table)
    return render(request, "view_project.html", {"project": table, "user": request.user})

@login_required
def modifyProject(request, pk):
    project = Project.objects.get(pk=pk)
    if project.current_iteration == None:
        ph = Phase.objects.get(phase_sequence = 1, in_project =project)
        project.update(current_phase = ph)
    iteration = Iteration.objects.get(pk=project.current_iteration.pk)
    phase = Phase.objects.get(pk=project.current_phase.pk)
#     table = ProjectTable(get_project_list(request))
# #    table = ProjectTable(Project.objects.filter(in_charge_by=request.user))
#     RequestConfig(request).configure(table)
    # last_phase = is_last_phase(project)
    pj = Project.objects.select_related("current_phase").get(pk = project.pk)
    last_phase = pj.current_phase.phase_sequence == pj.num_phase
    pj = Project.objects.select_related("current_iteration").get(pk = project.pk)
    last_iteration = pj.current_iteration.iteration_sequence == pj.num_iteration
    print(str(last_phase))
    print(str(last_iteration))
    return render(request, "modifyProject.html", {"project_name": project.project_title, "project_SLOC": project.project_sloc, "current_phase": phase.phase_name, "current_iteration": iteration.iteration_name, "num_phase": project.num_phase, "num_iteration": project.num_iteration, "project_id": project.id, "is_last_phase": last_phase, "is_last_iteration": last_iteration, "is_active": project.is_active})

@login_required
def iteration_view(request):
    table = IterationTable(Iteration.objects.all())
    RequestConfig(request, paginate={"per_page": 10}).configure(table)
    return render(request, "view_iteration.html", {"iteration": table})

@login_required
def phase_view(request):
    table = PhaseTable(Phase.objects.all())
    RequestConfig(request, paginate={"per_page": 10}).configure(table)
    return render(request, "view_phase.html", {"phase": table})

@login_required
def action_log_view(request):
    table = ActionLogTable(ActionLog.objects.all().order_by('-created_at'))
    RequestConfig(request, paginate={"per_page": 10}).configure(table)
    return render(request, "view_action_log.html", {"action_log": table})

@login_required
def user_view(request):
    table = UserTable(User.objects.all())
    RequestConfig(request, paginate={"per_page": 10}).configure(table)
    return render(request, "view_user.html", {"user": table})

@login_required
def user_info_view(request):
    table = UserInfoTable(Group.objects.all())
    RequestConfig(request, paginate={"per_page": 10}).configure(table)
    return render(request, "view_user_info.html", {"permission": table})

@login_required
def defect_view(request, pk):
    project = Project.objects.get(pk=pk)
    add_action_log(request, 'mgmtmode', project)
    table = DefectTable(Defect.objects.filter(recorded_in=project))
    RequestConfig(request, paginate={"per_page": 10}).configure(table)
    return render(request, "view_defect.html", {"defect": table, "project": project})

@login_required
def project_detail(request, pk):
    project = Project.objects.get(pk=pk)
    context={'project':project}
    template="project_detail.html"
    return render(request, template, context)

@login_required
def iteration_detail(request, pk):
    iteration = Iteration.objects.get(pk=pk)
    context={'iteration':iteration}
    template="iteration_detail.html"
    return render(request, template, context)

@login_required
def defect_detail(request, pk):
    defect = Defect.objects.get(pk=pk)
    context={'defect':defect}
    template="defect_detail.html"
    return render(request, template, context)

@login_required
def addProject(request):
    form = ProjectForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        #form.save()
        #print request.POST['email'] #not recommended
        instance = form.save(commit=False)
        #assign_member = form.cleaned_data.get('assign_member')
        data =form.cleaned_data['assign_developer']
#        in_charge_by = request.user
#        bar = Report.objects.create(report_title="on99")
#        instance.project_report=bar
#        instance.save()

        add_project(request, instance.project_title ,  instance.project_description,instance.project_sloc,instance.current_phase,instance.current_iteration, data, form.cleaned_data['phase_names'], form.cleaned_data['iteration_names'])

        return redirect(reverse(project_view))


    return render(request, "project_form.html", context)



@login_required
def removeProject(request, id):
    p = Project.objects.get(id=id)
    p.delete()

    return render(request, "view_project.html", context)

@login_required
def addIteration(request):
    title = 'Add Iteration Now'
    form = IterationForm(request.POST or None)
    context = {
        "title": title,
        "form": form
    }
    if form.is_valid():
        #form.save()
        #print request.POST['email'] #not recommended
        instance = form.save(commit=False)
        instance.save()
        context = {
            "title": "Thank you"
        }

    
    return render(request, "iteration_form.html", context)

@login_required
def editIteration(request, pk):
    instance = Iteration.objects.get(pk=pk)
    form = IterationForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect(reverse(iteration_view))
    return render(request, 'editIteration.html', {'form': form})

@login_required
def removeIteration(request, id):
    p = Project.objects.get(id=id)
    p.delete()

    return render(request, "view_iteration.html", context)

class addDefect(View):
    @method_decorator(login_required)
    def get(self, request, pk):
        project = Project.objects.get(pk=pk)
        projectmember = ProjectMember.objects.get(member=request.user, work_in=project)
        add_action_log(request, 'defectmode', project)
        title = 'Add Defect Now'
        form = DefectForm()
        context = {
            "title": title,
            "form": form,
            "project": project,
            "projectmember": projectmember,
        }

        return render(request, "defect_form.html", context)
    @method_decorator(login_required)
    def post(self, request, pk):
        pj = Project.objects.get(pk=pk)
        projectmember = ProjectMember.objects.get(member=request.user, work_in=pj)
        form = DefectForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            Defect.objects.filter(pk=instance.pk).update(
                recorded_in=pj,
                iteration_resolved=pj.current_iteration,
                defect_created_by=request.user
            )
            defect =  Defect.objects.get(pk=instance.pk)
            project = Project.objects.get(pk=pk)
            add_action_log(request, 'adddefect', project, None, None, defect)
            
        return HttpResponseRedirect("/view_defect/" + str(pk) + "/")


class editDefect(View):
    @method_decorator(login_required)
    def get(self, request, pk):
        instance = Defect.objects.get(pk=pk)
        project = Project.objects.get(pk=instance.recorded_in.pk)
        form = DefectForm(request.POST or None, instance=instance)

        return render(request, 'editDefect.html', {'form': form, 'project': project})
    @method_decorator(login_required)
    def post(self, request, pk):
        instance = Defect.objects.get(pk=pk)
        form = DefectForm(request.POST or None, instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            project = Project.objects.get(pk=instance.recorded_in.pk)
            add_action_log(request, 'moddefect', project, None, None, instance)
            
        return HttpResponseRedirect("/view_defect/" + str(project.pk) + "/")
    

def report_view(request, reporttype, pk):
    reporttypestr = str(reporttype)
    if reporttypestr == 'project':
        # project report
        pj = Project.objects.get(pk=pk)
#        rt = get_report(reporttype, pj)
        (table, yield_arr) = get_yield(pj)
        return render(request, "project_report.html", {
            'table': table,
            'yield_arr': yield_arr,
            'report_title': pj.project_report.report_title
        })
    elif reporttypestr == 'phase':
        # phase report
        ph = Phase.objects.get(pk=pk)
        rt = get_report(reporttype, ph)
        return render(request, "phase_report.html", {'report': rt})
    elif reporttypestr == 'iteration':
        # iteration report
        it = Iteration.objects.get(pk=pk)
        rt = get_report(reporttype, ph)
        return render(request, "iteration_report.html", {'report': rt})
class create_user(View):
    form = UserForm
    initial = {'key': 'value'}
    template_name = 'create_user.html'
    def get(self, request, *args, **kwargs):
        form = self.form()
        return render(request, self.template_name, {'form': form})
    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name=form.cleaned_data.get("groups")[0])
            user.groups.add(group)
            print(form.cleaned_data)
            # if in_group(request.user, "Administrator"):
            return HttpResponseRedirect('/staff_view/')
            # else:
            #     return HttpResponseRedirect('/welcomeHR/') 
        return render(request, self.template_name, {'form': form})

class edit_user(View):
    @method_decorator(login_required)
    def get(self, request, pk):
        user= User.objects.get(pk=pk)
        form=UserForm(instance=user)
        context={'form':form}
        template = 'edit_user.html'
        return render(request, template, context)
    @method_decorator(login_required)
    def post(self, request, pk):
        user= User.objects.get(pk=pk)
        form=UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect(reverse(project_view))
        context={'form':form}
        template = 'edit_user.html'
        return render(request, template, context)

@login_required
def staff_view(request):
    ManagerList = Group.objects.get(name="Manager").user_set.all()
    HRList = Group.objects.get(name="HR").user_set.all()
    DeveloperList = Group.objects.get(name="Developer").user_set.all()
    context={'ManagerList':ManagerList, 
              'HRList':HRList,
              'DeveloperList':DeveloperList  }
    return render(request, 'staff_view.html', context)

@login_required
def switch_project(request, pk):
    project = Project.objects.get(pk=pk)
    add_action_log(request, 'exitproj', project)
    return HttpResponseRedirect('/project/')

@login_required
def api_call(request, command, pk):
    project = Project.objects.get(pk=pk)
    success_page = HttpResponse("OK", content_type = "text/plain", status = 200)
    if command == 'pause_timer':
        add_action_log(request, 'pausework', project)
        return success_page
    elif command == 'resume_timer':
        add_action_log(request, 'resumework', project)
        return success_page
    elif command == 'switchPhase':
        sloc = request.POST.get("sloc", 0)
        #endIteration
        # update sloc of iteration and phase
        Iteration.objects.filter(pk=project.current_iteration.pk).update(iteration_sloc=sloc)
        Phase.objects.filter(pk=project.current_phase.pk).update(phase_sloc= F('phase_sloc') + sloc)
        # update delivered sloc
        iteration = Iteration.objects.get(pk=project.current_iteration.pk)
        add_to_delivered_sloc(iteration, sloc)
        # log close iteration
        add_action_log(request, 'clsitn', project, project.current_phase, project.current_iteration)
        add_action_log(request, 'clsphe', project, project.current_phase)
        #check is last phase
        newphase=Phase.objects.get(in_project=project, phase_sequence=project.current_phase.phase_sequence+1)
        newiteration = Iteration.objects.get(iteration_sequence=1, in_phase=newphase)
        Project.objects.filter(pk=project.pk).update(current_phase=newphase, current_iteration=newiteration)
        return HttpResponseRedirect('/modifyProject/' + pk + '/')
    elif command =='switchIteration':
        sloc = request.POST.get("sloc", 0)
        #endIteration
        # update sloc of iteration and phase
        iteration = Iteration.objects.get(pk=project.current_iteration.pk)
        phase = Phase.objects.get(pk=project.current_phase.pk)
        Iteration.objects.filter(pk=iteration.pk).update(iteration_sloc=sloc)
        Phase.objects.filter(pk=phase.pk).update(phase_sloc= F('phase_sloc') + sloc)
        # update delivered sloc
        add_to_delivered_sloc(iteration, sloc)
        add_action_log(request, 'clsitn', project, project.current_phase, project.current_iteration)
        # update delivered sloc
        newIteration = Iteration.objects.get(in_phase = phase, iteration_sequence = iteration.iteration_sequence + 1)
        Project.objects.filter(pk=project.pk).update(current_iteration = newIteration)
        return HttpResponseRedirect('/modifyProject/' + pk + '/')
    elif command == 'closeProject':
        sloc = request.POST.get("sloc", 0)
        #endIteration
        # update sloc of iteration and phase
        Iteration.objects.filter(pk=project.current_iteration.pk).update(iteration_sloc=sloc)
        Phase.objects.filter(pk=project.current_phase.pk).update(phase_sloc= F('phase_sloc') + sloc)
        # update delivered sloc
        iteration = Iteration.objects.get(pk=project.current_iteration.pk)
        add_to_delivered_sloc(iteration, sloc)
        add_action_log(request, 'clsitn', project, project.current_phase, project.current_iteration)
        add_action_log(request, 'clsphe', project, project.current_phase)
        add_action_log(request, 'clsproj', project)
        Project.objects.filter(pk=pk).update(is_active=False)
        return HttpResponseRedirect('/modifyProject/' + pk + '/')
    elif command == 'abortProject':
        #endIteration
        # update sloc of iteration and phase
        project.current_iteration.update(iteration_sloc=sloc)
        project.current_phase.update(phase_sloc= F('phase_sloc') + sloc)
        # update delivered sloc
        iteration = Iteration.objects.get(pk=project.current_iteration.pk)
        add_to_delivered_sloc(iteration, sloc)
        add_action_log('clsitn', project, project.current_phase, project.current_iteration)
        add_action_log('clsphe', project, project.current_phase)
        add_action_log('clsproj', project)
        project.update(is_active=False)
        return HttpResponseRedirect('/modifyProject/' + pk + '/')
    else:
        return None

class editProject(View):
    @method_decorator(login_required)
    def get(self, request, pk):
        instance = Project.objects.get(pk=pk)
        form = ProjectForm( instance=instance)
        context={'form':form}
        template = 'editProject.html'
        return render(request, template, context)
    @method_decorator(login_required)
    def post(self, request, pk):
        instance = Project.objects.get(pk=pk)
        form=ProjectForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            # return redirect(reverse(project_view))
            return HttpResponseRedirect('/project/')
        context={'form':form}
        template = 'editProject.html'
        return render(request, template, context)

# @login_required
# def editProject(request, pk):
#     instance = Project.objects.get(pk=pk)
#     form = ProjectForm(request.POST or None, instance=instance)
#     if form.is_valid():
#         form.save()
#         return redirect(reverse(project_view))
#     return render(request, 'editProject.html', {'form': form})

