from pathlib import Path
import logging

from crontab import CronTab

if __name__ == "__main__":
    ROOT_DIR = Path(__file__).parent.parent

    pipenv = "/usr/local/bin/pipenv"
    pipfile = Path.joinpath(ROOT_DIR, "Pipfile")
    script_concepts = Path.joinpath(ROOT_DIR, "jobs", "harvest_concepts.py")
    script_datasets = Path.joinpath(ROOT_DIR, "jobs", "harvest_datasets.py")
    script_dataservices = Path.joinpath(ROOT_DIR, "jobs", "harvest_dataservices.py")
    logfile = Path.joinpath(ROOT_DIR, "jobs", "cron.log")

    logging.basicConfig(
        filename=logfile,
        format="%(asctime)s %(levelname)s: %(message)s",
        level=logging.INFO,
    )
    logging.info("Creating cron job")

    cron = CronTab(user=True)
    cron.remove_all()

    # Set up job for harvesting of concepts
    cron_command = f"cd /app && PIPENV_PIPFILE={pipfile} {pipenv} run python3 -u {script_concepts} >> {logfile} 2>&1"
    cron.new(command=cron_command).every(6).hours()

    # Set up job for harvesting of datasets
    cron_command = f"cd /app && PIPENV_PIPFILE={pipfile} {pipenv} run python3 -u {script_datasets} >> {logfile} 2>&1"
    cron.new(command=cron_command).every(1).hours()

    # Set up job for harvesting of dataservices
    cron_command = f"cd /app && PIPENV_PIPFILE={pipfile} {pipenv} run python3 -u {script_dataservices} >> {logfile} 2>&1"
    cron.new(command=cron_command).every(1).hours()

    cron.write()

    logging.info("--- Jobs in cron start ---")
    for job in cron:
        logging.info(job)
    logging.info("--- Jobs in cron end ---")

    logging.info("Done!")
