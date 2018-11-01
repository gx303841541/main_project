# -*- coding: utf-8 -*-

"""
by Kobe Gong 2018-10-25
"""
import importlib
import os
import sys

import backend.httprunner.logger as logger
import backend.httprunner.parser as parser
from backend.httprunner.loader import (_extend_block, load_project_tests,
                                       load_python_module)
from backend.httprunner.utils import convert_to_dictstr
from backend.models import *

sys.path.insert(0, os.path.join(os.getcwd(), "backend/httprunner"))


class Formater():
    def __init__(self, ori_data):
        self.ori_data = ori_data

    def get_backend_api(self, data=None):
        TODO

    def get_frontend_api(self, data=None):
        TODO

    def get_backend_case(self, data=None):
        TODO

    def get_frontend_case(self, data=None):
        TODO

    def get_backend_step(self, data=None):
        TODO

    def get_frontend_step(self, data=None):
        pass


def get_backend_api(request_data):
    pass


def get_backend_case(request_data):
    pass


def get_backend_step(request_data):
    pass


def get_frontend_api(api_instance):
    pass


def get_frontend_case(case_instance):
    pass


def get_frontend_step(step_instance):
    pass


def get_httprunner_api(api_instance):
    api = {}
    # name
    if hasattr(api_instance, 'name'):
        function_meta = parser.parse_function(api_instance.name)
        name = function_meta["func_name"]
        api[name] = {}
        api[name]["function_meta"] = function_meta
    else:
        print('api name empty！')
        return False

    # variables
    if hasattr(api_instance, 'variables'):
        api[name]['variables'] = api_instance.variables
    else:
        api[name]['variables'] = []

    # request
    api[name]['request'] = {}
    # base_url and method
    api[name]['request']['base_url'] = api_instance.api_url
    api[name]['request']['method'] = api_instance.method

    # header
    if hasattr(api_instance, 'header'):
        api[name]['request']['header'] = api_instance.header
    else:
        api[name]['request']['header'] = {}

    # header
    if hasattr(api_instance, 'data'):
        api[name]['request']['data'] = api_instance.data
    elif hasattr(api_instance, 'parameters'):
        api[name]['request']['data'] = api_instance.parameters
    else:
        api[name]['request']['data'] = {}

    # validate
    if hasattr(api_instance, 'validate'):
        api[name]['validate'] = api_instance.validate
    else:
        api[name]['validate'] = {}

    # print(convert_to_dictstr(api))
    return api


def get_httprunner_case(case_instance):
    case = {}
    # step 1: get config
    case['config'] = {}
    # name
    if hasattr(case_instance, 'name'):
        case['config']['name'] = case_instance.name
    else:
        case['config']['name'] = 'I am a no name case, so said!'

    # parameters
    if hasattr(case_instance, 'parameters'):
        case['config']['parameters'] = case_instance.parameters
    else:
        case['config']['parameters'] = []

    # variables
    if hasattr(case_instance, 'variables'):
        case['config']['variables'] = case_instance.variables
    else:
        case['config']['variables'] = []

    # request
    case['config']['request'] = {}
    # base_url
    if hasattr(case_instance, 'base_url'):
        case['config']['request']['base_url'] = case_instance.base_url
    else:
        print('case name: %s, no base_url found!' % (case['config']['name']))
        return False

    # header
    if hasattr(case_instance, 'header'):
        case['config']['request']['header'] = case_instance.header
    else:
        case['config']['request']['header'] = {}

    # path
    case['config']['path'] = 'see me fly, I am flying in the sky...'

    # refs
    case['config']['refs'] = {}
    # debugtalk
    case['config']['refs']['debugtalk'] = {}
    case['config']['refs']['debugtalk'] = load_python_module(importlib.import_module("debugtalk"))

    # def-api
    api_map = {}
    case['config']['refs']['def-api'] = []
    for api_instance in case_instance.apis.all():
        api = get_httprunner_api(api_instance)
        if api:
            case['config']['refs']['def-api'] .append(api)
            api_name = list(api.keys())[0]
            api_map[api_name] = api[api_name]

    # def-testcase
    case['config']['refs']['def-testcase'] = {}

    # env
    case['config']['refs']['env'] = {}

    # step 2: get step
    case['teststeps'] = []
    steps = case_instance.my_steps.all().order_by('order')
    for step in steps:
        casestep = {}
        # name
        if hasattr(step, 'name'):
            casestep['name'] = step.name
        else:
            casestep['name'] = 'I am a no name step, so said!'

        # variables
        if hasattr(step, 'variables'):
            casestep['variables'] = step.variables
        else:
            casestep['variables'] = {}

        # extract
        if hasattr(step, 'extract'):
            casestep['extract'] = step.extract
        else:
            casestep['extract'] = {}

        # base_url
        if hasattr(step, 'base_url'):
            casestep['base_url'] = step.extract

        # header
        if hasattr(step, 'header'):
            casestep['header'] = step.header

        # validate
        if hasattr(step, 'validate'):
            casestep['validate'] = step.validate
        else:
            casestep['validate'] = {}

        # api
        if hasattr(step, 'api'):
            api = step.api
            casestep['api'] = api.name
            def_block = _get_block_by_name(casestep['api'], api_map)
            _extend_block(casestep, def_block)

        case['teststeps'].append(casestep)

    print(convert_to_dictstr(case))
    return case


def _get_api_name(api_with_paramaters):
    return api_with_paramaters.split('(')[0]


def _get_block_by_name(api_name, api_map):
    function_meta = parser.parse_function(api_name)
    func_name = function_meta["func_name"]
    call_args = function_meta["args"]
    block = api_map[func_name]
    def_args = block.get("function_meta", {}).get("args", [])

    if len(call_args) != len(def_args):
        err_msg = "{}: call args number is not equal to defined args number!\n".format(func_name)
        err_msg += "defined args: {}\n".format(def_args)
        err_msg += "reference args: {}".format(call_args)
        logger.log_error(err_msg)
        raise exceptions.ParamsError(err_msg)

    args_mapping = {}
    for index, item in enumerate(def_args):
        if call_args[index] == item:
            continue

        args_mapping[item] = call_args[index]

    if args_mapping:
        block = parser.substitute_variables(block, args_mapping)

    return block
