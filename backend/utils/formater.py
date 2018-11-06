# -*- coding: utf-8 -*-

"""
by Kobe Gong 2018-10-25
"""
import copy
import importlib
import json
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
        api["function_meta"] = function_meta
    else:
        print('api name empty！')
        return False

    # variables
    if hasattr(api_instance, 'variables') and api_instance.variables:
        api['variables'] = _parser_variables(api_instance.variables)

    # request
    api['request'] = {}
    # base_url and method
    api['request']['url'] = api_instance.api_url
    api['request']['method'] = api_instance.method

    # headers
    if hasattr(api_instance, 'headers') and api_instance.headers:
        api['request']['headers'] = _parser_headers(api_instance.headers)

    # content
    if hasattr(api_instance, 'data') and api_instance.data:
        api['request']['data'] = _parser_content(api_instance.data)
    elif hasattr(api_instance, 'params') and api_instance.params:
        api['request']['params'] = _parser_content(api_instance.params)
    elif hasattr(api_instance, 'json') and api_instance.json:
        api['request']['json'] = _parser_content(api_instance.json)

    # validate
    if hasattr(api_instance, 'validate') and api_instance.validate:
        api['validate'] = _parser_validate(api_instance.validate)

    # print(convert_to_dictstr(api))
    return name, api


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
    if hasattr(case_instance, 'parameters') and case_instance.parameters:
        case['config']['parameters'] = _parser_parameters(case_instance.parameters)

    # variables
    if hasattr(case_instance, 'variables') and case_instance.variables:
        case['config']['variables'] = _parser_variables(case_instance.variables)

    # request
    case['config']['request'] = {}
    # base_url
    if hasattr(case_instance, 'base_url') and case_instance.base_url:
        case['config']['request']['base_url'] = case_instance.base_url
    else:
        print('case name: %s, no base_url found!' % (case['config']['name']))
        return False

    # headers
    if hasattr(case_instance, 'headers') and case_instance.headers:
        case['config']['request']['headers'] = _parser_headers(case_instance.headers)

    # path
    case['config']['path'] = 'see me fly, I am flying in the sky...'

    # refs
    case['config']['refs'] = {}
    # debugtalk
    case['config']['refs']['debugtalk'] = {}
    case['config']['refs']['debugtalk'] = load_python_module(importlib.import_module("debugtalk"))

    # def-api
    case['config']['refs']['def-api'] = {}
    for api_instance in case_instance.apis.all():
        name, api = get_httprunner_api(api_instance)
        if name:
            case['config']['refs']['def-api'][name] = api

    # def-testcase
    case['config']['refs']['def-testcase'] = {}

    # env
    case['config']['refs']['env'] = {}

    # step 2: get step
    case['teststeps'] = []
    steps = case_instance.my_steps.all().order_by('order')
    if not steps:
        print('case name: %s, no steps found!' % (case['config']['name']))
        return False
    else:
        for step in steps:
            casestep = {}
            # name
            if hasattr(step, 'name'):
                casestep['name'] = step.name
            else:
                casestep['name'] = 'I am a no name step, so said!'
            print('step: %s' % casestep['name'])

            # variables
            if hasattr(step, 'variables') and step.variables:
                casestep['variables'] = _parser_variables(step.variables)

            # extract
            if hasattr(step, 'extract') and step.extract:
                casestep['extract'] = _parser_extract(step.extract)

            # base_url
            if hasattr(step, 'base_url') and step.base_url:
                casestep['base_url'] = step.base_url

            # headers
            if hasattr(step, 'headers') and step.headers:
                casestep['header'] = step.headers

            # validate
            if hasattr(step, 'validate') and step.validate:
                casestep['validate'] = _parser_validate(step.validate)

            # api
            if hasattr(step, 'api'):
                api = step.api
                casestep['api'] = api.name
                def_block = _get_block_by_name(casestep['api'], case['config']['refs']['def-api'])
                _extend_block(casestep, def_block)

            case['teststeps'].append(casestep)

    # print(convert_to_dictstr(case))
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


