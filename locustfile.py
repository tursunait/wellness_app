from locust import HttpUser, task, between


class WellnessUser(HttpUser):
    wait_time = between(1, 5)  # Wait between 1 and 5 seconds between tasks

    @task
    def visit_homepage(self):
        self.client.get(
            "/"
        )  # Equivalent to visiting http://wellness-app-tursunai.online:8501/
