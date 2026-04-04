import random
from locust import HttpUser, task, between

class PrecognitoUser(HttpUser):
    wait_time = between(1, 5)
    
    def on_start(self):
        """Mock login by setting a session cookie or header."""
        # In a real test we would hit the login endpoint
        # For performance tests, we can often pre-generate tokens
        self.headers = {"Authorization": "Bearer admin-token-mock"}

    @task(3)
    def view_dashboard(self):
        """Simulate a user viewing the dashboard assets."""
        self.client.get("/assets?limit=50&offset=0", headers=self.headers)

    @task(1)
    def view_anomalies(self):
        """Simulate a user viewing anomaly history."""
        self.client.get("/anomalies?limit=20", headers=self.headers)

    @task(5)
    def ingest_data(self):
        """Simulate a device sending telemetry data."""
        device_id = f"motor_{random.randint(1, 100)}"
        payload = {
            "device_id": device_id,
            "temperature": random.uniform(20.0, 90.0),
            "vibration": random.uniform(0.01, 0.5),
            "pressure": random.uniform(90.0, 110.0)
        }
        # Ingest endpoint is protected by admin_only
        self.client.post("/ingest/dev", json=payload, headers=self.headers)

    @task(2)
    def check_health(self):
        """Simulate a load balancer health check."""
        self.client.get("/health")
