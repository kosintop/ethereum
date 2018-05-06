from django.http import JsonResponse,HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from . import settings
from .models import Vendor, User, Reward
from .ethereum import manage


@csrf_exempt
@require_POST
def create_vendor(request):
    new_vendor = Vendor()
    if settings.DEBUG:
        vendor_name = "test_vendor"
    else:
        vendor_name = request.POST['vendor_name']

    new_vendor.name = vendor_name
    new_vendor.contract_address = manage.create_contract(vendor_name)
    new_vendor.save()
    return JsonResponse({'status':True, 'vendor_id':new_vendor.id})


@csrf_exempt
@require_POST
def create_user(request):
    new_user = User()
    if settings.DEBUG:
        new_user.first_name = 'test_first_name'
        new_user.last_name = 'test_last_name'
        new_user.email = 'test@email.com'
        new_user.tel = '0000000000'
    else:
        new_user.first_name = request.POST['first_name']
        new_user.last_name = request.POST['first_name']
        new_user.email = request.POST['first_name']
        new_user.tel = request.POST['first_name']
    new_user.wallet_address = manage.create_wallet()
    new_user.save()
    return JsonResponse({'status':True, 'user_id': new_user.id })


@csrf_exempt
@require_POST
def add_point(request):

    user_id = request.POST['user_id']
    vendor_id = request.POST['vendor_id']
    point = request.POST['point']

    manage.add_point(user_id,vendor_id,point)

    return JsonResponse({'status':True})


@csrf_exempt
@require_POST
def add_reward(request):

    if settings.DEBUG:
        item_name = 'test_item_name'
    else:
        item_name = request.POST['item_name']

    vendor_id = request.POST['vendor_id']
    point = request.POST['point']

    new_reward = Reward()
    new_reward.vendor = Vendor.objects.get(id=vendor_id)
    new_reward.name = item_name
    new_reward.point = point
    new_reward.save()

    return JsonResponse({'status':True, 'reward_id':new_reward.id})


@csrf_exempt
@require_POST
def get_item_by_vendor(request):
    vendor_id = request.POST['vendor_id']
    reward_list = Reward.objects.filter(vendor_id=vendor_id)

    return JsonResponse({'status':True,'result':reward_list})


@csrf_exempt
@require_POST
def exchange_reward(request):
    user_id = request.POST['user_id']
    reward_id = request.POST['reward_id']

    reward = Reward.objects.get(id=reward_id)

    manage.exchange_reward(user_id,reward_id,reward.vendor.id,reward.point)

    return JsonResponse({'status': True})


@csrf_exempt
@require_POST
def transfer_point(request):
    sender_id = request.POST['sender_id']
    receiver_id = request.POST['receiver_id']
    vendor_id = request.POST['vendor_id']
    point = request.POST['point']

    manage.transfer_point(sender_id,receiver_id,vendor_id,point)

    return JsonResponse({'status': True})


@csrf_exempt
def get_point_by_user(request,user_id=None):

    if settings.DEBUG:
        pass
    else:
        if request.method != 'POST':
            return HttpResponseBadRequest()
        user_id = request.POST['user_id']

    vendor_id_list = Vendor.objects.all().values_list(flat=True)
    point_by_vendor = manage.query_vendors_points_by_user_id(user_id,vendor_id_list)

    if settings.DEBUG:
        return point_by_vendor
    else:
        return JsonResponse({'status': True, 'result':point_by_vendor})


@csrf_exempt
def get_all_account(request):
    account_list = manage.get_all_account()
    return JsonResponse({'status': True, 'result':account_list})


@csrf_exempt
def test(request):
    return JsonResponse({'status': True, 'result': manage.test()})


# @csrf_exempt
# @require_POST
# def get_user_list(request):
#     return User.objects.all()