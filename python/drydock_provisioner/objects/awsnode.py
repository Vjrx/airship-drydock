#Copyright 2017 AT&T Intellectual Property.  All other rights reserved.
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
"""Models representing host profiles and constituent parts."""

from copy import deepcopy

import oslo_versionedobjects.fields as obj_fields
import drydock_provisioner.objects as objects
import drydock_provisioner.objects.base as base
import drydock_provisioner.objects.fields as hd_fields


@base.DrydockObjectRegistry.register
class AwsNode(base.DrydockPersistentObject, base.DrydockObject):

    VERSION = '1.0'

    fields = {
        'image_id':
        obj_fields.StringField(nullable=True),
        'instance_type':
        obj_fields.StringField(nullable=True),
        'subnet_id':
        obj_fields.StringField(nullable=True),
        'sec_grp':
        obj_fields.StringField(nullable=True),
    }

    def __init__(self, **kwargs):
        super(AwsNode, self).__init__(**kwargs)

    def get_image_id(self):
        return self.image_id
    
    def get_instance_type(self):
        return self.instance_type

    def get_subnet_id(self):
        return self.subnet_id

    def get_sec_grp(self):
        return self.sec_grp



    # HostProfile is keyed by name
    def get_id(self):
        return self.get_name()

    def get_name(self):
        return self.name


@base.DrydockObjectRegistry.register
class AwsNodeList(base.DrydockObjectListBase, base.DrydockObject):

    VERSION = '1.0'

    fields = {'objects': obj_fields.ListOfObjectsField('AwsNode')}
