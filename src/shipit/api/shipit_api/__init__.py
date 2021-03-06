# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os

import backend_common
import cli_common.taskcluster
import shipit_api.cli
import shipit_api.config
import shipit_api.models  # noqa
import shipit_api.worker


def create_app(config=None):
    app = backend_common.create_app(
        project_name=shipit_api.config.PROJECT_NAME,
        app_name=shipit_api.config.APP_NAME,
        config=config,
        extensions=[
            'log',
            'security',
            'cors',
            'api',
            'auth',
            'db',
            'pulse',
        ],
    )

    app.notify = cli_common.taskcluster.get_service(
        'notify',
        os.environ.get('TASKCLUSTER_CLIENT_ID', app.config.get('TASKCLUSTER_CLIENT_ID')),
        os.environ.get('TASKCLUSTER_ACCESS_TOKEN', app.config.get('TASKCLUSTER_ACCESS_TOKEN')),
    )

    app.api.register(os.path.join(os.path.dirname(__file__), 'api.yml'))
    app.cli.add_command(shipit_api.worker.cmd, 'worker')

    return app
