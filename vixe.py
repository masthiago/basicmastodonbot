from datetime import datetime, timedelta
from pathlib import Path
from random import randint
from time import sleep
from decouple import config
from mastodon import Mastodon

try:

    app_secret = Path(config('APP_SECRET_FILE'))

    if app_secret.is_file() is not True:
        Mastodon.create_app(
            config('APP_NAME'),
            api_base_url=config('BASE_INSTANCE_URL'),
            to_file=config('APP_SECRET_FILE')
        )

    cuscuzin = Mastodon(
        client_id=config('APP_SECRET_FILE'),
        api_base_url=config('BASE_INSTANCE_URL')
    )

    client_secret = Path(config('CLIENT_SECRET_FILE'))

    if client_secret.is_file() is True:

        cuscuzin = Mastodon(
            access_token=config('CLIENT_SECRET_FILE'),
            api_base_url=config('BASE_INSTANCE_URL')
        )

    else:
        cuscuzin.log_in(
            config('LOGIN_EMAIL'),
            config('LOGIN_PASSWORD'),
            to_file=config('CLIENT_SECRET_FILE')
        )

except Exception as err:
    print('\nAuthentication failed. \n{}\n'.format(err))
    exit(1)


try:

    while True:
        interval = randint(
            config('MIN_TIME_RANGE', cast=int),
            config('MAX_TIME_RANGE', cast=int)
        )
        repeat = {
            'is': 'i' * randint(1, 16),
            'xis': 'x' * randint(1, 8),
            'es': 'e' * randint(1, 8),
        }

        vixe = 'V{is}{xis}{es}!'.format(**repeat)

        next = (datetime.now() + timedelta(seconds=interval)).strftime(
            '%d/%m/%Y %H:%Mh'
        )

        next_str = 'Next: \n\n{} \n\n{}'.format(next, vixe)

        with open('next.txt', 'w') as next_file:
            next_file.write(next_str + '\n')

        cuscuzin.status_post(next_str, visibility='direct')

        sleep(interval)
        cuscuzin.toot(vixe)


except KeyboardInterrupt:
    print('\nExit\n')
    exit(0)

except Exception as err:
    print('\nRepeat failure. \n{}\n'.format(err))
    exit(2)
