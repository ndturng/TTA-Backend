"""
Tests for utility functions in the listings app.
"""
from django.test import TestCase
from unittest.mock import patch, MagicMock
from datetime import datetime
from listings.utils import product_media_path, generate_product_id
from listings.models import RealEstateProduct


class ProductMediaPathTests(TestCase):
    """Tests for the product_media_path function."""

    def setUp(self):
        """Set up test data."""
        # Create a mock product with ID
        self.mock_product = MagicMock()
        self.mock_product.id = "T-001"

        # Create a mock instance with product
        self.mock_instance = MagicMock()
        self.mock_instance.product = self.mock_product

    @patch('listings.utils.datetime')
    def test_product_media_path_with_valid_product(self, mock_datetime):
        """Test product_media_path with a valid product that has an ID."""
        # Mock the datetime.now() to return a fixed date
        mock_now = MagicMock()
        mock_now.year = 2025
        mock_now.month = 5
        mock_now.day = 14
        mock_datetime.now.return_value = mock_now

        # Call the function
        path = product_media_path(self.mock_instance, "test.png")

        # Check the result
        self.assertEqual(path, "products/T-001/2025/5/14/test.png")

    @patch('listings.utils.datetime')
    def test_product_media_path_with_unsaved_product(self, mock_datetime):
        """Test product_media_path with a product that doesn't have an ID yet."""
        # Mock datetime
        mock_now = MagicMock()
        mock_now.year = 2025
        mock_now.month = 5
        mock_now.day = 14
        mock_datetime.now.return_value = mock_now

        # Create instance without a product ID
        instance = MagicMock()
        instance.product = None

        # Call the function
        path = product_media_path(instance, "test.png")

        # Check that it uses the 'unsaved' folder
        self.assertEqual(path, "products/unsaved/2025/5/14/test.png")


class GenerateProductIdTests(TestCase):
    """Tests for the generate_product_id function."""

    def setUp(self):
        """Set up test data."""
        # Create test products
        RealEstateProduct.objects.create(
            id="T-001",
            title="Test Townhouse",
            description="A townhouse for testing",
            area=120,
            location="Test Location",
            price=1000000,
            for_sale=True,
            type="townhouse"
        )

        RealEstateProduct.objects.create(
            id="V-001",
            title="Test Villa",
            description="A villa for testing",
            area=200,
            location="Test Location",
            price=2000000,
            for_sale=True,
            type="villa"
        )

    def test_generate_id_for_existing_type(self):
        """Test generating an ID for a product type that already exists."""
        # Create a new townhouse product (without saving)
        new_townhouse = RealEstateProduct(
            title="New Townhouse",
            description="Another townhouse",
            area=130,
            location="Test Location",
            price=1100000,
            for_sale=True,
            type="townhouse"
        )

        # Generate ID
        product_id = generate_product_id(new_townhouse)

        # Check that it increments correctly
        self.assertEqual(product_id, "T-002")

    def test_generate_id_for_new_type(self):
        """Test generating an ID for a product type that doesn't exist yet."""
        # Create a new apartment product (without saving)
        new_apartment = RealEstateProduct(
            title="New Apartment",
            description="An apartment",
            area=80,
            location="Test Location",
            price=800000,
            for_sale=True,
            type="apartment"
        )

        # Generate ID
        product_id = generate_product_id(new_apartment)

        # Check that it starts from 001
        self.assertEqual(product_id, "A-001")

    def test_generate_id_with_unknown_type(self):
        """Test generating an ID for an unknown product type."""
        # Create a product with an unknown type
        unknown_product = RealEstateProduct(
            title="Unknown Product",
            description="Product with unknown type",
            area=100,
            location="Test Location",
            price=1000000,
            for_sale=True,
            type="unknown"
        )

        # Generate ID
        product_id = generate_product_id(unknown_product)

        # Check that it uses the fallback prefix
        self.assertEqual(product_id, "X-001")
