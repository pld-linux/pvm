Summary:	Parallel Virtual Machine
Name:		pvm
Version:	3.40
Release:	1
Copyright:	
Group:		Development/Library
Source0:	ftp://ftp.netlib.org/pvm3/%{name}.%{version}.tar.gz
BuildRoot:	/tmp/pvm_root

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
%setup -n pvm3

%build
PVM_ROOT=`pwd` make

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/usr/{bin,include,lib,man/man{1,3}}

install -s lib/LINUX/{pvm,pvmd3,pvmgs,pvm_gstat,pvmgroups,pvmgs,mtracer,trcsort} \
	$RPM_BUILD_ROOT/usr/pvm3/lib/LINUX

for f in aimk cshrc.stub debugger debugger2 ipcfree pvm pvmd\
		pvmgetarch pvmtmparch xpvm; do
	install -m755 lib/ $RPM_BUILD_ROOT/usr/bin
done

install include/{fpvm3,pvm3,pvmproto,pvmtev}.h $RPM_BUILD_ROOT/usr/include
install lib/LINUX/lib*.a $RPM_BUILD_ROOT/usr/lib

install man/man1/* $RPM_BUILD_ROOT%{_mandir}/man1
install man/man3/* $RPM_BUILD_ROOT%{_mandir}/man3

# Examples
cp -arv examples $RPM_BUILD_ROOT/usr/pvm3
cp -arv gexamples $RPM_BUILD_ROOT/usr/pvm3
cp -arv hoster $RPM_BUILD_ROOT/usr/pvm3
cp -arv misc $RPM_BUILD_ROOT/usr/pvm3
cp -arv tasker $RPM_BUILD_ROOT/usr/pvm3
cp -arv xep $RPM_BUILD_ROOT/usr/pvm3

ln -sf ../pvm3/lib/aimk $RPM_BUILD_ROOT/usr/bin/aimk
ln -sf ../pvm3/lib/pvm  $RPM_BUILD_ROOT/usr/bin/pvm
ln -sf ../../../pvm3/lib/pvmd $RPM_BUILD_ROOT/usr/bin/pvmd

%clean
rm -rf $RPM_BUILD_ROOT

%post
echo 'Please set the PVM_ROOT variable to point to /usr/pvm3'
echo -n

%preun

%files
%attr(-,root,root) /usr/bin/aimk
%attr(-,root,root) /usr/bin/pvm
%attr(-,root,root) /usr/bin/pvmd
%attr(-,root,root) /usr/pvm3/bin/LINUX/pvm_gstat
%attr(-,root,root) /usr/pvm3/bin/LINUX/pvmgroups
%attr(-,root,root) /usr/pvm3/bin/LINUX/pvmgs
%attr(-,root,root) /usr/pvm3/bin/LINUX/tracer
%attr(-,root,root) /usr/pvm3/bin/LINUX/trcsort
%attr(-,root,root) /usr/pvm3/lib/aimk
%attr(-,root,root) /usr/pvm3/lib/cshrc.stub
%attr(-,root,root) /usr/pvm3/lib/debugger
%attr(-,root,root) /usr/pvm3/lib/debugger2
%attr(-,root,root) /usr/pvm3/lib/ipcfree
%attr(-,root,root) /usr/pvm3/lib/pvm
%attr(-,root,root) /usr/pvm3/lib/pvmd
%attr(-,root,root) /usr/pvm3/lib/pvmgetarch
%attr(-,root,root) /usr/pvm3/lib/pvmtmparch
%attr(-,root,root) /usr/pvm3/lib/xpvm
%attr(-,root,root) /usr/pvm3/lib/LINUX/pvm
%attr(-,root,root) /usr/pvm3/lib/LINUX/pvmd3
%attr(-,root,root) /usr/pvm3/lib/LINUX/pvmgs
%attr(-,root,root) /usr/include/fpvm3.h
%attr(-,root,root) /usr/include/pvm3.h
%attr(-,root,root) /usr/include/pvmproto.h
%attr(-,root,root) /usr/include/pvmtev.h
%attr(-,root,root) /usr/lib/libfpvm3.a
%attr(-,root,root) /usr/lib/libgpvm3.a
%attr(-,root,root) /usr/lib/libpvm3.a
%attr(-,root,root) /usr/lib/libpvmtrc.a
%attr(-,root,root) %{_mandir}/man1/*
%attr(-,root,root) %{_mandir}/man3/*
%attr(-,root,root) /usr/pvm3/examples/* 
%attr(-,root,root) /usr/pvm3/gexamples/* 
%attr(-,root,root) /usr/pvm3/hoster/* 
%attr(-,root,root) /usr/pvm3/misc/* 
%attr(-,root,root) /usr/pvm3/tasker/* 
%attr(-,root,root) /usr/pvm3/xep/* 
%attr(-,root,root) %doc Readme 
%attr(-,root,root) %doc doc/* 

%changelog
