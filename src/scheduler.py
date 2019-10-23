from pathlib import Path

from crontab import CronTab

if __name__ == '__main__':

    ROOT_DIR = Path(__file__).parent.parent

    pipenv = '/usr/local/bin/pipenv'
    pipfile = Path.joinpath(ROOT_DIR, 'Pipfile')
    script = Path.joinpath(ROOT_DIR, 'jobs', 'harvest.py')
    logfile = Path.joinpath(ROOT_DIR, 'jobs', 'make.log')

    cron = CronTab(user=True)
    cron.remove_all()

    cron_command = f'PIPENV_PIPFILE={pipfile} {pipenv} run python3 {script} >> {logfile} 2>&1'
    cron.new(command=cron_command).hour.every(6)

    cron.write()
