#
# spec file for package avr-libc (Version 1.6.1)
#
# Copyright (c) 2008 SUSE LINUX Products GmbH, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild

Name:           avr-libc
Version:        1.6.7
Release:        %mkrel 2
Url:            http://savannah.nongnu.org/projects/avr-libc
Group:          Development/C
License:        BSD 3-Clause
Summary:        The C Runtime Library for AVR Microcontrollers
Source:         http://savannah.nongnu.org/download/%{name}/%{name}-%{version}.tar.bz2
Source1:        http://savannah.nongnu.org/download/%{name}/%{name}-user-manual-%{version}.tar.bz2
Source2:        http://savannah.nongnu.org/download/%{name}/%{name}-manpages-%{version}.tar.bz2
Source3:        logicp-1.01.tgz
Source4:        avr_isp.pl
Source5:        avr_common.mk
Patch:          contrib-examples.diff
AutoReqProv:    on
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  cross-avr-binutils >= 2.19.51.0.2-1mnb2
BuildRequires:  cross-avr-gcc >= 4.4.1-1mnb2
BuildRequires:  doxygen
BuildRequires:  findutils
Requires:       cross-avr-binutils

%description
The C runtime library for the AVR family of microcontrollers for use
with the GNU toolset (cross-avr-binutils, cross-avr-gcc, uisp, etc.).



Authors:
--------
    Joerg Wunsch <j.gnu@uriah.heep.sax.de>
    Marek Michalkiewicz <marekm@amelek.gda.pl>
    Theodore A. Roth <troth@openavr.org>

%prep
%setup -b 3
%patch -p1
# %ifarch x86_64 ia64 ppc64
# # avr-64bit datatypes fail on 64bit host architectures.
# # it is a bug, isn't it? 2007-01-08, jw
# %patch -p1
# %else
# %if "%(/bin/uname -i)" == "x86_64"
# # we come here with BUILD_DIST=i386 on a x86_64 machine.
# # we need to cover this case too, to make the selftests happy.
# %patch -p1
# %endif
# %endif

%build
export CFLAGS="$RPM_OPT_FLAGS"
export CXXFLAGS="$RPM_OPT_FLAGS"
export PREFIX=%{_prefix}
export PATH=$PREFIX/bin:$PATH
# export NO_BRP_STRIP_DEBUG=true
## silly hack, to be removed when the target is no longer avr-elf but avr.
# for tool in as ar gcc ranlib; do
#   test -f $PREFIX/bin/avr-$tool || \
#   ln -s avr-elf-$tool $PREFIX/bin/avr-$tool
# done
./configure --prefix=$PREFIX --host=avr
make %{?jobs:-j%jobs}

