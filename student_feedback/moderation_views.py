from google.cloud import tasks_v2
from django.conf import settings 
from django.views.decorators.csrf import csrf_exempt
from .models import Feedback
from django.urls import reverse 
import json 
from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponseForbidden
from .llm_classifier import classify_feedback
import logging 

logger  = logging.getLogger(__name__)

task_client = tasks_v2.CloudTasksClient()
project = settings.GCP_PROJECT
location = settings.GCP_REGION


def create_moderation_task(feedback_id):

    logger.info(f'Creating moderation request for feedback ID {feedback_id}')

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

        # Ensure this request contains the moderation secret 
        secret = request.headers.get('X-Moderation-Task-Secret')

        if secret != settings.MODERATION_TASK_SECRET:
            return HttpResponseForbidden()

        # Otherwise, process the request 
        data = json.loads(request.body)
        feedback_id = data.get('feedback_id')
        feedback = Feedback.objects.get(id=feedback_id)

        classification = classify_feedback(feedback.text)

        logger.info(f'Classification: {classification}')

        # Update Feedback object and save to the database to update the record 

        if classification == 'genuine':
            feedback.approved = True 
            # TODO - send to the appropriate department, 
            # likely using another cloud task(s) to categorize the request,
            # and send messages, either individually, or more likely, in batches.  
        else:
            feedback.approved = False 
            # TODO - may wish to monitor the volume and types of spam 
        
        feedback.save()

        logger.info(f'Saved feedback object: {feedback}')
            
        return JsonResponse({'success': True, 'status': classification})

    except Exception as e: 
        logger.exception(f'Error classifing feedback', e)
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
