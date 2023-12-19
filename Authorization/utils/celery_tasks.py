class RetryTask(Task):
    autoretry_for = (Exception,)
    retry_kwargs = {'max_retries': 5}
    retry_backoff = 2
    retry_jitter = True

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        message = f"\n\tmessage: Failure of {self.name} task ID:{task_id}\t error:{exc}\targs{args}\tkwargs:{kwargs}\n\terror information:{einfo}\n"
        # celery_logger.error(msg=message)
        print(message)

    def on_success(self, retval, task_id, args, kwargs):
        message = f"\n\tmessage: Success of task ID:{task_id}\t result:{retval}\targs{args}\tkwargs:{kwargs}\n"
        # celery_logger.info(msg=message)
        print(message)

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        if self.request.retries > 3:
            message = f"\n\tmessage: {self.request.retries}th Retry of task ID:{task_id}\t error:{exc}\targs{args}\tkwargs:{kwargs}\n\terror information:{einfo}\n"
            print(message)
            # celery_logger.error(msg=message)

@celery.task(base=RetryTask)
def send_email_task(email_data):
    response = NotificationService.sinc_send_email_notification(email_data)
    # async def in_celery_send_email():
    #     ntf_response = await NotificationService.send_email_notification(email_data)
    #     return ntf_response
    # response = asyncio.run(in_celery_send_email())
    return response.status_code