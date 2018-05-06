from django.template.response import TemplateResponse

from ..models import User, Vendor, Reward
from .. import API


def index(request):
    user_list = User.objects.all()
    vendor_list = Vendor.objects.all()

    points_list = []
    for user in user_list:
        points_list.append({'user_id':user.id,'point_list':[]})
        points = API.get_point_by_user(request,user.id)
        points_list[-1]['point_list'] = points

    reward_list = []
    for vendor in vendor_list:
        reward_list.append({'vendor_id': vendor.id, 'reward_list': []})
        reward_list[-1]['reward_list'] = Reward.objects.filter(vendor=vendor).values()


    return TemplateResponse(
        request=request,
        template='../templates/home.html',
        context={
            'user_list':user_list,
            'vendor_list':vendor_list,
            'point_list':points_list,
            'reward_list':reward_list,
        }
    )