def _parser_parameters(ori):
    print("parameters ori: %s" % ori)
    dst = []
    if isinstance(ori, (list)):
        return ori
    elif isinstance(ori, (str, bytes)):
        try:
            tmp_dst = json.loads(ori)
            if isinstance(tmp_dst, (list)):
                return tmp_dst
            elif isinstance(tmp_dst, (dict)):
                return [tmp_dst]
        except (TypeError, json.decoder.JSONDecodeError):
            pass

    ori.replace('\r\n', '\n')
    item_list = ori.split('\n')
    for item in item_list:
        k, v = item.split(':', maxsplit=1)
        dst.append({k.strip(): v.strip()})
    return dst


def _parser_variables(ori):
    print("variables ori: %s" % ori)
    dst = []
    if isinstance(ori, (list)):
        return ori
    elif isinstance(ori, (str, bytes)):
        try:
            tmp_dst = json.loads(ori)
            if isinstance(tmp_dst, (list)):
                return tmp_dst
            elif isinstance(tmp_dst, (dict)):
                return [tmp_dst]
        except (TypeError, json.decoder.JSONDecodeError):
            pass

    ori.replace('\r\n', '\n')
    item_list = ori.split('\n')
    for item in item_list:
        k, v = item.split(':', maxsplit=1)
        dst.append({k.strip(): v.strip()})
    return dst


def _parser_extract(ori):
    print("extract ori: %s" % ori)
    dst = []

    if isinstance(ori, (list)):
        return ori
    elif isinstance(ori, (str, bytes)):
        try:
            tmp_dst = json.loads(ori)
            if isinstance(tmp_dst, (list)):
                return tmp_dst
            elif isinstance(tmp_dst, (dict)):
                return [tmp_dst]
        except (TypeError, json.decoder.JSONDecodeError):
            pass

    ori.replace('\r\n', '\n')
    item_list = ori.split('\n')
    for item in item_list:
        k, v = item.split(':', maxsplit=1)
        dst.append({k.strip(): v.strip()})
    return dst


def _parser_validate(ori):
    print("validate ori: %s" % ori)
    dst = []

    if isinstance(ori, (list)):
        return ori
    elif isinstance(ori, (str, bytes)):
        try:
            tmp_dst = json.loads(ori)
            if isinstance(tmp_dst, (list)):
                return tmp_dst
            elif isinstance(tmp_dst, (dict)):
                return [tmp_dst]
        except (TypeError, json.decoder.JSONDecodeError):
            pass

    ori.replace('\r\n', '\n')
    item_list = ori.split('\n')
    for item in item_list:
        k, v = item.split(':', maxsplit=1)
        dst.append({k.strip(): v.strip()})
    return dst


def _parser_content(ori):
    print("content ori: %s" % ori)
    dst = {}

    if isinstance(ori, (dict)):
        return ori
    elif isinstance(ori, (str, bytes)):
        try:
            tmp_dst = json.loads(ori)
            if isinstance(tmp_dst, (dict)):
                return tmp_dst
        except (TypeError, json.decoder.JSONDecodeError):
            pass

    ori.replace('\r\n', '\n')
    item_list = ori.split('\n')
    for item in item_list:
        k, v = item.split(':', maxsplit=1)
        dst[k.strip()] = v.strip()
    return dst


def _parser_headers(ori):
    print("headers ori: %s" % ori)
    dst = {}

    if isinstance(ori, (dict)):
        return ori
    elif isinstance(ori, (str, bytes)):
        try:
            tmp_dst = json.loads(ori)
            if isinstance(tmp_dst, (dict)):
                return tmp_dst
        except (TypeError, json.decoder.JSONDecodeError):
            pass

    ori.replace('\r\n', '\n')
    item_list = ori.split('\n')
    for item in item_list:
        k, v = item.split(':', maxsplit=1)
        dst[k.strip()] = v.strip()
    return dst


def bytes_to_str(ori):
    src = copy.deepcopy(ori)
    if isinstance(src, bytes):
        return src.decode('utf-8')
    elif isinstance(src, str):
        return src
    elif isinstance(src, list):
        for id, item in enumerate(src):
            src[id] = bytes_to_str(item)
        return src
    elif isinstance(src, dict):
        for k, v in src.items():
            src[bytes_to_str(k)] = bytes_to_str(v)
        return src
    else:
        return src
