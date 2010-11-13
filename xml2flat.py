#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

# xml2flat.py - xml2flat - flatten XML documents into CSV-files
#
# Copyright (C) 2010, Stefan Schramm <mail@stefanschramm.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import libxml2
import sys

def parse_cmdline_arguments(args):

    # defaults
    filename = None
    delimiter = "\t"
    loop_expression = None
    column_expressions = []
    namespaces = []
    stop_if_node_not_found = False

    # parsing and syntax check
    args = iter(args)
    while True:
        try:
            arg = args.next()
        except StopIteration:
            break
        if arg == '-f':
            # filename
            try:
                filename = args.next()
                continue
            except StopIteration:
                sys.exit("Missing argument for -f (filename)")
        if arg == '-d':
            # delimiter
            try:
                delimiter = args.next()
                continue
            except StopIteration:
                sys.exit("Missing argument for -d (field delimiter)")
        if arg == '-n':
            # namespace (prefix and url)
            try:
                namespaces.append([args.next(), args.next()])
                continue
            except StopIteration:
                sys.exit("Missing argument for -n (namespace prefix) (namespace url)")
        if arg == '-s':
            # stop if column node not found
            stop_if_node_not_found = True
            continue
        if loop_expression == None:
            loop_expression = arg
            continue
        else:
            column_expressions.append(arg)
            continue
        sys.exit("Unknown option: " + arg)

    if loop_expression == None:
        sys.exit("The loop expression is required.")

    if len(column_expressions) == 0:
        sys.exit("At least one column expression is required.")

    return filename, delimiter, loop_expression, column_expressions, namespaces, stop_if_node_not_found


if __name__ == "__main__":

    try:
        # parse command line options
        (filename, delimiter, loop_expression, column_expressions, namespaces, stop_if_node_not_found) = parse_cmdline_arguments(sys.argv[1:])

        # determine data source (file or stdin)
        if filename != None and filename != "-":
            doc = libxml2.parseFile(filename)
        else:
            doc = libxml2.parseDoc(sys.stdin.read())

        context = doc.xpathNewContext()
        for namespace in namespaces:
            context.xpathRegisterNs(namespace[0], namespace[1])
        try:
            nodelist = context.xpathEval(loop_expression)
        except libxml2.xpathError:
            sys.exit("XPath syntax error in loop expression.")
        for node in nodelist:
            context.setContextNode(node)
            fields = []
            for column_expression in column_expressions:
                try:
                    column_nodelist = context.xpathEval(column_expression)
                except libxml2.xpathError:
                    sys.exit("XPath syntax error in column expression.")
                try:
                    fields.append(column_nodelist[0].content)
                except IndexError:
                    if stop_if_node_not_found:
                        sys.exit("Column node not found. XPath expression was: \"" + column_expression + "\". Remove -s option to get an empty string for this field.")
                    else:
                        fields.append("")
            print delimiter.join(fields)
        doc.freeDoc()
        context.xpathFreeContext()

    except KeyboardInterrupt:
        sys.exit("Aborted by user")

