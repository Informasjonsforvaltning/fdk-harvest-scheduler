from pathlib import Path
import logging

from crontab import CronTab

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',level=logging.INFO)
    logging.info('Creating cron job')
    ROOT_DIR = Path(__file__).parent.parent

    pipenv = '/usr/local/bin/pipenv'
    pipfile = Path.joinpath(ROOT_DIR, 'Pipfile')
    script = Path.joinpath(ROOT_DIR, 'jobs', 'harvest.py')
    logfile = Path.joinpath(ROOT_DIR, 'jobs', 'cron.log')

    cron = CronTab(user=True)
    cron.remove_all()

    cron_command = f'PIPENV_PIPFILE={pipfile} {pipenv} run python3 {script} >> {logfile} 2>&1'
    cron.new(command=cron_command).hour.every(6)

    cron.write()

    logging.info('--- Jobs in cron start ---')
    for job in cron:
        logging.info(job)
    logging.info('--- Jobs in cron end ---')

    logging.info('Done!')
