# StarSon POS Backend PDF Email Module

## Features
- Generates PDF receipts from sales data.
- Sends PDF to customer's email automatically.

## Structure
- `main.py` - Trigger logic.
- `utils/` - PDF and email tools.
- `receipts/` - PDF storage and templates.

## GitHub Upload (Mobile)
1. Go to https://github.com on your browser.
2. Create a new repo (e.g., StarSon-POS-Backend).
3. In repo, click **Add file > Upload files**.
4. Upload the extracted contents of this zip.
5. Commit directly to `main`.
6. (Optional) Use GitHub mobile app for easier tracking.

## Security
- Use `.env` file to secure email credentials.
- Ensure server limits access to `generated/` folder.