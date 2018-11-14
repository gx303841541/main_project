{
    'success': True,
    'html_report_name': 'report.html',
    'stat': {
        'errors': 0,
        'unexpectedSuccesses': 0,
        'testsRun': 2,
        'expectedFailures': 0,
        'successes': 2,
        'failures': 0,
        'skipped': 0
    },
    'details': [
        {
            'in_out': {
                'out': {},
                'in': {
                    'device_sn': 'dXJ1DuaGdU1lJPk',
                    'os_platform': 'ios',
                    'user_agent': 'iOS/10.3',
                    'xxoo': 'password1',
                    'user_id': 1001,
                    'app_version': '2.8.6',
                    'SECRET_KEY': 'DebugTalk'
                }
            },
            'success': True,
            'name': 'case1',
            'records': [
                {
                    'meta_data': {
                        'request': {
                            'url': 'http://127.0.0.1:5000/api/get-token',
                            'json': {
                                'sign': 'e3420bfe327396b7ecf372b3bcf53f1ab19918eb'
                            },
                            'start_timestamp': 1541139461.494844,
                            'body': Markup('{&#34;sign&#34;: &#34;e3420bfe327396b7ecf372b3bcf53f1ab19918eb&#34;}'),
                            'method': 'POST',
                            'headers': {
                                'Connection': 'keep-alive',
                                'user_agent': 'iOS/10.3',
                                'User-Agent': 'python-requests/2.18.4',
                                'Accept-Encoding': 'gzip, deflate',
                                'Content-Type': 'application/json',
                                'device_sn': 'dXJ1DuaGdU1lJPk',
                                'Accept': '*/*',
                                'app_version': '2.8.6',
                                'os_platform': 'ios',
                                'Content-Length': '52'
                            }
                        },
                        'validators': [
                            {
                                'check_result': 'pass',
                                'check': 'headers.Content-Type',
                                'expect': 'application/json',
                                'comparator': 'eq',
                                'check_value': 'application/json'
                            },
                            {
                                'check_result': 'pass',
                                'check': 'content.success',
                                'expect': True,
                                'comparator': 'eq',
                                'check_value': True
                            },
                            {
                                'check_result': 'pass',
                                'check': 'status_code',
                                'expect': 200,
                                'comparator': 'eq',
                                'check_value': 200
                            }
                        ],
                        'response': {
                            'content_type': 'application/json',
                            'json': {
                                'token': 'n16xceivgzkuR7lv',
                                'success': True
                            },
                            'elapsed_ms': 15.86,
                            'reason': 'OK',
                            'text': '{"success": true, "token": "n16xceivgzkuR7lv"}',
                            'url': 'http://127.0.0.1:5000/api/get-token',
                            'content': Markup('{&#34;success&#34;: true, &#34;token&#34;: &#34;n16xceivgzkuR7lv&#34;}'),
                            'headers': {
                                'Content-Type': 'application/json',
                                    'Content-Length': '46',
                                    'Server': 'Werkzeug/0.14.1 Python/3.5.2',
                                    'Date': 'Fri, 02 Nov 2018 06:17:41 GMT'
                            },
                            'encoding': 'None',
                            'ok': True,
                            'content_size': 46,
                            'status_code': 200,
                            'response_time_ms': 29.42,
                            'cookies': {}
                        }
                    },
                    'attachment': '',
                    'status': 'success',
                    'name': 'get token'
                },
                {
                    'meta_data': {
                        'request': {
                            'url': 'http://127.0.0.1:5000/api/users/1001',
                            'json': {
                                'password': '123456',
                                'name': 'user1'
                            },
                            'start_timestamp': 1541139461.5271647,
                            'body': Markup('{&#34;password&#34;: &#34;123456&#34;, &#34;name&#34;: &#34;user1&#34;}'),
                            'method': 'POST',
                            'headers': {
                                'Connection': 'keep-alive',
                                'User-Agent': 'python-requests/2.18.4',
                                'Accept-Encoding': 'gzip, deflate',
                                'Content-Type': 'application/json',
                                'device_sn': 'dXJ1DuaGdU1lJPk',
                                'Accept': '*/*',
                                'Content-Length': '39',
                                                'token': 'n16xceivgzkuR7lv'
                            }
                        },
                        'validators': [
                            {
                                'check_result': 'pass',
                                'check': 'headers.Content-Type',
                                'expect': 'application/json',
                                'comparator': 'eq',
                                'check_value': 'application/json'
                            }, {
                                'check_result': 'pass',
                                'check': 'content.success',
                                'expect': True,
                                'comparator': 'eq',
                                'check_value': True
                            }, {
                                'check_result': 'pass',
                                'check': 'content.msg',
                                'expect': 'user created successfully.',
                                'comparator': 'eq',
                                'check_value': 'user created successfully.'
                            }, {
                                'check_result': 'pass',
                                'check': 'status_code',
                                'expect': 201,
                                'comparator': 'eq',
                                'check_value': 201
                            }],
                        'response': {
                            'content_type': 'application/json',
                            'json': {
                                'msg': 'user created successfully.',
                                'success': True
                            },
                            'elapsed_ms': 10.015,
                            'reason': 'CREATED',
                            'text': '{"msg": "user created successfully.", "success": true}',
                            'url': 'http://127.0.0.1:5000/api/users/1001',
                            'content': Markup('{&#34;msg&#34;: &#34;user created successfully.&#34;, &#34;success&#34;: true}'),
                            'headers': {
                                    'Content-Type': 'application/json',
                                    'Content-Length': '54',
                                'Server': 'Werkzeug/0.14.1 Python/3.5.2',
                                'Date': 'Fri, 02 Nov 2018 06:17:41 GMT'
                            },
                            'encoding': 'None',
                            'ok': True,
                            'content_size': 54,
                            'status_code': 201,
                                        'response_time_ms': 16.42,
                                        'cookies': {}
                        }
                    },
                    'attachment': '',
                    'status': 'success',
                    'name': 'get user'
                }],
            'stat': {
                'errors': 0,
                'unexpectedSuccesses': 0,
                'testsRun': 2,
                'expectedFailures': 0,
                'successes': 2,
                'failures': 0,
                'skipped': 0
            },
            'time': {
                'start_at': 1541139461.490657,
                'duration': 0.05486035346984863
            },
            'base_url': 'http://127.0.0.1:5000'
        }],
    'time': {
        'start_at': 1541139461.490657,
        'duration': 0.05486035346984863,
        'start_datetime': '2018-11-02 06:17:41'
    },
    'platform': {
        'platform': 'Linux-4.13.0-38-generic-i686-with-Ubuntu-16.04-xenial',
        'httprunner_version': '1.5.14',
        'python_version': 'CPython 3.5.2'
    }
}
