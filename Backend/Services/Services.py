from django.contrib.auth.models import User
from fcm_django.models import FCMDevice


def send_push(title, body, data, to):
    try:
        user = User.objects.get(id=1)
        device = FCMDevice.objects.create(registration_id=to,
                                          user=user)
        device.send_message(title=title, body=body, data=data)
        return True
        # return JsonResponse({'code': 0, 'message': "ok"})
    except Exception as e:
        print(e.message)
        return False
        # return JsonResponse({'code': 2, 'message': "error"})