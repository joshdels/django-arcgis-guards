from datetime import date

from django.test import TestCase

from apps.accounts.models import User
from apps.client.models import Client
from apps.contract.models import Contract
from apps.operations.models import Deployment


class DeploymentModelTest(TestCase):

    def test_create_deployment(self):
        user = User.objects.create_user(
            username="admin",
            password="password123",
        )

        client = Client.objects.create(
            user=user,
            name="ABC Security",
        )

        contract = Contract.objects.create(
            client=client,
            title="Mall Security",
            number_of_guards=5,
            start_date=date(2026, 1, 1),
            end_date=date(2026, 12, 31),
        )

        deployment = Deployment.objects.create(
            contract=contract,
            name="Night Shift",
            location="Main Entrance",
            required_guards=3,
            remarks="Main gate deployment",
        )

        self.assertEqual(deployment.name, "Night Shift")
        self.assertEqual(deployment.location, "Main Entrance")
        self.assertEqual(deployment.required_guards, 3)
        self.assertTrue(deployment.is_active)
