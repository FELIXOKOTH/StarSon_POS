#!/bin/bash

# ============================
# STARSON POS - BRIGHT_ARM ENTERPRISE
# MITI PESA INTEGRATION LOCKDOWN
# ============================

# 1. Ask for encryption password
echo "Enter a strong passphrase to encrypt your MITI PESA integration:"
read -s PASSPHRASE

# 2. Encrypt the real integration file
openssl enc -aes-256-cbc -salt -in integrations/miti_pesa_api.py -out integrations/miti_pesa_api.py.enc -pass pass:$PASSPHRASE

# 3. Backup and remove original
mv integrations/miti_pesa_api.py integrations/miti_pesa_api.py.original.bak

# 4. Add a harmless dummy file
echo "# MITI PESA integration is currently inactive
def send_carbon_data_to_miti_pesa(*args, **kwargs):
    return {'status': 'inactive', 'message': 'MITI PESA is not yet enabled'}" > integrations/miti_pesa_api.py

# 5. Save decryption instructions
echo "# 🔒 MITI PESA Integration Activation
**Developer Note – Bright_Arm Enterprise (Founder only)**

To reactivate this secure module:

1. Decrypt the encrypted MITI PESA API file:
\`\`\`bash
openssl enc -aes-256-cbc -d -in integrations/miti_pesa_api.py.enc -out integrations/miti_pesa_api.py -pass pass:$PASSPHRASE
\`\`\`

2. Set environment variable:
\`\`\`bash
export ENABLE_MITI_PESA=true
\`\`\`

3. Restart the POS backend or system.

--- 

🔐 Passphrase used: ***KEEP THIS SAFE, DO NOT SHARE***
\`\`\`
$PASSPHRASE
\`\`\`

" > integrations/.miti_pesa_reactivation.md

echo "✅ MITI PESA integration secured and hidden."

