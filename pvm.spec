Summary:	Parallel Virtual Machine
Name:		pvm
Version:	3.4.0
Release:	2
Copyright:	free
Group:		Development/Libraries
Source0:	ftp://ftp.netlib.org/pvm3/%{name}%{version}.tgz
Source1:	pvmd.init
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define _pvm_root 	%{_datadir}/pvm3/
%define _pvm_arch	LINUX

%description
PVM is a software system that enables a collection of heterogeneous
computers to be used as a coherent and flexible concurrent computational
resource.

The individual computers may be shared- or local-memory multiprocessors,
vector supercomputers, specialized graphics engines, or scalar workstations,
that may be interconnected by a variety of networks, such as ethernet, FDDI.

User programs written in C, C++ or Fortran access PVM through library
routines.

%prep 
%setup -q -n pvm3

%build
PVM_ROOT=`pwd` make

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/usr/{bin,include,lib}
install -d $RPM_BUILD_ROOT%{_pvm_root}/lib/%{_pvm_arch}
install -d $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/{examples,gexamples,hoster,misc,tasker,xep}
install -d $RPM_BUILD_ROOT%{_mandir}/{man1,man3}
install -d $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/
install -d $RPM_BUILD_ROOT%{_sbindir}

install %{SOURCE1}  $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/pvmd

install lib/%{_pvm_arch}/{pvm,pvmgs} \
	$RPM_BUILD_ROOT%{_bindir}
install lib/%{_pvm_arch}/pvmd3 $RPM_BUILD_ROOT%{_sbindir}/



install lib/debugger	$RPM_BUILD_ROOT%{_bindir}
install lib/debugger2	$RPM_BUILD_ROOT%{_bindir}
install lib/pvmgetarch	$RPM_BUILD_ROOT%{_bindir}
install lib/pvmtmparch	$RPM_BUILD_ROOT%{_bindir}
install lib/xpvm	$RPM_BUILD_ROOT%{_bindir}

install include/{fpvm3,pvm3,pvmproto,pvmtev}.h $RPM_BUILD_ROOT%{_includedir}
install lib/%{_pvm_arch}/lib*.a $RPM_BUILD_ROOT%{_libdir}

install man/man1/* $RPM_BUILD_ROOT%{_mandir}/man1
install man/man3/* $RPM_BUILD_ROOT%{_mandir}/man3

# Examples
cp -rf examples/* $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/examples/
cp -rf gexamples/* $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/gexamples
cp -rf hoster/* $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/hoster
cp -rf misc/* $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/misc
cp -rf tasker/* $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/tasker
cp -rf xep/* $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/xep

#ln -sf  $RPM_BUILD_ROOT%{_bindir}/aimk %{_pvm_root}/lib/aimk
#ln -sf  $RPM_BUILD_ROOT%{_bindir}/pvm  %{_pvm_root}/lib/pvm
#ln -sf  $RPM_BUILD_ROOT%{_bindir}/pvmd %{_pvm_root}/lib/pvmd

%clean
rm -rf $RPM_BUILD_ROOT

%post
ln -sf %{_bindir}/pvmd3 %{_pvm_root}/lib/LINUX/pvmd3 
ln -sf %{_bindir}/pvm %{_pvm_root}/lib/LINUX/pvm 
ln -sf %{_bindir}/pvmgs %{_pvm_root}/lib/LINUX/pvmgs

%{_sysconfdir}/rc.d/init.d/pvmd restart
%postun

%{_sysconfdir}/rc.d/init.d/pvmd stop

%files
%{_sysconfdir}/rc.d/init.d/pvmd
%{_bindir}/debugger
%{_bindir}/debugger2
%{_bindir}/pvmgetarch
%{_bindir}/pvmtmparch
%{_bindir}/xpvm
%{_bindir}/pvm
%{_sbindir}/pvmd3
%{_bindir}/pvmgs
%{_includedir}/fpvm3.h
%{_includedir}/pvm3.h
%{_includedir}/pvmproto.h
%{_includedir}/pvmtev.h
%{_libdir}/libfpvm3.a
%{_libdir}/libgpvm3.a
%{_libdir}/libpvm3.a
%{_libdir}/libpvmtrc.a
%{_pvm_root}/lib/%{_pvm_arch}
%{_mandir}/man1/*
%{_mandir}/man3/*
%doc %{_docdir}/%{name}-%{version}/examples/* 
%doc %{_docdir}/%{name}-%{version}/gexamples/* 
%doc %{_docdir}/%{name}-%{version}/hoster/* 
%doc %{_docdir}/%{name}-%{version}/misc/* 
%doc %{_docdir}/%{name}-%{version}/tasker/* 
%doc %{_docdir}/%{name}-%{version}/xep/* 
