from urllib.error import HTTPError
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.messages import get_messages
from django.conf import settings
from django.shortcuts import redirect
from ghapi.all import GhApi

ORIGINAL_REPO_URI = getattr(settings, "ORIGINAL_REPO_URI", None)
DEFAULT_STATE_LENGTH = getattr(settings, "DEFAULT_STATE_LENGTH", None)
GITHUB_APP_NAME = getattr(settings, "GITHUB_APP_NAME", None)

def createFork(user, newForkName):
    githubUser= user.social_auth.get(provider ='github')
    gExtraData = githubUser.extra_data
    # Access token used to interact with the API
    accessToken = gExtraData['access_token']
    owner, repoName = ORIGINAL_REPO_URI.split("/")
    # Two different objects because it is not possible to override the owner later to check if the repo was already forked
    originalRepoApi = GhApi(owner=owner, repo=repoName, token=accessToken)
    userApi = GhApi(owner=user.username, token=accessToken)
    # Only repos owned by the user
    userRepos = originalRepoApi.repos.list_for_authenticated_user(affiliation="owner")
    userForks = [repo for repo in userRepos if repo['fork']]
    # To check if the current user already has a copy of this repository
    for fork in userForks:
        repo = userApi.repos.get(repo=fork.name)
        if(repo['parent']['full_name'] == ORIGINAL_REPO_URI):
            raise Exception('You already have a fork of the original repo under your account. Delete it before creating a new one')
    originalRepoApi.repos.create_fork(name=newForkName)
    return "https://github.com/{}/{}".format(user.username, newForkName)
 

def login(request):
    if(request.user.is_authenticated):
        return redirect('home')
    else:
        storage = get_messages(request)
        # In case there are social-auth errors, they are sent to the user
        authErrorMessages = [message for message in storage if "social-auth" in message.tags.split()]
        return render(request, 'login.html', {"appName": GITHUB_APP_NAME, "authErrorMessages": authErrorMessages})

@login_required
def home(request):
    if(request.method == "POST" ):
        try:
            newForkName = request.POST['newForkName']
        except(KeyError):
            return render(request, 'home.html', {
                'error_message': "Please submit a valid fork name.",
            })
        else:
            try:
                newForkURL = createFork(request.user, newForkName)
            except (HTTPError, Exception) as error:
                if(isinstance(error, HTTPError)):
                    if(error.code == 403):
                        return render(request, 'home.html', {
                            'error_message': "You need to install the app and provide access to all your repos before using it. Log out and click on the Install button to proceed.",
                        })
                return render(request, 'home.html', {
                    'error_message': "An error occured while forking the new repo: {}".format(error),
                })
            else:
                return render(request, 'home.html', {
                    "newForkURL": newForkURL
                })
    elif(request.method == "GET"):
        return render(request, 'home.html')