from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .helper import LatexParser

lp = LatexParser()

# Create your views here.
@csrf_exempt
def text_input(request) -> render:
    return render(request, 'app/text_io.html')

@csrf_exempt
def text_output(request) -> JsonResponse:
    if request.method == 'POST':
        user_input = request.POST.get('user_input', '')
        response = lp.parse(user_input)
        return JsonResponse({'parsed': response, 'statusCode': 200})
    else:
        return JsonResponse({'error': 'Invalid HTTP method', 'statusCode': 400})