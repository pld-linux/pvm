Summary:	Parallel Virtual Machine
Summary(pl):	Rozproszona Maszyna Wirtualna
Name:		pvm
Version:	3.4.3
Release:	23
License:	Free
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Source0:	ftp://ftp.netlib.org/pvm3/%{name}%{version}.tgz
Source1:	%{name}d.init
Source2:	ftp://www.netlib.org/pvm3/book/%{name}-book.ps
Patch0:		%{name}-aimk.patch
Patch1:		%{name}-noenv.patch
Patch2:		%{name}-vaargfix.patch
URL:		http://www.epm.ornl.gov/pvm/pvm_home.html
BuildRequires:	ncurses-devel >= 5.0
BuildRequires:	readline-devel
BuildRequires:	m4
Prereq:		/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pvm_root 	%{_datadir}/pvm3
%define		_pvm_arch	LINUX

%description
PVM is a software system that enables a collection of heterogeneous
computers to be used as a coherent and flexible concurrent
computational resource.

The individual computers may be shared- or local-memory
multiprocessors, vector supercomputers, specialized graphics engines,
or scalar workstations, that may be interconnected by a variety of
networks, such as ethernet, FDDI.

User programs written in C, C++ or Fortran access PVM through library
routines.

%description -l pl
PVM jest systemem pozwalaj±cym na u¿ywanie zestawu heterogenicznych
komputerów jako jednej maszyny.

%package devel
Summary:	PVM header files and static libraries
Summary(pl):	Pliki nag³ówkowe i biblioteki statyczne PVM
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Requires:	%{name} = %{version}

%description devel
This package contains PVM header files and static libraries.

%description devel -l pl
Pakiet zawiera pliki nag³ówkowe i biblioteki (statyczne) PVM.

%package examples
Summary:	PVM examples
Summary(pl):	Przyk³ady u¿ycia PVM
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Requires:	%{name}-devel = %{version}

%description examples
This package contains PVM examples written in C and Fortran, and book
written in English.

%description examples -l pl
Pakiet zawiera przyk³ady u¿ycia PVM napisane w C oraz Fortranie, a tak¿e
ksi±¿kê po angielsku.

%prep 
%setup -q -n pvm3
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
cp -f lib/aimk lib/aimk.tmp
sed -e "s!@PVM_ROOT@!%{_pvm_root}!" -e "s!@PVM_ARCH@!%{_pvm_arch}!" lib/aimk.tmp > lib/aimk

PCFLOPTS="%{rpmcflags} -DDEFBINDIR=\\\"\\\x24HOME/pvm3/bin/\\\x24PVM_ARCH\\\""
PCFLOPTS="$PCFLOPTS -DDEFDEBUGGER=\\\"%{_bindir}/debugger2\\\""
PCFLOPTS="$PCFLOPTS -DPVMDPATH=\\\"%{_sbindir}/pvmd3\\\""
PCFLOPTS="$PCFLOPTS -DPVMROOT=\\\"%{_pvm_root}\\\""

PVM_ROOT=`pwd` make CFLOPTS="$PCFLOPTS"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_includedir},%{_libdir},%{_pvm_root}/conf,%{_docdir}/%{name}} \
	$RPM_BUILD_ROOT%{_examplesdir}/%{name}/{examples,gexamples,hoster,misc,tasker,xep} \
	$RPM_BUILD_ROOT{%{_mandir}/man{1,3},/etc/rc.d/init.d,%{_sbindir}}

install %{SOURCE1}  $RPM_BUILD_ROOT/etc/rc.d/init.d/pvmd

install lib/%{_pvm_arch}/{pvm,pvmgs} $RPM_BUILD_ROOT%{_bindir}
install lib/%{_pvm_arch}/pvmd3 $RPM_BUILD_ROOT%{_sbindir}
install lib/debugger	$RPM_BUILD_ROOT%{_bindir}
install lib/debugger2	$RPM_BUILD_ROOT%{_bindir}
install lib/pvmgetarch	$RPM_BUILD_ROOT%{_bindir}
install lib/pvmtmparch	$RPM_BUILD_ROOT%{_bindir}
install lib/aimk	$RPM_BUILD_ROOT%{_bindir}
install conf/%{_pvm_arch}.def $RPM_BUILD_ROOT%{_pvm_root}/conf
install include/{fpvm3,pvm3,pvmproto,pvmtev}.h $RPM_BUILD_ROOT%{_includedir}
install lib/%{_pvm_arch}/lib*.a $RPM_BUILD_ROOT%{_libdir}

install man/man1/* $RPM_BUILD_ROOT%{_mandir}/man1
install man/man3/* $RPM_BUILD_ROOT%{_mandir}/man3

# Examples
cp -rf examples gexamples hoster misc tasker xep $RPM_BUILD_ROOT%{_examplesdir}/%{name}
install %{SOURCE2}  $RPM_BUILD_ROOT%{_docdir}/%{name}/pvm-book.ps
gzip -9nf $RPM_BUILD_ROOT%{_docdir}/%{name}/pvm-book.ps

%clean
rm -rf $RPM_BUILD_ROOT

# NOTE: don't uncomment scripts unless you do something with this:
# Normal user can't use pvmd ran by another user (or root).
# User who wants to run pvm, runs his own copy of pvmd.

##%post
##/sbin/chkconfig --add pvmd
##if [ -f /var/lock/subsys/pvmd ]; then
##	/etc/rc.d/init.d/pvmd restart >&2
##else
##	echo "Run \"/etc/rc.d/init.d/pvmd start\" to start PVM daemon." >&2
##fi

##%preun
##if [ "$1" = "0" ]; then
##	if [ -f /var/lock/subsys/pvmd ]; then
##		/etc/rc.d/init.d/pvmd stop >&2
##	fi
##	/sbin/chkconfig --del pvmd
##fi

%files
%defattr(644,root,root,755)
##%attr(755,root,root) /etc/rc.d/init.d/pvmd
%attr(755,root,root) %{_bindir}/debugger
%attr(755,root,root) %{_bindir}/debugger2
%attr(755,root,root) %{_bindir}/pvmgetarch
%attr(755,root,root) %{_bindir}/pvmtmparch
%attr(755,root,root) %{_bindir}/pvm
%attr(755,root,root) %{_bindir}/pvmgs
%attr(755,root,root) %{_sbindir}/pvmd3
%dir %{_pvm_root}
%{_mandir}/man1/pvm*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/aimk
%{_pvm_root}/conf
%{_includedir}/fpvm3.h
%{_includedir}/pvm3.h
%{_includedir}/pvmproto.h
%{_includedir}/pvmtev.h
%{_libdir}/libfpvm3.a
%{_libdir}/libgpvm3.a
%{_libdir}/libpvm3.a
%{_libdir}/libpvmtrc.a
%{_mandir}/man1/aimk.1*
%{_mandir}/man3/*

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}
%{_docdir}/%{name}
