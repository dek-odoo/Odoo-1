# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: ElvenStudio
#    Copyright 2015 elvenstudio.it
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
 'name': 'Picking 2binvoice after invoice cancel FIX',
 'license': 'AGPL-3',
 'version': '0.0.2',
 'category': 'Account',
 'website': 'https://github.com/ElvenStudio/Odoo',
 'summary': "Restore picking after invoice cancel",
 'description': """
    This module will restore the picking state from 'invoiced' to '2binvoiced' after invoice cancel.
""",
 'author': "ElvenStudio",
 'license': 'AGPL-3',
 'website': 'http://www.elvenstudio.it',

 'images': ['images/elvenstudio.png'],

 'depends': [
     'stock_account'
 ],

 'data': [],

 'installable': True,
 'application': False,
 }
