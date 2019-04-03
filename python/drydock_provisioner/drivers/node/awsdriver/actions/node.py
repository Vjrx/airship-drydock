# Copyright 2017 AT&T Intellectual Property.  All other rights reserved.
#
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

import boto3
import logging
import drydock_provisioner.error as errors
from drydock_provisioner.orchestrator.actions.orchestrator import BaseAction



class BaseMaasAction(BaseAction):
    def __init__(self, *args, maas_client=None):
        super().__init__(*args)



class DeployNode(BaseMaasAction):
    """Action to write persistent OS to node."""

    def start(self):
        str_msg = ''
        ec2 = boto3.resource('ec2')

        try:
            site_design = self._load_site_design()

        except Exception as ex:
            self.task.add_status_msg(
                msg="Error loading site design.{0}".format(str(ex)),
                error=True,
                ctx='NA',
                ctx_type='NA')
            self.task.set_status(hd_fields.TaskStatus.Complete)
            self.task.failure()
            self.task.save()
            return

        try:
            aws_conf = site_design.aws_node
            image_id = aws_conf.image_id
            instance_type = aws_conf.instance_type
            subnet_id = aws_conf.subnet_id
            sec_grp = aws_conf.sec_grp
    
            instances = ec2.create_instances(
                ImageId=image_id, InstanceType=instance_type, MaxCount=1, MinCount=1,
                NetworkInterfaces=[
                    {'SubnetId': subnet_id, 'DeviceIndex': 0, 'AssociatePublicIpAddress': True,
                     'Groups': [sec_grp]}])
            instances[0].wait_until_running()

        except Exception as ex:
            self.task.add_status_msg(
                msg="Error creating aws instance.{0}".format(str(ex)),
                error=True,
                ctx='NA',
                ctx_type='NA')

        
        return
