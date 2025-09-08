from abc import ABC, abstractmethod

class RevenueService(ABC):
    """
    An abstract base class for all revenue service integrations.
    """

    @abstractmethod
    def send_invoice(self, invoice_data):
        """
        Sends invoice data to the revenue authority.

        Args:
            invoice_data: A dictionary containing the invoice details.

        Returns:
            A dictionary containing the response from the revenue authority.
        """
        pass

    @abstractmethod
    def get_tax_rates(self, country_code):
        """
        Retrieves the current tax rates for a given country.

        Args:
            country_code: The ISO 3166-1 alpha-2 country code.

        Returns:
            A dictionary of tax rates.
        """
        pass

    @abstractmethod
    def verify_customer_pin(self, pin, country_code):
        """
        Verifies a customer's tax PIN.

        Args:
            pin: The customer's tax PIN.
            country_code: The ISO 3166-1 alpha-2 country code.

        Returns:
            A boolean indicating whether the PIN is valid.
        """
        pass
