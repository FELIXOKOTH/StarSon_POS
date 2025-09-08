from .kra_etims import KraEtimsService

# A dictionary that maps provider names to their respective service classes.
REVENUE_SERVICE_PROVIDERS = {
    "KRA_ETIMS": KraEtimsService,
    "kra": KraEtimsService, 
    # Add other providers here as you create them.
}

def get_revenue_service(provider_name):
    """
    Returns an instance of the specified revenue service provider.

    Args:
        provider_name: The name of the provider (e.g., "KRA_ETIMS").

    Returns:
        An instance of the RevenueService, or None if the provider is not found.
    """
    provider_class = REVENUE_SERVICE_PROVIDERS.get(provider_name)
    return provider_class() if provider_class else None
