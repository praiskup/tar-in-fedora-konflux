Summary: A GNU file archiving program.
Name: tar
Version: 1.15.1
Release: 15
License: GPL
Group: Applications/Archiving
URL: http://www.gnu.org/software/tar/
Source0: ftp://ftp.gnu.org/pub/gnu/tar/tar-%{version}.tar.gz
Source1: ftp://ftp.gnu.org/pub/gnu/tar/tar-%{version}.tar.gz.sig
Source2: tar.1
Patch6: tar-1.14-nolibrt.patch
Patch8: tar-1.14-loneZeroWarning.patch
Patch9: tar-1.15.1-makeCheck.patch
Patch10: tar-1.15.1-gcc4.patch
Patch11: tar-1.15.1-lseek.patch
Patch12: tar-1.15.1-sparseTotals.patch
Patch13: tar-1.15.1-newerOption.patch
Patch14: tar-1.15.1-padCorrectly.patch
Patch15: tar-1.15.1-vfatTruncate.patch
Patch16: tar-1.15.1-heapOverflow.patch
Patch17: tar-1.15.1-hugeSparse.patch

Prereq: info
BuildRequires: autoconf automake gzip
Buildroot: %{_tmppath}/%{name}-%{version}-root

%description
The GNU tar program saves many files together in one archive and can
restore individual files (or all of the files) from that archive. Tar
can also be used to add supplemental files to an archive and to update
or list files in the archive. Tar includes multivolume support,
automatic archive compression/decompression, the ability to perform
remote archives, and the ability to perform incremental and full
backups.

If you want to use tar for remote backups, you also need to install
the rmt package.

%prep
%setup -q
%patch6 -p1 -b .nolibrt
%patch8 -p1 -b .loneZeroWarning
%patch9 -p1 -b .makeCheck
%patch10 -p1 -b .gcc4
%patch11 -p1 -b .lseek
%patch12 -p1 -b .sparseTotals
%patch13 -p1 -b .newerOption
%patch14 -p1 -b .padCorrectly
%patch15 -p1 -b .vfatTruncate
%patch16 -p0 -b .heapOverflow
%patch17 -p1 -b .hugeSparse

%build

%ifos linux
%configure --bindir=/bin --libexecdir=/sbin
make LIBS=-lbsd
%else
%configure
make
%endif

%install
rm -rf $RPM_BUILD_ROOT

%ifos linux
%makeinstall bindir=$RPM_BUILD_ROOT/bin libexecdir=$RPM_BUILD_ROOT/sbin
ln -s tar ${RPM_BUILD_ROOT}/bin/gtar
%else
%makeinstall
%endif

