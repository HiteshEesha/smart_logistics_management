# validators/business_validator.py

from datetime import datetime


class BusinessValidator:
    """
    Validates business rules for each row.
    """

    def validate(self, row: dict):
        """
        Returns a list of validation errors.
        """

        errors = []

        # Rule 1: Quantity should be greater than zero
        quantity = row.get("quantity")

        if quantity is not None:
            if quantity <= 0:
                errors.append("Quantity must be greater than 0.")

        # Rule 2: Shipment date cannot be in the future
        shipment_date = row.get("shipment_date")

        if shipment_date is not None:
            if shipment_date > datetime.today():
                errors.append("Shipment date cannot be a future date.")

        # Rule 3: Delivery date must be after shipment date
        delivery_date = row.get("delivery_date")

        if shipment_date and delivery_date:
            if delivery_date < shipment_date:
                errors.append(
                    "Delivery date must be after shipment date."
                )

        # Rule 4: Amount cannot be negative
        amount = row.get("amount")

        if amount is not None:
            if amount < 0:
                errors.append("Amount cannot be negative.")

        # Rule 5: Discount cannot exceed amount
        discount = row.get("discount")

        if amount is not None and discount is not None:
            if discount > amount:
                errors.append(
                    "Discount cannot exceed Amount."
                )

        # Rule 6: Email validation
        email = row.get("email")

        if email:
            if "@" not in email or "." not in email:
                errors.append("Invalid Email Address.")

        return errors