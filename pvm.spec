Summary:	Parallel Virtual Machine
Name:		pvm
Version:	3.4.0
%define	xpvm_version	1.2.5
Release:	3
Copyright:	free
Group:		Development/Libraries
Source0:	ftp://ftp.netlib.org/pvm3/%{name}%{version}.tgz
Source1:	pvmd.init
Source3:	http://www.netlib.org/pvm3/xpvm/XPVM.src.%{xpvm_version}.tgz
Patch0:		xpvm.patch
Patch1:		xpvm-help-path.patch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
BuildRequires:	ncurses-devel >= 5.0
BuildRequires:	readline-devel
# xpvm buildreq:
BuildRequires:	tk-devel
BuildRequires:	tcl-devel
BuildRequires:	XFree86-devel

%define _pvm_root 	%{_datadir}/pvm3
%define _pvm_arch	LINUX
%define _xpvm_root	%{_pvm_root}/xpvm
%define _xbindir	%{_prefix}/X11R6/bin

%description
PVM is a software system that enables a collection of heterogeneous
computers to be used as a coherent and flexible concurrent computational
resource.

The individual computers may be shared- or local-memory multiprocessors,
vector supercomputers, specialized graphics engines, or scalar workstations,
that may be interconnected by a variety of networks, such as ethernet, FDDI.

User programs written in C, C++ or Fortran access PVM through library
routines.

%package gui
Summary:	TCL/TK graphical frontend to monitor and manage a PVM cluster.
Group:		X11/Development/Libraries
Requires:	pvm

%description gui
Xpvm is a TCL/TK based tool that allows full manageability of the PVM cluster
as well as the ability to monitor cluster performance.

%prep 
%setup -q -n pvm3
%setup -q -T -n pvm3 -D -a3
%patch0 -p0
%patch1 -p1

%build
PVM_ROOT=`pwd` make CFLOPTS="%{?debug:-O -g}%{!?debug:$RPM_OPT_FLAGS}"
PVM_ROOT=`pwd` XPVM_ROOT=`pwd`/xpvm make -C xpvm CFLOPTS="%{?debug:-O -g}%{!?debug:$RPM_OPT_FLAGS}"

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/usr/{bin,include,lib}
install -d $RPM_BUILD_ROOT%{_pvm_root}/lib/%{_pvm_arch}
install -d $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/{examples,gexamples,hoster,misc,tasker,xep}
install -d $RPM_BUILD_ROOT%{_mandir}/{man1,man3}
install -d $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d
install -d $RPM_BUILD_ROOT%{_sbindir}

install %{SOURCE1}  $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/pvmd

install lib/%{_pvm_arch}/{pvm,pvmgs} \
	$RPM_BUILD_ROOT%{_bindir}
install lib/%{_pvm_arch}/pvmd3 $RPM_BUILD_ROOT%{_sbindir}/

install lib/debugger	$RPM_BUILD_ROOT%{_bindir}
install lib/debugger2	$RPM_BUILD_ROOT%{_bindir}
install lib/pvmgetarch	$RPM_BUILD_ROOT%{_bindir}
install lib/pvmtmparch	$RPM_BUILD_ROOT%{_bindir}
#install lib/xpvm	$RPM_BUILD_ROOT%{_bindir}

install include/{fpvm3,pvm3,pvmproto,pvmtev}.h $RPM_BUILD_ROOT%{_includedir}
install lib/%{_pvm_arch}/lib*.a $RPM_BUILD_ROOT%{_libdir}

install man/man1/* $RPM_BUILD_ROOT%{_mandir}/man1
install man/man3/* $RPM_BUILD_ROOT%{_mandir}/man3

# Examples
cp -rf examples/* $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/examples
cp -rf gexamples/* $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/gexamples
cp -rf hoster/* $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/hoster
cp -rf misc/* $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/misc
cp -rf tasker/* $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/tasker
cp -rf xep/* $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/xep

ln -sf %{_sbindir}/pvmd3 $RPM_BUILD_ROOT%{_pvm_root}/lib/LINUX/pvmd3
ln -sf %{_bindir}/pvm $RPM_BUILD_ROOT%{_pvm_root}/lib/LINUX/pvm
ln -sf %{_bindir}/pvmgs $RPM_BUILD_ROOT%{_pvm_root}/lib/LINUX/pvmgs

# profile.d
install -d $RPM_BUILD_ROOT/etc/profile.d
cat >$RPM_BUILD_ROOT/etc/profile.d/pvm.sh <<EOF
PVM_ROOT="%{_pvm_root}"
XPVM_ROOT="%{_xpvm_root}"
export PVM_ROOT XPVM_ROOT
EOF
cat >$RPM_BUILD_ROOT/etc/profile.d/pvm.csh <<EOF
setenv PVM_ROOT "%{_pvm_root}"
setenv XPVM_ROOT "%{_xpvm_root}"
EOF

# xpvm
install -d $RPM_BUILD_ROOT%{_xbindir}
install xpvm/src/LINUX/xpvm $RPM_BUILD_ROOT%{_xbindir}
install -d $RPM_BUILD_ROOT%{_xpvm_root}
install xpvm/*.tcl $RPM_BUILD_ROOT%{_xpvm_root}
cp -rf xpvm/src/xbm $RPM_BUILD_ROOT%{_xpvm_root}
cp -rf xpvm/src/help $RPM_BUILD_ROOT%{_xpvm_root}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_sysconfdir}/rc.d/init.d/pvmd restart

%postun
%{_sysconfdir}/rc.d/init.d/pvmd stop

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_sysconfdir}/rc.d/init.d/pvmd
%attr(755,root,root) %{_bindir}/debugger
%attr(755,root,root) %{_bindir}/debugger2
%attr(755,root,root) %{_bindir}/pvmgetarch
%attr(755,root,root) %{_bindir}/pvmtmparch
%attr(755,root,root) %{_bindir}/pvm
%attr(755,root,root) %{_sbindir}/pvmd3
%attr(755,root,root) %{_bindir}/pvmgs
%{_includedir}/fpvm3.h
%{_includedir}/pvm3.h
%{_includedir}/pvmproto.h
%{_includedir}/pvmtev.h
%{_libdir}/libfpvm3.a
%{_libdir}/libgpvm3.a
%{_libdir}/libpvm3.a
%{_libdir}/libpvmtrc.a
%dir %{_pvm_root}
%{_pvm_root}/lib
%{_mandir}/man1/*
%{_mandir}/man3/*
%doc %{_docdir}/%{name}-%{version}/examples/* 
%doc %{_docdir}/%{name}-%{version}/gexamples/* 
%doc %{_docdir}/%{name}-%{version}/hoster/* 
%doc %{_docdir}/%{name}-%{version}/misc/* 
%doc %{_docdir}/%{name}-%{version}/tasker/* 
%doc %{_docdir}/%{name}-%{version}/xep/* 
%attr(755,root,root) /etc/profile.d/pvm.sh
%attr(755,root,root) /etc/profile.d/pvm.csh

%files gui
%defattr(644,root,root,755)
%attr(755,root,root) %{_xbindir}/xpvm
%{_xpvm_root}
