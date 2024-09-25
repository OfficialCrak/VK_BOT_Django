import json
import time

import vk_api
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from vk_api.utils import get_random_id
import asyncio
import aiohttp
from .config import VK_GROUP_TOKEN, CONFIRMATION_TOKEN
import logging
from aiovk import TokenSession, API
import random
logging.basicConfig(level=logging.INFO)
vk_session = vk_api.VkApi(token=VK_GROUP_TOKEN)
vk = vk_session.get_api()


def generate_large_random_id():
    return random.randint(1, 9999999999999999)


@csrf_exempt
def bot(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        event_type = body.get('type')

        if event_type == 'confirmation':
            return HttpResponse(CONFIRMATION_TOKEN)

        elif event_type == 'message_new':
            message = body['object']['message']['text']
            user_id = body['object']['message']['from_id']
            message_id = body['object']['message']['id']
            logging.info(f"Получено сообщение: {message} от {user_id}, message_id: {message_id}")

            random_id = generate_large_random_id()

            try:
                vk.messages.send(
                    user_id=user_id,
                    random_id=random_id,
                    message=f"Повторяю за вами: {message}"
                )
                logging.info(f"Сообщение {message} его random_id {random_id}")
                logging.info(f"Отправлен ответ: {message} пользователю {user_id} с random_id: {random_id}")
            except vk_api.exceptions.ApiError as e:
                logging.error(f"Ошибка отправки сообщения: {e}")

            return HttpResponse('ok', status=200)

    return JsonResponse({'response': 'not supported'})


