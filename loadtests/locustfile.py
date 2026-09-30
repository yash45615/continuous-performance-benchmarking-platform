from locust import HttpUser, between, task


class ApiUser(HttpUser):

    wait_time = between(
        0.1,
        0.5
    )

    @task(5)
    def health(self):

        self.client.get(
            "/health",
            name="GET /health"
        )

    @task(3)
    def product(self):

        self.client.get(
            "/api/products/101",
            name="GET /api/products/{id}"
        )

    @task(1)
    def slow_endpoint(self):

        self.client.get(
            "/api/slow",
            name="GET /api/slow"
        )