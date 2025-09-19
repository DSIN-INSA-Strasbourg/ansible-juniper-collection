#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ansible-juniper-collection: Ansible collection to configure and deploy firmware on
# Juniper EX switches
# Copyright (C) 2025 INSA Strasbourg
#
# This file is part of ansible-juniper-collection.
#
# ansible-juniper-collection is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ansible-juniper-collection is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ansible-juniper-collection. If not, see <https://www.gnu.org/licenses/>.

from ansible.errors import AnsibleFilterError


class FilterModule(object):
    def filters(self):
        return {
            "combine_trusted_settings": self.combine_trusted_settings,
        }

    # Combine specified dict to list items whose trusted attribute is true
    def combine_trusted_settings(self, netiflist, trusted_settings):
        res = []

        try:
            for netif in netiflist:
                if 'trusted' in netif and netif['trusted'] is True:
                    res.append(trusted_settings | netif)
                else:
                    res.append(netif)
            return res
        except Exception as e:
            raise AnsibleFilterError(str(e))
