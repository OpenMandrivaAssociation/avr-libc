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
Release:        %mkrel 1
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
Requires:       cross-avr-binutils cross-avr-gcc

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

