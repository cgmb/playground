#! /usr/bin/env python
# encoding: utf-8

# the following two variables are used by the target "waf dist"
VERSION='0.0.1'
APPNAME='isprime'

# these variables are mandatory ('/' are converted automatically)
top = '.'
out = '.build'

def options(opt):
	opt.load('compiler_cxx')

def configure(conf):
	conf.load('compiler_cxx')

def build(bld):
	bld.program(
		features='cxx cxxprogram', 
		source='main.cxx',
		target='isprime',
		install_path='.',
		cxxflags=['-Og', '-Wall'],
	)
