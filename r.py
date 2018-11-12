{
    'platform': {
        'httprunner_version': '1.5.14',
        'python_version': 'CPython 3.5.2',
        'platform': 'Linux-4.13.0-38-generic-i686-with-Ubuntu-16.04-xenial'
    },
    'stat': {
        'failures': 1,
        'skipped': 0,
        'expectedFailures': 0,
        'testsRun': 2,
        'errors': 0,
        'successes': 1,
        'unexpectedSuccesses': 0
    },
    'success': False,
    'details': [
        {
            'base_url': 'http://127.0.0.1:5000',
            'success': False,
            'time': {
                'duration': 0.07493185997009277,
                'start_at': 1541307744.7349083
            },
            'name': 'case3',
            'in_out': {
                    'in': {
                        'user_agent': 'iOS/10.3',
                        'device_sn': 'ByW3gmKuirsPisp',
                        'SECRET_KEY': 'DebugTalk',
                        'app_version': '2.8.6',
                        'os_platform': 'ios',
                        'user_id': 1001,
                        'xxoo': 'password1'
                    },
                'out': {}
            },
            'stat': {
                'failures': 1,
                'skipped': 0,
                'expectedFailures': 0,
                'errors': 0,
                'testsRun': 2,
                'successes': 1,
                'unexpectedSuccesses': 0
            },
            'records': [
                {
                    'name': 'get token',
                    'attachment': '',
                    'meta_data': {
                        'validators': [{
                            'comparator': 'eq',
                            'check_value': 200,
                            'expect': 200,
                            'check': 'status_code',
                            'check_result': 'pass'
                        }, {
                            'comparator': 'eq',
                            'check_value': True,
                            'expect': True,
                            'check': 'content.success',
                            'check_result': 'pass'
                        }, {
                            'comparator': 'eq',
                            'check_value': 'application/json',
                            'expect': 'application/json',
                            'check': 'headers.Content-Type',
                            'check_result': 'pass'
                        }],
                        'response': {
                            'reason': 'OK',
                            'content': b '{"success": true, "token": "J413bOGu7gARcGl4"}',
                            'headers': {
                                'Server': 'Werkzeug/0.14.1 Python/3.5.2',
                                'Content-Length': '46',
                                'Content-Type': 'application/json',
                                'Date': 'Sun, 04 Nov 2018 05:02:24 GMT'
                            },
                            'encoding': None,
                            'response_time_ms': 28.46,
                            'content_size': 46,
                            'json': {
                                'token': 'J413bOGu7gARcGl4',
                                'success': True
                            },
                            'status_code': 200,
                            'url': 'http://127.0.0.1:5000/api/get-token',
                            'ok': True,
                            'text': '{"success": true, "token": "J413bOGu7gARcGl4"}',
                            'elapsed_ms': 18.684,
                            'cookies': {},
                            'content_type': 'application/json'
                        },
                        'request': {
                            'start_timestamp': 1541307744.735791,
                            'url': 'http://127.0.0.1:5000/api/get-token',
                            'method': 'POST',
                            'headers': {
                                'user_agent': 'iOS/10.3',
                                'Accept': '*/*',
                                'device_sn': 'ByW3gmKuirsPisp',
                                'Content-Type': 'application/json',
                                'User-Agent': 'python-requests/2.18.4',
                                'os_platform': 'ios',
                                'Accept-Encoding': 'gzip, deflate',
                                'Connection': 'keep-alive',
                                'Content-Length': '52',
                                'app_version': '2.8.6'
                            },
                            'json': {
                                'sign': 'e4deb271a738983caec08b2f30443648952f8aec'
                            },
                            'body': b '{"sign": "e4deb271a738983caec08b2f30443648952f8aec"}'
                        }
                    },
                    'status': 'success'
                },
                {
                    'name': 'get user',
                    'attachment': 'Traceback (most recent call last):\n  File "/home/kobe/main_project/backend/httprunner/api.py", line 59, in test\n    test_runner.run_test(teststep_dict)\nbackend.httprunner.exceptions.ValidationFailure: validate: status_code equals 201(int)\t==> fail\n500(int) equals 201(int)\nvalidate: content.success equals True(bool)\t==> fail\nFalse(bool) equals True(bool)\nvalidate: content.msg equals user created successfully.(str)\t==> fail\nuser already existed.(str) equals user created successfully.(str)\n\nDuring handling of the above exception, another exception occurred:\n\nTraceback (most recent call last):\n  File "/home/kobe/main_project/backend/httprunner/api.py", line 61, in test\n    self.fail(str(ex))\nAssertionError: validate: status_code equals 201(int)\t==> fail\n500(int) equals 201(int)\nvalidate: content.success equals True(bool)\t==> fail\nFalse(bool) equals True(bool)\nvalidate: content.msg equals user created successfully.(str)\t==> fail\nuser already existed.(str) equals user created successfully.(str)\n',
                    'meta_data': {
                        'validators': [{
                            'comparator': 'eq',
                            'check_value': 200,
                            'expect': 200,
                            'check': 'status_code',
                            'check_result': 'pass'
                        },
                            {
                            'comparator': 'eq',
                            'check_value': True,
                            'expect': True,
                            'check': 'content.success',
                            'check_result': 'pass'
                        }, {
                            'comparator': 'eq',
                            'check_value': 'application/json',
                            'expect': 'application/json',
                            'check': 'headers.Content-Type',
                            'check_result': 'pass'
                        }],
                        'response': {
                            'reason': 'INTERNAL SERVER ERROR',
                            'content': b '{"success": false, "msg": "user already existed."}',
                            'headers': {
                                'Server': 'Werkzeug/0.14.1 Python/3.5.2',
                                'Content-Length': '50',
                                'Content-Type': 'application/json',
                                'Date': 'Sun, 04 Nov 2018 05:02:24 GMT'
                            },
                            'encoding': None,
                            'response_time_ms': 27.95,
                            'content_size': 50,
                            'json': {
                                'success': False,
                                'msg': 'user already existed.'
                            },
                            'status_code': 500,
                            'url': 'http://127.0.0.1:5000/api/users/1001',
                            'ok': False,
                            'text': '{"success": false, "msg": "user already existed."}',
                            'elapsed_ms': 19.382,
                            'cookies': {},
                            'content_type': 'application/json'
                        },
                        'request': {
                            'start_timestamp': 1541307744.772001,
                            'url': 'http://127.0.0.1:5000/api/users/1001',
                            'method': 'POST',
                            'headers': {
                                'Accept': '*/*',
                                'token': 'J413bOGu7gARcGl4',
                                'device_sn': 'ByW3gmKuirsPisp',
                                'Content-Type': 'application/json',
                                'User-Agent': 'python-requests/2.18.4',
                                'Accept-Encoding': 'gzip, deflate',
                                'Connection': 'keep-alive',
                                'Content-Length': '39'
                            },
                            'json': {
                                'name': 'user1',
                                'password': '123456'
                            },
                            'body': b '{"name": "user1", "password": "123456"}'
                        }
                    },
                    'status': 'failure'
                }]
        }
    ],
    'time': {
        'duration': 0.07493185997009277,
        'start_at': 1541307744.7349083
    }
}
