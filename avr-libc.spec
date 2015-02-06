#
# spec file for package avr-libc (Version 1.6.1)
#
# Copyright (c) 2008 SUSE LINUX Products GmbH, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

Name:		avr-libc
Version:	1.8.0
Release:	2
Url:		http://savannah.nongnu.org/projects/avr-libc
Group:		Development/C
License:	BSD
Summary:	The C Runtime Library for AVR Microcontrollers
Source0:	http://savannah.nongnu.org/download/%{name}/%{name}-%{version}.tar.bz2
Source1:	http://savannah.nongnu.org/download/%{name}/%{name}-user-manual-%{version}.tar.bz2
Source2:	http://savannah.nongnu.org/download/%{name}/%{name}-manpages-%{version}.tar.bz2
Source3:	logicp-1.01.tgz
Source4:	%{name}.rpmlintrc
Patch100:	logicp-1.01-mdv-replace-deprecated-vector-names.patch
AutoReqProv:	on
BuildRequires:	cross-avr-binutils >= 2.21.1
BuildRequires:	cross-avr-gcc >= 4.6.1
BuildRequires:	doxygen
BuildRequires:	findutils
BuildRequires:	dos2unix
Requires:	cross-avr-binutils cross-avr-gcc
BuildArch:	noarch

%description
The C runtime library for the AVR family of microcontrollers for use
with the GNU toolset (cross-avr-binutils, cross-avr-gcc, uisp, etc.).


Authors:
--------
    Joerg Wunsch <j.gnu@uriah.heep.sax.de>
    Marek Michalkiewicz <marekm@amelek.gda.pl>
    Theodore A. Roth <troth@openavr.org>

%prep
%setup -q -b 3
dos2unix doc/examples/twitest/twitest.c
pushd ../logicp-1.01
%patch100 -p1
popd

%build
export CFLAGS="%{optflags}"
export CXXFLAGS="%{optflags}"
export PREFIX=%{_prefix}
export PATH=%{_prefix}/bin:$PATH
./configure --prefix=%{_prefix} --host=avr
make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
export PREFIX=%{_prefix}
export PATH=%{_prefix}/bin:$PATH
# ./domake DESTDIR=%%{buildroot} install
make DESTDIR=%{buildroot} install
tar jxvf %{S:1}
mv %{name}-user-manual-%{version} user-manual-%{version}
mkdir -p %{buildroot}/usr/share/doc/%{name}-%{version}
cp -pr AUTHORS ChangeLog LICENSE NEWS user-manual-%{version} %{buildroot}/usr/share/doc/%{name}-%{version}
cat >> %{buildroot}/usr/share/doc/%{name}-%{version}/00_index.html <<EOF
<head><meta http-equiv="Refresh" content="0; user-manual-%{version}/pages.html"></head>
<a href="user-manual-%{version}/pages.html">user-manual-%{version}/pages.html</a>
EOF
tar jxvf %{S:2} -C %{buildroot}/%{_prefix}/share
mv %{buildroot}/%{_prefix}/share/man %{buildroot}/usr/share/doc/%{name}-%{version}
find %{buildroot}/usr/share/doc/%{name}-%{version}/man -type f -print | xargs xz

%check
### selftest ###
cd ../logicp*
## how do we tell the linker that crt*.o is at a nonstandard location?
ln -sf %{buildroot}/%{_prefix}/avr/lib/crttn*.o .
ln -sf %{buildroot}/%{_prefix}/avr/lib/avr?/crtm*.o .
make test CFLAGS="-Wall -g -Os -mint8 -I%{buildroot}/%{_prefix}/avr/include/ -L%{buildroot}/%{_prefix}/avr/lib/avr4" CPU=mega8
make test CFLAGS="-Wall -g -Os -mint8 -I%{buildroot}/%{_prefix}/avr/include/ -L%{buildroot}/%{_prefix}/avr/lib/avr4" CPU=mega48
make test CFLAGS="-Wall -g -Os -mint8 -I%{buildroot}/%{_prefix}/avr/include/ -L%{buildroot}/%{_prefix}/avr/lib"      CPU=tiny2313

%files
%defattr (-, root, root)
%doc /usr/share/doc/%{name}-%{version}
%{_bindir}/avr-man
%{_prefix}/avr/lib/*
%{_prefix}/avr/include


%changelog
* Thu Jan 12 2012 Dmitry Mikhirev <dmikhirev@mandriva.org> 1.8.0-1
+ Revision: 760371
- new version 1.8.0

* Wed Oct 19 2011 Andrey Smirnov <asmirnov@mandriva.org> 1.7.1-1
+ Revision: 705388
- Updated to 1.7.1

  + Oden Eriksson <oeriksson@mandriva.com>
    - rebuild

* Thu Apr 01 2010 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 1.6.8-1mdv2010.1
+ Revision: 530555
- Updated to version 1.6.8
- Revert bogus changes from previous avr-libc commit.

  + Yvan T. <yvanttt@mandriva.org>
    - Rebuild package with gcc-avr 4.4.3 to avoid link error when cross compiling
      Also remove dependency to avr-gcc.
      Instead avr-gcc now depend on this package

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
