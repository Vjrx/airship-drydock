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
"""Generic driver for node provisioning."""

import drydock_provisioner.objects.fields as hd_fields
import drydock_provisioner.error as errors

from drydock_provisioner.drivers.driver import ProviderDriver


class NodeDriver(ProviderDriver):

    driver_name = "node_generic"
    driver_key = "node_generic"
    driver_desc = "Generic Node Driver"

    def __init__(self, **kwargs):
        super(NodeDriver, self).__init__(**kwargs)

        self.supported_actions = [
            hd_fields.OrchestratorAction.ValidateNodeServices,
            hd_fields.OrchestratorAction.CreateNetworkTemplate,
            hd_fields.OrchestratorAction.CreateStorageTemplate,
            hd_fields.OrchestratorAction.CreateBootMedia,
            hd_fields.OrchestratorAction.PrepareHardwareConfig,
            hd_fields.OrchestratorAction.IdentifyNode,
            hd_fields.OrchestratorAction.ConfigureHardware,
            hd_fields.OrchestratorAction.InterrogateNode,
            hd_fields.OrchestratorAction.ApplyNodeNetworking,
            hd_fields.OrchestratorAction.ApplyNodeStorage,
            hd_fields.OrchestratorAction.ApplyNodePlatform,
            hd_fields.OrchestratorAction.DeployNode,
            hd_fields.OrchestratorAction.DestroyNode,
            hd_fields.OrchestratorAction.ConfigureUserCredentials,
            hd_fields.OrchestratorAction.ConfigureNodeProvisioner
        ]

    def execute_task(self, task_id):
        task = self.state_manager.get_task(task_id)
        task_action = task.action

        if task_action in self.supported_actions:
            task.success()
            task.set_status(hd_fields.TaskStatus.Complete)
            task.save()
            return
        else:
            raise errors.DriverError("Unsupported action %s for driver %s" %
                                     (task_action, self.driver_desc))

    def get_available_images(self):
        """Return images that can be deployed to nodes by this driver."""

        return []

    def get_available_kernels(self, image):
        """Return a list of kernels that can be specified for deployment.

        :param image: str specifying what image the kernel will be activated
                      within
        """

        return []
