#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Last Updated: Oct. 31, 2022

Initialization function for gatherTweet package

Copyright (C) 2022 Claudia Kann

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
__title__ = 'gatherTweet'
__version__ = '1.0'
__author__ = 'Claudia Kann'
__license__ = 'GPL-3'
__copyright__ = 'Copyright 2022 Claudia Kann'
__contact__ = 'ckann@caltech.edu'


try:
    from .model import TwitterEvent, TwitterKeyPair, TwitterActivity 
    from .pulling_functions import pulling_functions as pull
    from .checking_functions import checking_functions as check
    from .analysis_function import analysis, read
except:
    pass


__all__ = ['TwitterEvent', 'TwitterKeyPair', 
           'TwitterActivity','pull', 'check', 'analysis', 'read']

          