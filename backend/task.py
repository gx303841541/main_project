import time

from backend.httprunner.api import HttpRunner
from backend.httprunner.cli import main_hrun
from backend.httprunner.logger import logger
from celery import shared_task, task
from main_project import celery_app


@task
def run_case(something_about_cases, callback=None, dot_env_path=None):
    print("To run: %s" % (something_about_cases))
    try:
        runner = HttpRunner()
        runner.run(something_about_cases, )
    except Exception:
        print("!!!!!!!!!! exception stage: {} !!!!!!!!!!".format(runner.exception_stage))
        raise

    # runner.gen_html_report(
    #    html_report_name=args.html_report_name,
    #    html_report_template=args.html_report_template
    # )
    print(runner.summary)
    return runner.summary
