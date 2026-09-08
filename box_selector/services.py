from itertools import permutations

from .models import Box


def can_fit(product, box):
    product_dimensions = (
        product.length,
        product.width,
        product.height,
    )

    box_dimensions = (
        box.internal_length,
        box.internal_width,
        box.internal_height,
    )

    return any(
        all(
            product_dimension <= box_dimension
            for product_dimension, box_dimension
            in zip(orientation, box_dimensions)
        )
        for orientation in permutations(product_dimensions)
    )


def find_best_box(product):
    boxes = Box.objects.all().order_by("cost")

    for box in boxes:
        if can_fit(product, box) and product.weight <= box.max_weight:
            return box

    return None