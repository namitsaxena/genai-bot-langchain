
class SchedulerUtility():

    def __init__(self):
        print("Scheduler utility initialized..")

    def get_job_status(self, job_name):
        """
        get's the given scheduler tool's job's status
        :param job_name: job's name
        :return: job's status
        """
        print(f"getting status for job: {job_name}")
        return "running"

    # stops the job
    def stop_job(self, job_name):
        print(f"stopping job: {job_name}")
        return True