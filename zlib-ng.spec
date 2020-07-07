%global commit fe69810c265858b7b4242663d51336726f4a98be
%global commitdate 20200609
%global shortcommit %(c=%{commit}; echo ${c:0:9})

Name:		zlib-ng
Version:	1.9.9
Release:	0.1.%{commitdate}git%{shortcommit}%{?dist}
Summary:	Zlib replacement with optimizations
License:	zlib
Url:		https://github.com/zlib-ng/zlib-ng
Source0:	https://github.com/zlib-ng/zlib-ng/archive/%{commit}/%{name}-%{shortcommit}.tar.gz

# Be explicit about the soname in order to avoid unintentional changes.
%global soname libz-ng.so.1.9.9

ExclusiveArch:	aarch64 i686 ppc64le s390x x86_64
BuildRequires:	gcc, systemtap-sdt-devel, cmake

%description
zlib-ng is a zlib replacement that provides optimizations for "next generation"
systems.

%package	devel
Summary:	Development files for %{name}
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description	devel
The %{name}-devel package contains static libraries and header files for
developing application that use %{name}.

%prep
%autosetup -p1 -n %{name}-%{commit}

%build
# zlib-ng uses a different macro for library directory.
%cmake . -DWITH_SANITIZERS=ON -DINSTALL_LIB_DIR=%{_libdir}
%make_build

%check
# Tests fail when run in parallel.
ctest -V

%install
%make_install

%files
%{_libdir}/%{soname}
%{_libdir}/libz-ng.so.1
%license LICENSE.md
%doc README.md

%files devel
%{_includedir}/zconf-ng.h
%{_includedir}/zlib-ng.h
%{_libdir}/libz-ng.so
%{_datadir}/pkgconfig/%{name}.pc
# Glob the extension in case the compression changes in the future.
%{_mandir}/man3/%{name}.3.*

%changelog
* Mon Jul 06 2020 Tulio Magno Quites Machado Filho <tuliom@ascii.art.br> - 1.9.9-0.1.20200609gitfe69810c2
- Improve the archive name.
- Starte release at 0.1 as required for prerelease.
- Make the devel package require an arch-dependent runtime subpackage.
- Remove %%ldconfig_scriptlets.
- Glob the man page extension.
- Move unversioned shared library to the devel subpackage

* Wed Jul 01 2020 Tulio Magno Quites Machado Filho <tuliom@ascii.art.br> - 1.9.9-0.20200609gitfe69810c2
- Initial commit
