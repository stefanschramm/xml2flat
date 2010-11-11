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

# TODO:
# - input file or stdin
# - register namespaces by cmdline argument (or remove namespaces from document root node?)
# - catch other exceptions (xpath syntax error, broken document, etc.)
# - what, if a know wasn't found (xpath returned empty list) - empty string? - exception?

delimiter = "\t"

#RSS:
#loop_expression = "//rss:item"
#namespaces = [["rss", "http://purl.org/rss/1.0/"]]
#column_expressions = ["rss:link", "rss:title"]

#ATOM:
namespaces = [["atom", "http://www.w3.org/2005/Atom"]]
loop_expression = "//atom:entry"
column_expressions = ["atom:link/@href", "atom:title"]
#example data: http://www.heise.de/newsticker/heise-atom.xml

doc = libxml2.parseFile("test.xml")
context = doc.xpathNewContext()
for namespace in namespaces:
	context.xpathRegisterNs(namespace[0], namespace[1])
nodelist = context.xpathEval(loop_expression)
for node in nodelist:
	context.setContextNode(node)
	fields = []
	for column_expression in column_expressions:
		column_nodelist = context.xpathEval(column_expression)
		try:
			fields.append(column_nodelist[0].content)
		except IndexError:
			# node wasn't found - place empty string # TODO: make option
			fields.append("")
	print delimiter.join(fields)
doc.freeDoc()
context.xpathFreeContext()

