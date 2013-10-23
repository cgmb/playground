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
	conf.env.CXXFLAGS = ['-std=c++11', '-Og', '-Wall']
	conf.load('compiler_cxx')

def build(bld):
	bld.stlib(
		features='cxx cxxstlib',
		source='primes.cxx',
		include='primes.h',
		target='primes',
	)

	bld.program(
		features='cxx cxxprogram',
		use='primes',
		source='main.cxx',
		target='isprime',
		install_path='.',
	)
