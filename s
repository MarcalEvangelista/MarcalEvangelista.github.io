name: Update ADS Publications

on:
  schedule:
    - cron: '0 0 * * 0' # roda todo domingo à meia-noite UTC
  workflow_dispatch:  # permite execução manual

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.x

      - name: Install PyYAML
        run: pip install pyyaml requests

      - name: Run update script
        run: python scripts/update_publications.py

      - name: Commit changes
        run: |
          git config --global user.name "github-actions"
          git config --global user.email "github-actions@github.com"
          git add _data/publications.yml
          git commit -m "Atualização automática das publicações ADS" || echo "Sem mudanças"
          git push
