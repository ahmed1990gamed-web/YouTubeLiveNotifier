name: Notify Live Stream

on:
  schedule:
    - cron: '*/5 * * * *'  # السكربت هيشتغل كل 5 دقائق
  workflow_dispatch:  # يسمح بالتشغيل اليدوي أيضًا

jobs:
  notify:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run notify_live.py
        # عدّل notify_live.py حسب مكان الملف الفعلي
        run: python notify_live.py
        env:
          TELEGRAM_TOKEN: ${{ secrets.TELEGRAM_TOKEN }}
          CHAT_ID: ${{ secrets.CHAT_ID }}
          YOUTUBE_API_KEY: ${{ secrets.YOUTUBE_API_KEY }}
          KEYWORD: ${{ secrets.KEYWORD }}
