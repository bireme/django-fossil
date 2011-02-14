# -*- encoding: utf-8 -*-

# django-fossil: immutable audit trails for interrelated model instances
#
# Copyright (C) 2010 BIREME/PAHO/WHO
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 2.1 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful, 
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

VERSION = (0, 7, 'stable')

def get_version():
    return '%d.%d-%s'%VERSION

__author__ = 'OpenTrials team (Marinho Brandao, Luciano Ramalho and Rafael Soares)'
#__date__ = '$Date: 2008-07-26 14:04:51 -0300 (Ter, 26 Fev 2008) $'[7:-2]
__license__ = 'GNU Lesser General Public License (LGPL)'
__url__ = 'http://reddes.bvsalud.org/projects/clinical-trials/browser/sandbox/django-fossil'
__version__ = get_version()

