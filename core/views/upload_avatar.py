from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


@login_required
def update_avatar(request):
    if request.method == 'POST' and request.FILES.get('avatar'):
        try:
            profile = request.user.profile
            profile.avatar = request.FILES['avatar']
            profile.save()
            return JsonResponse({
                'success': True,
                'avatar_url': profile.avatar.url
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)  # Captura o erro real
            }, status=400)
    return JsonResponse({
        'success': False,
        'error': 'Requisição inválida'
    }, status=400)
