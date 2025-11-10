from django.conf import settings 
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse 
from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponseForbidden

from .models import Feedback
from .llm_classifier import classify_feedback

from google.cloud import tasks_v2

import json 
import logging 

logger  = logging.getLogger(__name__)

task_client = tasks_v2.CloudTasksClient()
project = settings.GCP_PROJECT
location = settings.GCP_REGION


def create_moderation_task(feedback_id):

    logger.debug(f'Creating moderation request for feedback ID {feedback_id}')

    parent = task_client.queue_path(project, location, 'feedback-moderation-queue')
    moderation_url = settings.BASE_URL + reverse('moderate_feedback')

    payload = json.dumps({'feedback_id': feedback_id}).encode()

    task = { 
        'http_request': {
            'http_method': tasks_v2.HttpMethod.POST,
            'url': moderation_url,
            'headers': {
                'Content-Type': 'application/json',
                'X-Moderation-Task-Secret': settings.MODERATION_TASK_SECRET
            },
            'body': payload
        }
    }

    logger.debug(f'Moderation task: {task}')

    task_client.create_task(request={'parent': parent, 'task': task})


@csrf_exempt
def moderate_feedback(request):  

    logger.info('Moderation request received')

    try: 
        if request.method != 'POST':
            return HttpResponseNotAllowed(['POST'])

        secret = request.headers.get('X-Moderation-Task-Secret') 

        if secret != settings.MODERATION_TASK_SECRET:
            return HttpResponseForbidden()

        data = json.loads(request.body)
        feedback_id = data.get('feedback_id')
        feedback = Feedback.objects.get(id=feedback_id)

        classification = classify_feedback(feedback.text)
        logger.info(f'Classification: {classification}')

        # Update Feedback object and save to the database to update the record 
        if classification == 'genuine':
            feedback.status = Feedback.APPROVED 
        else:
            feedback.status = Feedback.BLOCKED 
        
        feedback.save()
        logger.info(f'Saved feedback object: {feedback}')
            
        return JsonResponse({'success': True, 'status': classification})

    except Exception as e: 
        logger.exception(f'Error classifing feedback', e)
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


