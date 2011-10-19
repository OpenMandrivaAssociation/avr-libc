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

Name:		avr-libc
Version:	1.7.1
Release:	%mkrel 1
Url:		http://savannah.nongnu.org/projects/avr-libc
Group:		Development/C
License:	BSD 3-Clause
Summary:	The C Runtime Library for AVR Microcontrollers
Source0:	http://savannah.nongnu.org/download/%{name}/%{name}-%{version}.tar.bz2
Source1:	http://savannah.nongnu.org/download/%{name}/%{name}-user-manual-%{version}.tar.bz2
Source2:	http://savannah.nongnu.org/download/%{name}/%{name}-manpages-%{version}.tar.bz2
Source3:	logicp-1.01.tgz
Patch0:		avr-libc-1.7.1-progmem.patch
Patch1:		savannah32698-power.patch
AutoReqProv:	on
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
BuildRequires:	cross-avr-binutils >= 2.21.1
BuildRequires:	cross-avr-gcc >= 4.6.1
BuildRequires:	doxygen
BuildRequires:	findutils
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
%patch0 -p1
%patch1 -p1

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
cp -pr AUTHORS ChangeLog INSTALL LICENSE NEWS user-manual-%{version} %{buildroot}/usr/share/doc/%{name}-%{version}
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

%clean
rm -rf %{buildroot}

%files
%defattr (-, root, root)
%doc /usr/share/doc/%{name}-%{version}
%{_bindir}/avr-man
%{_prefix}/avr/lib/*
%{_prefix}/avr/include
