import json
import time
import random
from datetime import datetime

from backend.httprunner.api import HttpRunner
from backend.httprunner.logger import logger
from backend.models import *
from backend.utils import formater, pagination, rsp_msg
from celery import Celery, shared_task, task
from main_project import celery_app
from rest_framework.reverse import reverse

#celery_app = Celery('tasks', broker='amqp://guest@localhost//', backend='amqp://guest@localhost//')


@task
def add(x, y):
    print(x, y, x + y)
    return x + y


@task
def run_xxx(callback=None, dot_env_path=None):
    print("New task: to run suite %s" % ('xxoo'))
    return ('fuck you!')


@celery_app.task(bind=True)
def run_suite(self, callback=None, dot_env_path=None, *, suite):
    print("New task: to run suite %s" % (suite.name))
    timestamp = '_' + \
        datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H:%M:%S')
    # time.sleep(60)
    result = {
        'total': 0,
        'successes': 0,
        'failures': 0,
        'skipped': 0,
        'errors': 0,
        'unknow': 0
    }
    case_results = []
    for case in suite.my_cases.all().order_by('order'):
        case_result_msg, case_result = run_case(
            case=case, request=None, return_caseresult_url=False, statistics=True)
        case_results.append(case_result)
        if case_result_msg['success']:
            result['total'] += 1
            for item in case_result_msg['statistics']:
                result[item] += case_result_msg['statistics'][item]
        else:
            result['total'] += 1
            result['errors'] += 1

    suite_result = SuiteResult.objects.create(
        name=suite.name + timestamp + '--' + str(random.randint(10000000, 99999999)), suite=suite, **result)
    print("suite result %s created!" % (suite.name + timestamp))
    for case_result in case_results:
        if case_result:
            case_result.suiteresult = suite_result
            case_result.save()
    return result, suite_result


def run_case(callback=None, dot_env_path=None, return_caseresult_url=False, statistics=False, *, case, request):
    print("New task: to run case %s" % (case.name))
    case_ressult = None
    try:
        # format data to httprunner format
        data = formater.get_httprunner_case(case)

    except Exception as e:
        rsp_msg.CASE_RUN_FAIL['msg'] = str(e)
        return (rsp_msg.CASE_RUN_FAIL, case_ressult)

    try:
        timestamp = '_' + \
            datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H:%M:%S')
        runner = HttpRunner()
        runner.run(data, )
        # print(runner.summary)
        # runner.gen_html_report(html_report_name='report.html')
        records = runner.summary['details'][0].pop('records')
        result = 'pass' if runner.summary['success'] else 'fail'
        case_ressult = CaseResult.objects.create(
            name=case.name + timestamp, content=json.dumps(formater.bytes_to_str(runner.summary)), result=result, case=case)
        print("case result %s created!" % (case.name + timestamp))

        steps = case.my_steps.all().order_by('order')
        for step in steps:
            record = records.pop(0)
            result = 'pass' if record['status'] == 'success' else 'fail'
            if 'meta_data' in record and 'response' in record['meta_data'] and 'cookies' in record['meta_data']['response']:
                record['meta_data']['response']['cookies'] = 'To do it later...'

            step_result = StepResult.objects.create(
                name=step.name + timestamp, content=json.dumps(formater.bytes_to_str(record)), result=result, caseresult=case_ressult, step=step)
            print("step result %s created!" % (step.name + timestamp))

        if return_caseresult_url:
            rsp_msg.CASE_RUN_SUCCESS['result'] = reverse(
                'caseresult-detail', args=[case_ressult.pk], request=request)

        if statistics:
            successes = 0
            failures = 0
            skipped = 0
            errors = 0
            unknow = 0
            if runner.summary['success']:
                successes = 1
            elif runner.summary['stat']['failures']:
                failures = 1
            elif runner.summary['stat']['skipped']:
                skipped = 1
            elif runner.summary['stat']['errors']:
                errors = 1
            else:
                unknow = 1
            rsp_msg.CASE_RUN_SUCCESS['statistics'] = {
                'successes': successes,
                'failures': failures,
                'skipped': skipped,
                'errors': errors,
                'unknow': unknow
            }
        return (rsp_msg.CASE_RUN_SUCCESS, case_ressult)

    except Exception as e:
        rsp_msg.CASE_RUN_FAIL['msg'] = "[%s]: %s" % (
            runner.exception_stage, str(e))
        return (rsp_msg.CASE_RUN_FAIL, case_ressult)
