# Copyright 2017 AT&T Intellectual Property.  All other rights reserved.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Task driver for completing node provisioning with Canonical MaaS 2.2+."""

import logging
import uuid
import concurrent.futures

from oslo_config import cfg

import drydock_provisioner.error as errors
import drydock_provisioner.objects.fields as hd_fields
import drydock_provisioner.config as config

from drydock_provisioner.drivers.node.driver import NodeDriver
from drydock_provisioner.drivers.node.maasdriver.api_client import MaasRequestFactory
from drydock_provisioner.drivers.node.maasdriver.models.boot_resource import BootResources

from drydock_provisioner.drivers.node.awsdriver.actions.node import DeployNode


class AwsNodeDriver(NodeDriver):
    awsdriver_options = [
        cfg.StrOpt(
            'aws access key', help='The API key for accessing Aws',
            secret=True),
        cfg.StrOpt('aws secret access key', help='The API key for accessing Aws API'),
        cfg.IntOpt(
            'poll_interval',
            default=10,
            help='Polling interval for querying aws status in seconds'),
                          ]

    driver_name = 'awsdriver'
    driver_key = 'awsdriver'
    driver_desc = 'AWS Node Provisioning Driver'

    action_class_map = {
        hd_fields.OrchestratorAction.DeployNode:
        DeployNode,
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        cfg.CONF.register_opts(
           AwsNodeDriver.awsdriver_options, group=AwsNodeDriver.driver_key)

        self.logger = logging.getLogger(
            cfg.CONF.logging.nodedriver_logger_name)

    def execute_task(self, task_id):
        # actions that should be threaded for execution
        threaded_actions = [
            hd_fields.OrchestratorAction.DeployNode
        ]

        action_timeouts = {
            hd_fields.OrchestratorAction.DeployNode:
            config.config_mgr.conf.timeouts.deploy_node,
        }

        task = self.state_manager.get_task(task_id)

        if task is None:
            raise errors.DriverError("Invalid task %s" % (task_id))

        if task.action not in self.supported_actions:
            raise errors.DriverError("Driver %s doesn't support task action %s"
                                     % (self.driver_desc, task.action))

        task.set_status(hd_fields.TaskStatus.Running)
        task.save()

        if task.action in threaded_actions:
            if task.retry > 0:
                msg = "Retrying task %s on previous failed entities." % str(
                    task.get_id())
                task.add_status_msg(
                    msg=msg,
                    error=False,
                    ctx=str(task.get_id()),
                    ctx_type='task')

            with concurrent.futures.ThreadPoolExecutor(max_workers=16) as e:
                subtask_futures = dict()
                subtask = self.orchestrator.create_task(
                        design_ref=task.design_ref,
                        action=task.action,
                        retry=task.retry)
                task.register_subtask(subtask)
                

                action = self.action_class_map.get(task.action, None)(
                        subtask,
                        self.orchestrator,
                        self.state_manager)
                subtask_futures[subtask.get_id().bytes] = e.submit(
                        action.start)


        task.set_status(hd_fields.TaskStatus.Complete)
        task.save()

        return
