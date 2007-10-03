Summary:	Parallel Virtual Machine
Summary(es.UTF-8):	Máquina virtual paralela
Summary(pl.UTF-8):	Rozproszona Maszyna Wirtualna
Summary(pt_BR.UTF-8):	Máquina virtual paralela
Name:		pvm
Version:	3.4.5
Release:	2
License:	Free
Group:		Applications/Networking
Source0:	ftp://ftp.netlib.org/pvm3/%{name}%{version}.tgz
# Source0-md5:	086e6d707b40adba04bddba8e5b6b17d
Source1:	%{name}d.init
Source2:	ftp://www.netlib.org/pvm3/book/%{name}-book.ps
# Source2-md5:	4a2f619000d672f572f9678a46e4e2d1
Patch0:		%{name}-aimk.patch
Patch1:		%{name}-noenv.patch
Patch2:		%{name}-gcc4.patch
URL:		http://www.epm.ornl.gov/pvm/pvm_home.html
BuildRequires:	m4
BuildRequires:	ncurses-devel >= 5.0
BuildRequires:	readline-devel
BuildRequires:	rpmbuild(macros) >= 1.213
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
%ifarch %{x8664}
%define		_pvm_arch	LINUX64
%else
%error "Unsupported architecture"
exit 1
%endif
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

%description -l es.UTF-8
PVM suministra una biblioteca de envío de mensajes y un ambiente que
puede configurarse en "runtime", en una gran variedad de plataformas
de multiprocesamiento.

%description -l pl.UTF-8
PVM jest systemem pozwalającym na używanie zestawu heterogenicznych
komputerów jako jednej maszyny.

%description -l pt_BR.UTF-8
O PVM provê uma biblioteca de envio de mensagens e ambiente que pode
ser configurado em "runtime", em uma variedade de plataformas de
multiprocessamento.

%package devel
Summary:	PVM header files and static libraries
Summary(es.UTF-8):	Archivos de inclusión y bibliotecas para pvm
Summary(pl.UTF-8):	Pliki nagłówkowe i biblioteki statyczne PVM
Summary(pt_BR.UTF-8):	Arquivos de inclusão e bibliotecas para o pvm
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains PVM header files and static libraries.

%description devel -l es.UTF-8
Este paquete contiene los archivos de inclusión y bibliotecas que se
necesitan para desarrollar programas que usan pvm.

%description devel -l pl.UTF-8
Pakiet zawiera pliki nagłówkowe i biblioteki (statyczne) PVM.

%description devel -l pt_BR.UTF-8
Este pacote contém os arquivos de inclusão e bibliotecas que são
necessários para desenvolver programas que usam o pvm.

%package examples
Summary:	PVM examples
Summary(pl.UTF-8):	Przykłady użycia PVM
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description examples
This package contains PVM examples written in C and Fortran, and book
written in English.

%description examples -l pl.UTF-8
Pakiet zawiera przykłady użycia PVM napisane w C oraz Fortranie, a
także książkę po angielsku.

%package -n pvmd
Summary:	PVM Daemon
Summary(pl.UTF-8):	Demon PVM
Group:		Applications/Networking
#Requires(post,preun):	/sbin/chkconfig

%description -n pvmd
PVM Daemon.

%description -n pvmd -l pl.UTF-8
Demon PVM.

%prep
%setup -q -n %{name}3
%patch0 -p1
%patch1 -p1
%patch2 -p1

cp %{SOURCE2} .

%build
cp -f lib/aimk lib/aimk.tmp
sed -e "s!@PVM_ROOT@!%{_pvm_root}!" -e "s!@PVM_ARCH@!%{_pvm_arch}!" lib/aimk.tmp > lib/aimk

PCFLOPTS="%{rpmcflags} -DDEFBINDIR=\\\"%{_pvm_root}/bin/\\\x24PVM_ARCH\\\""
PCFLOPTS="$PCFLOPTS -DDEFDEBUGGER=\\\"%{_bindir}/debugger2\\\""
PCFLOPTS="$PCFLOPTS -DPVMDPATH=\\\"%{_sbindir}/pvmd3\\\""
PCFLOPTS="$PCFLOPTS -DPVMROOT=\\\"%{_pvm_root}\\\""

PVM_ROOT=`pwd` \
%{__make} \
	CFLOPTS="$PCFLOPTS"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_includedir},%{_libdir},%{_pvm_root}/conf} \
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

##%preun -n pvmd
##if [ "$1" = "0" ]; then
##	if [ -f /var/lock/subsys/pvmd ]; then
##		/etc/rc.d/init.d/pvmd stop >&2
##	fi
##	/sbin/chkconfig --del pvmd
##fi

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/debugger
%attr(755,root,root) %{_bindir}/debugger2
%attr(755,root,root) %{_bindir}/pvmgetarch
%attr(755,root,root) %{_bindir}/pvmtmparch
%attr(755,root,root) %{_bindir}/pvm
%attr(755,root,root) %{_bindir}/pvmgs
%dir %{_pvm_root}
%{_mandir}/man1/pvm.1*
%{_mandir}/man1/pvm_intro.1*
%{_mandir}/man1/PVM.1*

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
%doc pvm-book.ps
%{_examplesdir}/%{name}

%files -n pvmd
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/pvmd3
%attr(754,root,root) /etc/rc.d/init.d/pvmd
%{_mandir}/man1/pvmd*
%{_mandir}/man1/pvm_shmd*
