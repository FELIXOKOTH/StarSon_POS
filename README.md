
# StarSon POS Enhancements

StarSon POS is a modular, eco-friendly Point-of-Sale system developed by BRIGHTARM Enterprise in collaboration with Greenpeace Africa. This repository contains enhancements aimed at addressing modern POS system challenges while promoting sustainability and global compliance.

## Key Enhancements Included

### 1. Tree-Saving Logic in Receipts
- Calculates number of trees saved per receipt.
- Visible on eco-receipts, avoids duplication per receipt ID.

### 2. Mobile Provider Detection
- Detects customer’s mobile network from phone number.
- Auto-routes SMS via client’s preferred local provider.
- Maintains privacy using backend logic with no external exposure.

### 3. Role-Based Shift Tracking
- Unique login for each cashier.
- Shift start, end, and break tracking.
- Daily report generation per user for accountability.

### 4. Offline Data Sync
- Allows data input offline.
- Auto-syncs when online.
- Ensures business continuity and remote deployments.

### 5. Language Translation Module
- Multilingual interface support (auto and manual).
- Backend integration with future localization options.

### 6. Technician Access System
- Technicians install front-end only.
- Department Heads can assign technicians.
- Admin controls core and system-wide access.

## Installation

1. Clone the repository or upload files manually:
   ```bash
   git clone https://github.com/your-felixokoth/StarSon_POS.git
   ```

2. Unzip and place contents in relevant `frontend` and `backend` folders.

3. Configure `.env` file and run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. Start the backend and test locally:
   ```bash
   python manage.py runserver
   ```

## Admin Access

- Default admin credentials:
  - **Username:** `admin`
  - **Password:** `..............`
- Please change after first login.

## License

Developed by BRIGHTARM Enterprise. Protected and intended for ethical climate-smart use.
