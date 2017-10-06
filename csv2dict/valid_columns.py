#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' validate column headers based on contents of `columns.txt`'''

import argparse
import os
import sys
import re


def validate(array):
    errors = []
    # read valid columns from file
    valid_columns_file_name = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'columns.txt'
    )   
    with open(valid_columns_file_name, 'r') as valid_columns_file:
        valid_columns = valid_columns_file.read().splitlines()
        for member in array:
            if not normalize(member) in valid_columns:
                errors.append('{}'.format(member))
        if len(errors) > 0:
            return errors
        else:
            return True


def normalize(heading):
    '''normalize numbered headings for repeating fields'''
    return re.sub('\d+', '%d', heading)


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('header_name', nargs='+')

    if argv is None:
        argv = parser.parse_args()

    assert(validate(argv.header_name))



# main() idiom for importing into REPL for debugging
if __name__ == "__main__":
    sys.exit(main())


"""
Copyright © 2016, Regents of the University of California
All rights reserved.
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
- Redistributions of source code must retain the above copyright notice,
  this list of conditions and the following disclaimer.
- Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.
- Neither the name of the University of California nor the names of its
  contributors may be used to endorse or promote products derived from this
  software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
"""
