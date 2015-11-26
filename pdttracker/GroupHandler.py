from django.contrib.auth.models import User, Group

def in_group(user, group_name):
	# user = request.user
	group = Group.objects.get(name=group_name)
	user_group = user.groups.all()
	if user_group[0] == group:
		return True
	else:
		return False