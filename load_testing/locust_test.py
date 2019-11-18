
from locust import HttpLocust, TaskSet, task, between


class WebsiteTasks(TaskSet):

    @task
    def get(self):
        self.client.get("/notes")


class WebsiteUser(HttpLocust):
    host = 'http://192.168.1.27'
    task_set = WebsiteTasks
    wait_time = between(1, 2)


# locust -f locust_test.py
