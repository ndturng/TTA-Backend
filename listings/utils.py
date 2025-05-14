"""
Utility functions for the listings app.
"""
from datetime import datetime


def product_media_path(instance, filename):
    """
    File will be uploaded to MEDIA_ROOT/products/{product_id}/{year}/{month}/{day}/{filename}
    Handle cases where the product might not be saved yet.

    Args:
        instance: The ProductMedia instance
        filename: Original filename

    Returns:
        str: Path where the file should be saved
    """
    now = datetime.now()

    # Check if the product is saved (has an id) or use a temporary folder
    if hasattr(instance, 'product') and instance.product and instance.product.id:
        product_id = instance.product.id
    else:
        # Use a temporary folder for files uploaded before the product is saved
        product_id = 'unsaved'

    return f"products/{product_id}/{now.year}/{now.month}/{now.day}/{filename}"


def generate_product_id(product_instance):
    """
    Generate a custom ID based on product type.

    Args:
        product_instance: The RealEstateProduct instance

    Returns:
        str: Generated ID in format {prefix}-{number}
    """
    # Import here to avoid circular import
    from listings.models import RealEstateProduct

    # Define prefix for each product type
    type_prefixes = {
        "land": "L",
        "townhouse": "T",
        "villa": "V",
        "apartment": "A",
    }

    # Get prefix based on product type
    prefix = type_prefixes.get(product_instance.type, "X")

    # Find the latest product with the same prefix
    latest_products = RealEstateProduct.objects.filter(
        id__startswith=f"{prefix}-"
    ).order_by('id')

    if latest_products.exists():
        # Get the latest ID and increment the number
        latest_id = latest_products.last().id
        # Extract the number part
        try:
            latest_num = int(latest_id.split('-')[1])
            # Increment and zero-pad to 3 digits
            new_num = str(latest_num + 1).zfill(3)
        except (ValueError, IndexError):
            # Fallback in case of parsing error
            new_num = "001"
    else:
        # First product of this type
        new_num = "001"

    return f"{prefix}-{new_num}"
