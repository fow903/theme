###################################################################################
# 
#    Copyright (C) 2018 MuK IT GmbH
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
###################################################################################

import os
import re
import io
import sys
import base64
import shutil
import urllib
import logging
import tempfile
import mimetypes
import unicodedata

from odoo.tools.mimetypes import guess_mimetype

_logger = logging.getLogger(__name__)

#----------------------------------------------------------
# File Helper
#----------------------------------------------------------

def slugify(value):
    value = str(unicodedata.normalize('NFKD', value))
    if sys.version_info < (3,):
        value = str(value.encode('ascii', 'ignore'))
    value = str(re.sub('[^\w\s-]', '', value).strip().lower())
    value = str(re.sub('[-\s]+', '-', value))
    return value

def check_name(name):
    tmp_dir = tempfile.mkdtemp()
    try:
        open(os.path.join(tmp_dir, name), 'a').close()
    except IOError:
        return False
    finally:
        shutil.rmtree(tmp_dir)
    return True

def compute_name(name, suffix, escape_suffix):
    if escape_suffix:
        name, extension = os.path.splitext(name)
        return "%s(%s)%s" % (name, suffix, extension)
    else:
        return "%s(%s)" % (name, suffix)

def unique_name(name, names, escape_suffix=False):
    if not name in names:
        return name
    else:
        suffix = 1
        name = compute_name(name, suffix, escape_suffix)
        while name in names:
            suffix += 1
            name = compute_name(name, suffix, escape_suffix)
        return name 

def unique_files(files):
    ufiles = []
    unames = []
    for file in files:
        uname = unique_name(file[0], unames, escape_suffix=True)
        ufiles.append((uname, file[1]))
        unames.append(uname)
    return ufiles  

def guess_extension(filename=None, mimetype=None, binary=None):
    extension = filename and os.path.splitext(filename)[1][1:].strip().lower()
    if not extension and mimetype:
        extension = mimetypes.guess_extension(mimetype)[1:].strip().lower()
    if not extension and binary:
        mimetype = guess_mimetype(binary, default="")
        extension = mimetypes.guess_extension(mimetype)[1:].strip().lower()
    return extension