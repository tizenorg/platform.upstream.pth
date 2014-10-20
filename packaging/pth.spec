Name:           pth
Version:        2.0.7
Release:        0
License:        LGPL-2.1+
Summary:        GNU Portable Threads
Url:            http://www.gnu.org/software/pth/
Group:          Development/Libraries/C and C++
Source:         %{name}-%{version}.tar.bz2
Source2:        baselibs.conf
Source1001: 	pth.manifest
BuildRequires:  autoconf

%description
Pth is a very portable POSIX/ANSI-C based library for Unix platforms
which provides non-preemptive priority-based scheduling for multiple
threads of execution ("multithreading") inside server applications. All
threads run in the same address space of the server application, but
each thread has it's own individual program-counter, run-time stack,
signal mask and errno variable.

%package -n libpth
Summary:        GNU Portable Threads
Group:          Development/Libraries/C and C++
Provides:       pth
Obsoletes:      pth
%define library_name libpth
%define debug_package_requires %{library_name} = %{version}-%{release}

%description -n libpth
Pth is a very portable POSIX/ANSI-C based library for Unix platforms
which provides non-preemptive priority-based scheduling for multiple
threads of execution ("multithreading") inside server applications. All
threads run in the same address space of the server application, but
each thread has it's own individual program-counter, run-time stack,
signal mask and errno variable.

%package -n libpth-devel
Summary:        GNU Portable Threads
Group:          Development/Libraries/C and C++
Requires:       %{library_name} = %{version}
Provides:       pth-devel = %{version}
Obsoletes:      pth-devel < %{version}

%description -n libpth-devel
Pth is a very portable POSIX/ANSI-C based library for Unix platforms
which provides non-preemptive priority-based scheduling for multiple
threads of execution ("multithreading") inside server applications. All
threads run in the same address space of the server application, but
each thread has it's own individual program-counter, run-time stack,
signal mask and errno variable.

%prep
%setup -q
cp %{SOURCE1001} .

%build
export ac_cv_func_sigstack=no
autoconf
%ifarch %{arm}
CFLAGS="${RPM_OPT_FLAGS/-D_FORTIFY_SOURCE=2/-D_FORTIFY_SOURCE=0}"
%endif

%configure --disable-static --with-pic \
%ifarch %arm
            --with-mctx-mth=sjlj --with-mctx-dsp=sjlj --with-mctx-stk=ss \
%endif
            --enable-optimize=yes \
            --enable-pthread=no \
            --with-gnu-ld
make pth_p.h
make %{?_smp_mflags}

%check
make test

%install
%make_install
#empty dependency_libs
rm -f %{buildroot}%{_libdir}/libpth.la

%post   -n %{library_name} -p /sbin/ldconfig

%postun -n %{library_name} -p /sbin/ldconfig

%files -n libpth
%manifest %{name}.manifest
%defattr(-,root,root)
%doc COPYING
%{_libdir}/libpth*.so.*

%files -n libpth-devel
%manifest %{name}.manifest
%defattr(-,root,root)
%{_bindir}/pth-config
%{_includedir}/pth.h
%dir %{_datadir}/aclocal
%{_datadir}/aclocal/pth.m4
%{_libdir}/libpth*.so
%doc %{_mandir}/man1/*
%doc %{_mandir}/man3/*

%changelog
