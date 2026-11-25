# Sahibi Budget App

A beautiful, modern budget tracking app built with KivyMD featuring:
- **Category dropdown menu** with default categories (Groceries, Electric, Transport, etc.)
- **Add custom categories** with icons and colors
- **Salary tracking** with automatic deduction from expenses
- **Expense logging** with notes and categories
- **Category filtering** with chip-based UI
- **Data persistence** (local JSON storage)
- **Dark/Light theme** toggle
- **Modern Material Design 3** UI

## Features

### Category Dropdown Menu
- Pre-loaded categories: Groceries, Electric, Transport, Entertainment, Healthcare, Education, Shopping, Other
- **Add custom categories** with custom icons (Material Icons) and colors
- **Filter expenses** by tapping category chips
- **Delete custom categories** (built-in protected)

### Salary & Expense Tracking
- Set monthly salary
- **Expenses automatically deduct from salary**
- Remaining balance shown in real-time
- Color-coded: Green (positive), Red (negative)
- Add notes to both salary and expenses

### Modern UI Design
- Gradient salary card with icons
- Horizontal scrollable category filter chips
- Smooth animations and transitions
- Material Design 3 components
- Dark/Light theme support
- Navigation drawer for settings

## Building APK

### GitHub Actions (Recommended)
1. Push this folder to GitHub repository
2. Go to **Actions** tab
3. Click **"Build Budget App APK"**
4. Click **"Run workflow"** → **"debug"** → **"Run workflow"**
5. Wait 10-20 minutes
6. Download APK from **Artifacts**

### Local Build (Linux/WSL)
```bash
pip install cython==0.29.36 buildozer
buildozer -v android debug
```

## Project Structure
```
sahibi-budget-app/
├── .github/workflows/build-apk.yml   # GitHub Actions CI/CD
├── buildozer.spec                    # Buildozer configuration
├── main.py                           # Complete app (single file)
└── README.md
```

## Requirements
- Python 3.10 (pinned for buildozer compatibility)
- kivy, kivymd
- Android API 21+ (Android 5.0+)

## Data Storage
Data saved locally as JSON:
- Salary amount
- All expenses with category, note, date
- Custom categories
- Theme preference

## License
Personal use - Sahibi Budget App