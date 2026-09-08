from django.test import TestCase
from rest_framework.test import APITestCase

from .models import Box, Product
from .services import can_fit, find_best_box


class CanFitTests(TestCase):

    def test_product_fits_when_rotated(self):
        product = Product.objects.create(
            name="Test Product",
            length=10,
            width=20,
            height=30,
            weight=1,
        )

        box = Box.objects.create(
            name="Test Box",
            internal_length=30,
            internal_width=10,
            internal_height=20,
            max_weight=5,
            cost=50,
        )

        self.assertTrue(can_fit(product, box))

    def test_product_does_not_fit_when_too_heavy(self):
        product = Product.objects.create(
            name="Heavy Product",
            length=10,
            width=20,
            height=30,
            weight=6,
        )

        Box.objects.create(
            name="Test Box",
            internal_length=30,
            internal_width=30,
            internal_height=30,
            max_weight=5,
            cost=50,
        )

        self.assertIsNone(find_best_box(product))


class BoxRecommendationAPITests(APITestCase):

    def test_recommend_box_success(self):
        product = Product.objects.create(
            name="Laptop",
            length=30,
            width=20,
            height=3,
            weight=2,
        )

        Box.objects.create(
            name="Small Box",
            internal_length=25,
            internal_width=25,
            internal_height=10,
            max_weight=5,
            cost=50,
        )

        medium_box = Box.objects.create(
            name="Medium Box",
            internal_length=35,
            internal_width=25,
            internal_height=10,
            max_weight=5,
            cost=80,
        )

        response = self.client.post(
            "/api/recommend-box/",
            {
                "product_id": product.id,
                "quantity": 1,
            },
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["box_id"], medium_box.id)
        self.assertEqual(response.data["box_name"], "Medium Box")

    def test_recommend_box_invalid_product(self):
        response = self.client.post(
            "/api/recommend-box/",
            {
                "product_id": 999,
                "quantity": 1,
            },
            format="json",
        )

        self.assertEqual(response.status_code, 404)

    def test_recommend_box_invalid_quantity(self):
        product = Product.objects.create(
            name="Laptop",
            length=30,
            width=20,
            height=3,
            weight=2,
        )

        response = self.client.post(
            "/api/recommend-box/",
            {
                "product_id": product.id,
                "quantity": 0,
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)

    def test_recommend_box_no_suitable_box(self):
        product = Product.objects.create(
            name="Heavy Product",
            length=30,
            width=20,
            height=3,
            weight=10,
        )

        Box.objects.create(
            name="Small Box",
            internal_length=40,
            internal_width=30,
            internal_height=10,
            max_weight=5,
            cost=50,
        )

        response = self.client.post(
            "/api/recommend-box/",
            {
                "product_id": product.id,
                "quantity": 1,
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data["detail"],
            "No suitable box found.",
        )