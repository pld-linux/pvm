Summary: Parallel Virtual Machine
Name: pvm3
%define version 4.beta6
Version: %{version}
Release: 1
Copyright: 
Group: Development/Library
Source0: pvm3.%{PACKAGE_VERSION}.tar.gz
BuildRoot: /tmp/pvm_root
URL: ftp://ftp.netlib.org/pvm3/pvm3.%{PACKAGE_VERSION}.tar.gz
Packager: Mihai Ibanescu <misa@dntis.ro>

%description
PVM is a software system that enables a collection of heterogeneous
computers to be used as a coherent and flexible concurrent computational
resource.

The individual computers may be shared- or local-memory multiprocessors,
vector supercomputers, specialized graphics engines, or scalar
workstations, that may be interconnected by a variety of networks,
such as ethernet, FDDI.

User programs written in C, C++ or Fortran access PVM through library
routines.

%prep 
%setup -n pvm3

%build
PVM_ROOT=`pwd` make

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/usr/bin
mkdir -p $RPM_BUILD_ROOT/usr/include
mkdir -p $RPM_BUILD_ROOT/usr/lib
mkdir -p $RPM_BUILD_ROOT/usr/local/pvm3/bin/LINUX
mkdir -p $RPM_BUILD_ROOT/usr/local/pvm3/lib/LINUX
mkdir -p $RPM_BUILD_ROOT/usr/man/man1
mkdir -p $RPM_BUILD_ROOT/usr/man/man3

for f in pvm_gstat pvmgroups pvmgs tracer trcsort; do
	install -m755 -s bin/LINUX/$f $RPM_BUILD_ROOT/usr/local/pvm3/bin/LINUX
done
for f in pvm pvmd3 pvmgs; do
	install -m755 -s lib/LINUX/$f $RPM_BUILD_ROOT/usr/local/pvm3/lib/LINUX
done
for f in aimk cshrc.stub debugger debugger2 ipcfree pvm pvmd\
		pvmgetarch pvmtmparch xpvm; do
	install -m755 lib/$f $RPM_BUILD_ROOT/usr/local/pvm3/lib
done
for f in fpvm3.h pvm3.h pvmproto.h pvmtev.h; do
	install -m755 include/$f $RPM_BUILD_ROOT/usr/include
done

for f in libfpvm3.a libgpvm3.a libpvm3.a libpvmtrc.a; do 
	install -m755 lib/LINUX/$f $RPM_BUILD_ROOT/usr/lib
done

cp -a man/man1/* $RPM_BUILD_ROOT/usr/man/man1
cp -a man/man3/* $RPM_BUILD_ROOT/usr/man/man3

# Examples
cp -arv examples $RPM_BUILD_ROOT/usr/local/pvm3
cp -arv gexamples $RPM_BUILD_ROOT/usr/local/pvm3
cp -arv hoster $RPM_BUILD_ROOT/usr/local/pvm3
cp -arv misc $RPM_BUILD_ROOT/usr/local/pvm3
cp -arv tasker $RPM_BUILD_ROOT/usr/local/pvm3
cp -arv xep $RPM_BUILD_ROOT/usr/local/pvm3

ln -sf ../local/pvm3/lib/aimk $RPM_BUILD_ROOT/usr/bin/aimk
ln -sf ../local/pvm3/lib/pvm  $RPM_BUILD_ROOT/usr/bin/pvm
ln -sf ../../../local/pvm3/lib/pvmd $RPM_BUILD_ROOT/usr/bin/pvmd

%clean
rm -rf $RPM_BUILD_ROOT

%post
echo 'Please set the PVM_ROOT variable to point to /usr/local/pvm3'
echo -n

%preun

%files
%attr(-,root,root) /usr/bin/aimk
%attr(-,root,root) /usr/bin/pvm
%attr(-,root,root) /usr/bin/pvmd
%attr(-,root,root) /usr/local/pvm3/bin/LINUX/pvm_gstat
%attr(-,root,root) /usr/local/pvm3/bin/LINUX/pvmgroups
%attr(-,root,root) /usr/local/pvm3/bin/LINUX/pvmgs
%attr(-,root,root) /usr/local/pvm3/bin/LINUX/tracer
%attr(-,root,root) /usr/local/pvm3/bin/LINUX/trcsort
%attr(-,root,root) /usr/local/pvm3/lib/aimk
%attr(-,root,root) /usr/local/pvm3/lib/cshrc.stub
%attr(-,root,root) /usr/local/pvm3/lib/debugger
%attr(-,root,root) /usr/local/pvm3/lib/debugger2
%attr(-,root,root) /usr/local/pvm3/lib/ipcfree
%attr(-,root,root) /usr/local/pvm3/lib/pvm
%attr(-,root,root) /usr/local/pvm3/lib/pvmd
%attr(-,root,root) /usr/local/pvm3/lib/pvmgetarch
%attr(-,root,root) /usr/local/pvm3/lib/pvmtmparch
%attr(-,root,root) /usr/local/pvm3/lib/xpvm
%attr(-,root,root) /usr/local/pvm3/lib/LINUX/pvm
%attr(-,root,root) /usr/local/pvm3/lib/LINUX/pvmd3
%attr(-,root,root) /usr/local/pvm3/lib/LINUX/pvmgs
%attr(-,root,root) /usr/include/fpvm3.h
%attr(-,root,root) /usr/include/pvm3.h
%attr(-,root,root) /usr/include/pvmproto.h
%attr(-,root,root) /usr/include/pvmtev.h
%attr(-,root,root) /usr/lib/libfpvm3.a
%attr(-,root,root) /usr/lib/libgpvm3.a
%attr(-,root,root) /usr/lib/libpvm3.a
%attr(-,root,root) /usr/lib/libpvmtrc.a
%attr(-,root,root) /usr/man/man1/*
%attr(-,root,root) /usr/man/man3/*
%attr(-,root,root) /usr/local/pvm3/examples/* 
%attr(-,root,root) /usr/local/pvm3/gexamples/* 
%attr(-,root,root) /usr/local/pvm3/hoster/* 
%attr(-,root,root) /usr/local/pvm3/misc/* 
%attr(-,root,root) /usr/local/pvm3/tasker/* 
%attr(-,root,root) /usr/local/pvm3/xep/* 
%attr(-,root,root) %doc Readme 
%attr(-,root,root) %doc doc/* 

%changelog
