# list_deps
From a makefile list the prerequisites for building a target

The set of makefiles should include no references to absolute file names.

The definition of CFLAGS, CXXFLAGS, etc must include 

$(MM)

For example 

CFLAGS = $(MM) -ggdb -I. $(DDBG)

Change directory to a directory used for a build.
(It is best if this directory cleaned includes only a makefile:

_BUILD_OPTION_MACRO_1_=_abc_

HERE = $(dir $(CURDIR))

include ../Makefile__

and this makefile defines the work

The macro HERE facilitates the use of VPATH but since this introduces maintenance difficulties the use of VPATH is not recommended.

This including of makefiles is not mandatory.
)

Most of the references to sources will be of form for example

../../abc/def.cpp

In the build directory type the command

filt_make.sh # target

where

 Hash is the number of directories up to the root of tyhe build.
 target is the target as supplied to the normal make command.

The result is a list of files relative to the root which suffice to build the target.




