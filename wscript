#! /usr/bin/env python
# encoding: utf-8

# the following two variables are used by the target "waf dist"
VERSION='0.0.1'
APPNAME='isprime'

# these variables are mandatory ('/' are converted automatically)
top = '.'
out = '.build'

def check_version(minimum, version):
	assert len(minimum) == 3
	return (
		version[0] > minimum[0] or
		version[0] == minimum[0] and version[1] > minimum[1] or
		version[0] == minimum[0] and version[1] == minimum[1] and version[2] >= minimum[2]
		)

def options(opt):
	opt.load('compiler_cxx')

def configure(conf):
	conf.load('compiler_cxx')

	conf.env.CXXFLAGS = ['-Wall']
	if conf.env.CXX_NAME == 'gcc':
		if check_version('470', conf.env.CC_VERSION):
			conf.env.CXXFLAGS.append('-std=c++11')
		else: 
			conf.env.CXXFLAGS.append('-std=c++0x')
		 
		if check_version('480', conf.env.CC_VERSION):
			conf.env.CXXFLAGS.append('-Og')
		else:
			conf.env.CXXFLAGS.append('-O2')

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
