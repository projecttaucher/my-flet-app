name: Build Flet APK
on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Java
        uses: actions/setup-java@v4
        with:
          distribution: 'temurin'
          java-version: '17'

      - name: Setup Flutter
        uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.22.0' # إصدار ثابت ومستقر

      - uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: Install Flet
        run: pip install flet

      - name: Build APK
        # هنا نخبر النظام أننا جهزنا Flutter بالفعل، فلا داعي للسؤال
        run: flet build apk main.py --module-name main
