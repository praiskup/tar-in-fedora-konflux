# Makefile for source rpm: tar
# $Id$
NAME := tar
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common
