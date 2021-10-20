from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
import sys
sys.path.append("../../landon-website")
import globals

def index(request):
	return render(request, "forum/index.html")
def topics(request):
	topics = Topic.objects.order_by("date_added")
	context = {
		"topics": topics
	}
	return render(request, "forum/topics.html", context)
def topic(request, topic_id):
	topic = Topic.objects.get(id=topic_id)
	print(topic.view)
	topic.view["count"] += 1
	topic.save()
	owner = topic.owner
	entries = topic.entry_set.order_by("-date_added")
	for entry in entries:
		if request.user == entry.owner:
			entry.userIsOwner = True
		else:
			entry.userIsOwner = False
	context = {
		"topic": topic,
		"entries": entries,
		"owner": owner,
		"view": topic.view
	}
	return render(request, "forum/topic.html", context)
@login_required
def new_topic(request):
	currUser = request.user
	if request.method != "POST":
		form = TopicForm()
	else:
		form = TopicForm(data=request.POST)
		print(request.POST["text"])
		if form.is_valid():
			newTopic = form.save(commit = False)
			newTopic.owner = currUser
			form.save()
			topicName = request.POST["text"]
			topicObj = Topic.objects.get(text = topicName)
			groups = Group.objects.all()
			group = groups.get(text="Topic Starter")
			request.user.groups.add(group)
			request.user.save()
			return redirect("forum:topic", topic_id = topicObj.id)
	context = {
		"form": form
	}
	return render(request, "forum/new_topic.html", context)
@login_required
def new_entry(request, topic_id):
	currUser = request.user
	topic = Topic.objects.get(id=topic_id)
	if request.method != "POST":
		form = EntryForm()
	else:
		form = EntryForm(data=request.POST)
		if form.is_valid():
			newEntry = form.save(commit = False)
			newEntry.topic = topic
			newEntry.owner = currUser
			newEntry.save()
			return redirect("forum:topic", topic_id = topic_id)
	context = {
		"topic": topic,
		"form": form
	}
	return render(request, "forum/new_entry.html", context)
def edit_entry(request, entry_id):
	entry = Entry.objects.get(id = entry_id)
	topic = entry.topic
	if request.method != "POST":
		form = EntryForm(instance = entry)
	else:
		form = EntryForm(instance = entry, data = request.POST)
		if form.is_valid():
			form.save()
			return redirect("forum:topic", topic_id=topic.id)
	context = {
		"entry": entry,
		"topic": topic,
		"form": form
	}
	return render(request, "forum/edit_entry.html", context)
def user(request, user_id):
	userBadges = []
	if request.user.groups.filter(name="Admin").exists():
		userBadges.append({
			"name": "Admin",
			"description": "Admin for this site."
		})
	if request.user.groups.filter(name="Developer").exists():
		userBadges.append({
			"name": "Developer",
			"description": "Developer for this site."
		})
	if request.user.groups.filter(name="Topic Starter").exists():
		userBadges.append({
			"name": "Topic Starter",
			"description": "Create a new topic."
		})
	context = {
		"userBadges": userBadges,
		"maxUserBadges": globals.maxUserBadges,
		"userBadgesCount": len(userBadges),
		"userBadgesPercent": int((len(userBadges) / globals.maxUserBadges) * 100),
		"userBadgesPercentNotDone": 100 - int((len(userBadges) / globals.maxUserBadges) * 100)
	}
	return render(request, "forum/user.html", context)
