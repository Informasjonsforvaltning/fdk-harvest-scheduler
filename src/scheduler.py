from pathlib import Path
import logging

from crontab import CronTab

if __name__ == "__main__":
    ROOT_DIR = Path(__file__).parent.parent

    poetry = "/usr/local/bin/poetry"
    script_concepts = Path.joinpath(ROOT_DIR, "jobs", "harvest_concepts.py")
    script_datasets = Path.joinpath(ROOT_DIR, "jobs", "harvest_datasets.py")
    script_dataservices = Path.joinpath(ROOT_DIR, "jobs", "harvest_dataservices.py")
    script_public_services = Path.joinpath(ROOT_DIR, "jobs", "harvest_public_services.py")
    script_informationmodels = Path.joinpath(ROOT_DIR, "jobs", "harvest_informationmodels.py")
    script_compact_fuseki = Path.joinpath(ROOT_DIR, "jobs", "compact_fuseki.py")
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
    cron_command = f"cd /app && {poetry} run python3 -u {script_concepts} >> {logfile} 2>&1"
    cron.new(command=cron_command).every(6).hours()

    # Set up job for harvesting of datasets
    cron_command = f"cd /app && {poetry} run python3 -u {script_datasets} >> {logfile} 2>&1"
    cron.new(command=cron_command).every(1).hours()

    # Set up job for harvesting of dataservices
    cron_command = f"cd /app && {poetry} run python3 -u {script_dataservices} >> {logfile} 2>&1"
    cron.new(command=cron_command).every(1).hours()

    # Set up job for harvesting of public_services
    cron_command = f"cd /app && {poetry} run python3 -u {script_public_services} >> {logfile} 2>&1"
    cron.new(command=cron_command).every(1).hours()

    # Set up job for harvesting of information models
    cron_command = f"cd /app && {poetry} run python3 -u {script_informationmodels} >> {logfile} 2>&1"
    cron.new(command=cron_command).every(6).hours()

    # Set up job for compaction of Fuseki database
    cron_command = f"cd /app && {poetry} run python3 -u {script_compact_fuseki} >> {logfile} 2>&1"
    cron.new(command=cron_command).setall('30 8,20 * * *')

    cron.write()

    logging.info("--- Jobs in cron start ---")
    for job in cron:
        logging.info(job)
    logging.info("--- Jobs in cron end ---")

    logging.info("Done!")
