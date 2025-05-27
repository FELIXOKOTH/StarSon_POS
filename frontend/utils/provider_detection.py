def detect_provider(phone_number):
    safaricom_prefixes = ['+254700', '+254701', '+254702', '+254703', '+254704', '+254705', '+254706',
                          '+254707', '+254708', '+254709', '+254710', '+254711', '+254712', '+254713',
                          '+254714', '+254715', '+254716', '+254717', '+254718', '+254719']
    airtel_prefixes = ['+254730', '+254731', '+254732', '+254733', '+254734', '+254735', '+254736',
                       '+254737', '+254738', '+254739']
    telkom_prefixes = ['+254770', '+254771', '+254772', '+254773', '+254774', '+254775']

    for prefix in safaricom_prefixes:
        if phone_number.startswith(prefix):
            return "Safaricom"
    for prefix in airtel_prefixes:
        if phone_number.startswith(prefix):
            return "Airtel"
    for prefix in telkom_prefixes:
        if phone_number.startswith(prefix):
            return "Telkom Kenya"

    return "Unknown Provider"

# Test example
print(detect_provider('+254712345678'))  # Output: Safaricom

