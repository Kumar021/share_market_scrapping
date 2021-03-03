# share_market_scrapping
# RUN Server command
python manage.py runserver --settings=finance.settings.dev
python manage.py makemigrations --settings=finance.settings.dev
python manage.py migrate --settings=finance.settings.dev
python manage.py createsuperuser --settings=finance.settings.dev

SCRAPE COMMAND
python manage.py nifty_50_share --settings=finance.settings.dev (ONLY change file inside trading/management/commands folder)
