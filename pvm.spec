Summary:	Parallel Virtual Machine
Summary(es):	Máquina virtual paralela
Summary(pl):	Rozproszona Maszyna Wirtualna
Summary(pt_BR):	Máquina virtual paralela
Name:		pvm
Version:	3.4.4
Release:	3
License:	Free
Group:		Development/Libraries
Source0:	ftp://ftp.netlib.org/pvm3/%{name}%{version}.tgz
# Source0-md5: 806abe9a866eab5981383c17ff9ed175
Source1:	%{name}d.init
Source2:	ftp://www.netlib.org/pvm3/book/%{name}-book.ps
Patch0:		%{name}-aimk.patch
Patch1:		%{name}-noenv.patch
URL:		http://www.epm.ornl.gov/pvm/pvm_home.html
BuildRequires:	ncurses-devel >= 5.0
BuildRequires:	readline-devel
BuildRequires:	m4
Prereq:		/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pvm_root 	%{_libdir}/pvm3
%ifarch %{ix86}
%define		_pvm_arch	LINUX
%else
%ifarch alpha
%define		_pvm_arch	LINUXALPHA
%else
%ifarch sparc sparc64
%define		_pvm_arch	LINUXSPARC
%else
%ifarch ppc
%define		_pvm_arch	LINUXPPC
%else
%ifarch hppa
%define		_pvm_arch	LINUXHPPA
%else
%error "Unsupported architecture"
exit 1
%endif
%endif
%endif
%endif
%endif

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

%description -l es
PVM suministra una biblioteca de envío de mensajes y un ambiente que
puede configurarse en "runtime", en una gran variedad de plataformas
de multiprocesamiento.

%description -l pl
PVM jest systemem pozwalaj±cym na u¿ywanie zestawu heterogenicznych
komputerów jako jednej maszyny.

%description -l pt_BR
O PVM provê uma biblioteca de envio de mensagens e ambiente que pode
ser configurado em "runtime", em uma variedade de plataformas de
multiprocessamento.

%package devel
Summary:	PVM header files and static libraries
Summary(es):	Archivos de inclusión y bibliotecas para pvm
Summary(pl):	Pliki nag³ówkowe i biblioteki statyczne PVM
Summary(pt_BR):	Arquivos de inclusão e bibliotecas para o pvm
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
This package contains PVM header files and static libraries.

%description devel -l es
Este paquete contiene los archivos de inclusión y bibliotecas que se
necesitan para desarrollar programas que usan pvm.

%description devel -l pl
Pakiet zawiera pliki nag³ówkowe i biblioteki (statyczne) PVM.

%description devel -l pt_BR
Este pacote contém os arquivos de inclusão e bibliotecas que são
necessários para desenvolver programas que usam o pvm.

%package examples
Summary:	PVM examples
Summary(pl):	Przyk³ady u¿ycia PVM
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description examples
This package contains PVM examples written in C and Fortran, and book
written in English.

%description examples -l pl
Pakiet zawiera przyk³ady u¿ycia PVM napisane w C oraz Fortranie, a
tak¿e ksi±¿kê po angielsku.

%package -n pvmd
Summary:	PVM Daemon
Summary(pl):	Serwer PVM
Group:		Development/Libraries
#Requires:	%{name}-devel = %{version}

%description -n pvmd

%description -n pvmd -l pl

%prep
%setup -q -n pvm3
%patch0 -p1
%patch1 -p1

%build
cp -f lib/aimk lib/aimk.tmp
sed -e "s!@PVM_ROOT@!%{_pvm_root}!" -e "s!@PVM_ARCH@!%{_pvm_arch}!" lib/aimk.tmp > lib/aimk

PCFLOPTS="%{rpmcflags} -DDEFBINDIR=\\\"%{_pvm_root}/bin/\\\x24PVM_ARCH\\\""
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

%post -n pvmd
##/sbin/chkconfig --add pvmd
##if [ -f /var/lock/subsys/pvmd ]; then
##	/etc/rc.d/init.d/pvmd restart >&2
##else
	echo "Run \"/etc/rc.d/init.d/pvmd start\" to start PVM daemon." >&2
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
%dir %{_pvm_root}
%{_mandir}/man1/pvm*
%{_mandir}/man1/PVM*

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

%files -n pvmd
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/pvmd3
%attr(600,root,root) /etc/rc.d/init.d/pvmd