( cd $RPM_BUILD_ROOT
  for dir in ./bin ./sbin .%{_bindir} .%{_libexecdir}
  do
    [ -d $dir ] || continue
    strip $dir/* || :
  done
  gzip -9nf .%{_infodir}/tar.info*
  rm -f .%{_infodir}/dir
)

mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man1
install -c -m 0644 %{SOURCE2} ${RPM_BUILD_ROOT}%{_mandir}/man1

# XXX Nuke unpackaged files.
rm -f ${RPM_BUILD_ROOT}/sbin/rmt

%find_lang %name

%check
rm -f ${RPM_BUILD_ROOT}/test/testsuite
make check

%clean
rm -rf ${RPM_BUILD_ROOT}

%post
/sbin/install-info %{_infodir}/tar.info.gz %{_infodir}/dir

%preun
if [ $1 = 0 ]; then
   /sbin/install-info --delete %{_infodir}/tar.info.gz %{_infodir}/dir
fi

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS ChangeLog ChangeLog.1 NEWS README THANKS TODO
%ifos linux
/bin/tar
/bin/gtar
%{_mandir}/man1/tar.1*
%else
%{_bindir}/*
%{_libexecdir}/*
%{_mandir}/man*/*
%endif

%{_infodir}/tar.info*

%changelog
* Thu Apr 13 2006 Peter Vrabec <pvrabec@redhat.com> 1.15.1-15
- fix segmentation faul introduced with hugeSparse.patch

* Wed Mar 22 2006 Peter Vrabec <pvrabec@redhat.com> 1.15.1-14
- fix problems with extracting large sparse archive members (#185460)

* Fri Feb 17 2006 Peter Vrabec <pvrabec@redhat.com> 1.15.1-13
- fix heap overlfow bug CVE-2006-0300 (#181773)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.15.1-12.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.15.1-12.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Feb 06 2006 Peter Vrabec <pvrabec@redhat.com> 1.15.1-12
- fix extracting sparse files to a filesystem like vfat,
  when ftruncate may fail to grow the size of a file.(#179507)

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Nov 04 2005 Peter Vrabec <pvrabec@redhat.com> 1.15.1-11
- correctly pad archive members that shrunk during archiving (#172373)

* Tue Sep 06 2005 Peter Vrabec <pvrabec@redhat.com> 1.15.1-10
- provide man page (#163709, #54243, #56041)

* Mon Aug 15 2005 Peter Vrabec <pvrabec@redhat.com> 1.15.1-9
- silence newer option (#164902)

* Wed Jul 27 2005 Peter Vrabec <pvrabec@redhat.com> 1.15.1-8
- A file is dumpable if it is sparse and both --sparse
  and --totals are specified (#154882)
 
* Tue Jul 26 2005 Peter Vrabec <pvrabec@redhat.com> 1.15.1-7
- exclude listed02.at from testsuite

* Fri Jul 22 2005 Peter Vrabec <pvrabec@redhat.com> 1.15.1-6
- remove tar-1.14-err.patch, not needed (158743)

* Fri Apr 15 2005 Peter Vrabec <pvrabec@redhat.com> 1.15.1-5
- extract sparse files even if the output fd is not seekable.(#154882)
- (sparse_scan_file): Bugfix. offset had incorrect type.

* Mon Mar 14 2005 Peter Vrabec <pvrabec@redhat.com>
- gcc4 fix (#150993) 1.15.1-4

* Mon Jan 31 2005 Peter Vrabec <pvrabec@redhat.com>
- rebuild 1.15.1-3

* Mon Jan 17 2005 Peter Vrabec <pvrabec@redhat.com>
- fix tests/testsuite

* Fri Jan 07 2005 Peter Vrabec <pvrabec@redhat.com>
- upgrade to 1.15.1

* Mon Oct 11 2004 Peter Vrabec <pvrabec@redhat.com>
- patch to stop issuing lone zero block warnings
- rebuilt

* Mon Oct 11 2004 Peter Vrabec <pvrabec@redhat.com>
- URL added to spec file
- spec file clean up

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Jun  7 2004 Jeff Johnson <jbj@jbj.org> 1.14-1
- upgrade to 1.14.

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun 17 2003 Jeff Johnson <jbj@redhat.com> 1.13.25-13
- rebuilt because of crt breakage on ppc64.
- dump automake15 requirement.

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Fri Nov 29 2002 Tim Powers <timp@redhat.com> 1.13.25-10
- fix broken buildrquires on autoconf253

* Thu Nov  7 2002 Jeff Johnson <jbj@redhat.com> 1.13.25-9
- rebuild from CVS.

* Fri Aug 23 2002 Phil Knirsch <pknirsch@redhat.com> 1.13.25-8
- Included security patch from errata release.

* Mon Jul  1 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.13.25-7
- Fix argv NULL termination (#64869)

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Apr  9 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.13.25-4
- Fix build with autoconf253 (LIBOBJ change; autoconf252 worked)

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Oct 23 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.13.25-2
- Don't include hardlinks to sockets in a tar file (#54827)

* Thu Sep 27 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.13.25-1
- 1.13.25

* Tue Sep 18 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.13.22-1
- Update to 1.13.22, adapt patches

* Mon Aug 27 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.13.19-6
- Fix #52084

* Thu May 17 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.13.19-5
- Fix build with current autoconf (stricter checking on AC_DEFINE)
- Fix segfault when tarring directories without having read permissions
  (#40802)

* Tue Mar  6 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Don't depend on librt.

* Fri Feb 23 2001 Trond Eivind Glomsrød <teg@redhat.com>
- langify

* Thu Feb 22 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix up the man page (#28915)

* Wed Feb 21 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- 1.3.19, nukes -I and fixes up -N
- Add -I back in as an alias to -j with a nice loud warning

* Mon Oct 30 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 1.3.18
- Update man page to reflect changes

* Thu Oct  5 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix the "ignore failed read" option (Bug #8330)

* Mon Sep 25 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- fix hang on tar tvzf - <something.tar.gz, introduced by
  exit code fix (Bug #15448), Patch from Tim Waugh <twaugh@redhat.com>

* Fri Aug 18 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- really fix exit code (Bug #15448)

* Mon Aug  7 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- fix exit code (Bug #15448), patch from Tim Waugh <twaugh@redhat.com>

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jun 19 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- FHSify

* Fri Apr 28 2000 Bill Nottingham <notting@redhat.com>
- fix for ia64

* Wed Feb  9 2000 Bernhard Rosenkränzer <bero@redhat.com>
- Fix the exclude bug (#9201)

* Wed Feb 02 2000 Cristian Gafton <gafton@redhat.com>
- man pages are compressed
- fix description
- fix fnmatch build problems

* Sun Jan  9 2000 Bernhard Rosenkränzer <bero@redhat.com>
- 1.13.17
- remove dotbug patch (fixed in base)
- update download URL

* Fri Jan  7 2000 Bernhard Rosenkränzer <bero@redhat.com>
- Fix a severe bug (tar xf any_package_containing_. would delete the
  current directory)

* Wed Jan  5 2000 Bernhard Rosenkränzer <bero@redhat.com>
- 1.3.16
- unset LINGUAS before running configure

* Tue Nov  9 1999 Bernhard Rosenkränzer <bero@redhat.com>
- 1.13.14
- Update man page to know about -I / --bzip
- Remove dependancy on rmt - tar can be used for anything local
  without it.

* Fri Aug 27 1999 Preston Brown <pbrown@redhat.com>
- upgrade to 1.13.11.

* Wed Aug 18 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.13.9.

* Thu Aug 12 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.13.6.
- support -y --bzip2 options for bzip2 compression (#2415).

* Fri Jul 23 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.13.5.

* Tue Jul 13 1999 Bill Nottingham <notting@redhat.com>
- update to 1.13

* Sat Jun 26 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.12.64014.
- pipe patch corrected for remote tars now merged in.

* Sun Jun 20 1999 Jeff Johnson <jbj@redhat.com>
- update to tar-1.12.64013.
- subtract (and reopen #2415) bzip2 support using -y.
- move gtar to /bin.

* Tue Jun 15 1999 Jeff Johnson <jbj@redhat.com>
- upgrade to tar-1.12.64011 to
-   add bzip2 support (#2415)
-   fix filename bug (#3479)

* Mon Mar 29 1999 Jeff Johnson <jbj@redhat.com>
- fix suspended tar with compression over pipe produces error (#390).

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 8)

* Mon Mar 08 1999 Michael Maher <mike@redhat.com>
- added patch for bad name cache. 
- FIXES BUG 320

* Wed Feb 24 1999 Preston Brown <pbrown@redhat.com>
- Injected new description and group.

* Fri Dec 18 1998 Preston Brown <pbrown@redhat.com>
- bumped spec number for initial rh 6.0 build

* Tue Aug  4 1998 Jeff Johnson <jbj@redhat.com>
- add /usr/bin/gtar symlink (change #421)

* Tue Jul 14 1998 Jeff Johnson <jbj@redhat.com>
- Fiddle bindir/libexecdir to get RH install correct.
- Don't include /sbin/rmt -- use the rmt from dump.
- Turn on nls.

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Oct 16 1997 Donnie Barnes <djb@redhat.com>
- updated from 1.11.8 to 1.12
- various spec file cleanups
- /sbin/install-info support

* Thu Jun 19 1997 Erik Troan <ewt@redhat.com>
- built against glibc

* Thu May 29 1997 Michael Fulbright <msf@redhat.com>
- Fixed to include rmt
