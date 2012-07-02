#!/usr/bin/python
# encoding: utf-8
# -*- encoding: utf-8 -*-


def handle_mongo_result(result):
    """handle async mongo with tornado.gen.Task Result"""
    args, kwargs = result
    if kwargs.get('error'):
        raise Exception(kwargs['error'])
    return args[0]

