%define         libcudd         %mklibname cudd 2
%define         libcudd_devel   %mklibname -d cudd

Name:           cudd
Version:        2.5.0
Release:        1
Summary:        CU Decision Diagram Package
Group:          Sciences/Mathematics
License:        BSD
URL:            http://vlsi.colorado.edu/~fabio/CUDD/
Source0:        ftp://vlsi.Colorado.EDU/pub/%{name}-%{version}.tar.gz
# This patch was sent upstream in September 2005.
# Build shared libraries as well as static archives, and incidentally unbreak
# parallel make.
Patch0:         cudd-2.5.0-sharedlib.patch
# This patch was sent upstream in September 2005.
# Fix some mixed signed/unsigned operations
Patch1:         cudd-2.5.0-signedness.patch
# This patch was sent upstream in September 2005.
# Don't ignore the return values of certain functions
Patch2:         cudd-2.5.0-retval.patch
# This patch was sent upstream in September 2005.
# Fix a bunch of "used without being initialized" warnings
Patch3:         cudd-2.5.0-init.patch
# This patch was sent upstream in September 2005.
# On 64 bit platforms, fix the size definitions of void * and long.
# Use the correct floating point structure based on endianness.
Patch4:         cudd-2.5.0-arch.patch


%description
CUDD is a package for the manipulation of Binary Decision Diagrams
(BDDs), Algebraic Decision Diagrams (ADDs) and Zero-suppressed
Binary Decision Diagrams (ZDDs).


%package        -n %{libcudd}
Summary:        Runtime libraries for %{name}
Group:          Sciences/Mathematics
Requires:       %{libcudd} = %{version}-%{release}


%description    -n %{libcudd}
Runtime libraries for %{name}.


%package        -n %{libcudd_devel}
Summary:        Header files and man pages for %{name}
Group:          Development/C++
Requires:       %{libcudd} = %{version}-%{release}
Provides:       %{name}-devel = %{version}-%{release}


%description    -n %{libcudd_devel}
Development headers and man pages for %{name}.


%prep
%setup -q
%patch0
%patch1
%patch2
%patch3
%patch4

# Fix two doc files with DOS line endings
for f in dddmp/README.*; do
  sed 's/\r//' $f > ${f}.fixed
  touch -r $f ${f}.fixed
  mv -f ${f}.fixed $f
done


%build
# Build the shared libraries and binaries
make %{?_smp_mflags} CPPFLAGS="%{optflags}" ICFLAGS="%{optflags} -fPIC" \
  XCFLAGS="-DHAVE_IEEE_754 -DBSD"


%install
# Install the shared libraries
mkdir -p $RPM_BUILD_ROOT%{_libdir}
for slib in */*.so; do
  install -p -m 755 ${slib}.%{version} $RPM_BUILD_ROOT%{_libdir}/
  mv ${slib}.2 $RPM_BUILD_ROOT%{_libdir}
  mv ${slib} $RPM_BUILD_ROOT%{_libdir}
done

# Install the header files
mkdir -p $RPM_BUILD_ROOT%{_includedir}/%{name}
for hdr in include/*; do
  install -p -m 644 ${hdr} $RPM_BUILD_ROOT%{_includedir}/%{name}/
done

# Install the test binary
mkdir -p $RPM_BUILD_ROOT%{_bindir}
install -p -m 0755 nanotrav/nanotrav $RPM_BUILD_ROOT%{_bindir}

# Install the test binary man page
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
install -p -m 0644 nanotrav/nanotrav.1 $RPM_BUILD_ROOT%{_mandir}/man1

# Put all the documentation in one place for easy installation
mkdir doc
mv cudd/doc doc/cudd
mv dddmp/doc doc/dddmp
mv dddmp/R* doc/dddmp
mv mtr/doc doc/mtr
mv nanotrav/doc doc/nanotrav
mv nanotrav/README doc/nanotrav
mv st/doc doc/st


%files
%doc README LICENSE RELEASE.NOTES doc/nanotrav
%{_bindir}/nanotrav
%{_mandir}/man1/*


%files -n %{libcudd}
%doc README LICENSE doc/cudd doc/dddmp doc/mtr doc/st
%{_libdir}/*.so.*


%files -n %{libcudd_devel}
%doc README LICENSE doc/cudd doc/dddmp doc/mtr doc/st
%{_includedir}/%{name}
%{_libdir}/*.so