%install
rm -rf $RPM_BUILD_ROOT
export PREFIX=%{_prefix}
export PATH=$PREFIX/bin:$PATH
cp %{S:4} %{S:5} doc/examples
# ./domake DESTDIR=$RPM_BUILD_ROOT install
make DESTDIR=$RPM_BUILD_ROOT install
tar jxvf %{S:1}
mv %{name}-user-manual-%{version} user-manual-%{version}
mkdir -p $RPM_BUILD_ROOT/usr/share/doc/%{name}-%{version}
cp -pr AUTHORS ChangeLog INSTALL LICENSE NEWS user-manual-%{version} $RPM_BUILD_ROOT/usr/share/doc/%{name}-%{version}
tar jxvf %{S:2} -C $RPM_BUILD_ROOT/$PREFIX/share
mv $RPM_BUILD_ROOT/$PREFIX/share/man $RPM_BUILD_ROOT/usr/share/doc/%{name}-%{version}
# gzipped to make http://dist.suse.de/data/i386/lint/avr-libc happy.
find $RPM_BUILD_ROOT/usr/share/doc/%{name}-%{version}/man -type f -print | xargs gzip
#
### selftest ###
cd ../logicp*
## how do we tell the linker that crt*.o is at a nonstandard location?
ln -sf $RPM_BUILD_ROOT/$PREFIX/avr/lib/crttn*.o .
ln -sf $RPM_BUILD_ROOT/$PREFIX/avr/lib/avr?/crtm*.o .
make test CFLAGS="-Wall -g -Os -mint8 -I$RPM_BUILD_ROOT/$PREFIX/avr/include/ -L$RPM_BUILD_ROOT/$PREFIX/avr/lib/avr4" CPU=mega8
make test CFLAGS="-Wall -g -Os -mint8 -I$RPM_BUILD_ROOT/$PREFIX/avr/include/ -L$RPM_BUILD_ROOT/$PREFIX/avr/lib/avr4" CPU=mega48
make test CFLAGS="-Wall -g -Os -mint8 -I$RPM_BUILD_ROOT/$PREFIX/avr/include/ -L$RPM_BUILD_ROOT/$PREFIX/avr/lib"      CPU=tiny2313

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, root)
%doc /usr/share/doc/%{name}-%{version}
%{_bindir}/avr-man
%{_prefix}/avr/lib/*
%{_prefix}/avr/include
# %doc /usr/share/man/man?/*.*



%changelog
* Tue Dec 29 2009 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 1.6.7-1mdv2010.1
+ Revision: 483257
- Updated to version 1.6.7 (and rediffed contrib-examples.diff).

* Tue Nov 17 2009 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 1.6.1-7mdv2010.1
+ Revision: 466898
- Fixed group/release tags.
- BuildRequires for latest versions of cross-avr-binutils and
  cross-avr-gcc
- Fix requires for latest cross-avr-gcc
- Dont hard require avr-programmer, may be later import it and add a
  Suggests?
- Fix prefix for avr toolchain in Mandriva.
- Install documentation in common location at
  /usr/share/doc/avr-libc-<version>

  + Marcelo Ricardo Leitner <mrl@mandriva.com>
    - import avr-libc


* Wed Jan 30 2008 jw@suse.de
- update to 1.6.1
  * The fplib/math library is completely rewritten.
  * Functions of numbers to ascii conversion are completely rewritten.
  * Test suite is added to the Avr-libc project.
  * A few new util's headers: util/atomic.h, util/setbaud.h.
  * Many new devices added, many revised.
* Sat Oct 13 2007 bwalle@suse.de
- update to 1.4.6
  o Exclude 64-bit types for -mint8 (obsoletes no64bit_int.patch)
  o varios bugfixes (upstream #18115, #18385, #18509, #18662,
    [#18686], #18688, #18726, #18899, #18903, #18915, #19009, #19050,
    [#19060], #19134, #19135, #19280, #19281, #19445, #19495, #19650,
    [#19666] #19841)
  o new devices: AT90USB82, AT90USB162, ATmega325P, ATmega3250P,
    ATmega329P, ATmega3290P, AT90PWM1, ATmega8HVA, ATmega16HVA
  o The "largedemo" has been ported to the ATtiny2313.
  o Integrate a copy of the license file into the documentation.
  o Include an alphabetical index of all globals
  o Added 'avr25' architecture.
  o new functions (memchr_P, memcmp_P, memmem, memmem_P, memrchr,
    memrchr_P, strcasestr, strcasestr_P, strchrnul, strchrnul_P,
    strchr_P, strcspn, strcspn_P, strpbrk, strpbrk_P, strrchr_P,
    strsep_P, strspn, strspn_P)
  o Optimized functions (atoi, atol, strchr, strcmp, strcmp_P,
    strlwr, strrev, strsep, strstr, strstr_P, strupr)
* Thu Apr  5 2007 jw@suse.de
- gzipped manpages to make rpmlint happy.
  user-manual moved *into* /usr/share/doc/packages/avr-libc.
* Mon Jan 15 2007 jw@suse.de
- 64bit datatypes on 64bit hosts only fail with -mint8
  Now properly ifdefed.
* Tue Jan  9 2007 jw@suse.de
- update to 1.4.5
  ATmega165P/169P support. Fixes to the HD44780 driver.
  Power Management API. New "asmdemo" example.
  sleep.h: Fix the entry for the ATtiny2313.
  new devices: ATmega2560, ATmega2561.
  fp_split.S: Pop 3 bytes for avr6
  Bugs fixed: 15512 16125 16411 16434 16441
    16868 17068 17470 17551 17591 17608
- make test now tests 3 CPUs
* Tue Jan  9 2007 jw@suse.de
- compiling and linking my logicp application
  as a simple selftest.
- avr-64bit datatypes fail on 64bit hosts.
* Tue May 30 2006 jw@suse.de
- update to 1.4.4
  added /opt/cross/share/man/man3/* and /opt/cross/share/doc symlink
* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Tue Jan 10 2006 jw@suse.de
- update to 1.4.2
* Wed Nov 23 2005 jw@suse.de
- upstreamed patches removed.
- update to 1.4.0
* Wed Oct  5 2005 dmueller@suse.de
- add norootforbuild
* Wed Aug 17 2005 jw@suse.de
- update to 1.2.5, fixes many things for atmega48
  e.g. [#105226].
* Tue May 17 2005 jw@suse.de
- removed dependency on uisp.
* Tue May 10 2005 jw@suse.de
- initial version: avr-libc-1.2.3
