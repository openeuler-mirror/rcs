Summary: Revision Control System (RCS) file version management tools
Name: rcs
Version: 5.9.4
Release: 13
License: GPLv3+
URL: http://www.gnu.org/software/rcs/
Source: ftp://ftp.gnu.org/gnu/rcs/%{name}-%{version}.tar.xz
Patch0: rcs-5.8-build-tweaks.patch
Patch1: rcs-5.9.4-t810_disable.patch
Patch6000: backport-rcs-5.9.4-SIGSTKSZ.patch

Provides: bundled(gnulib)
BuildRequires:  gcc autoconf groff ghostscript ed texinfo
Requires: diffutils
Requires(post): /sbin/install-info
Requires(postun): /sbin/install-info

%description
The Revision Control System (RCS) is a system for managing multiple
versions of files.  RCS automates the storage, retrieval, logging,
identification and merging of file revisions.  RCS is useful for text
files that are revised frequently (for example, programs,
documentation, graphics, papers and form letters).

The rcs package should be installed if you need a system for managing
different versions of files.

%package_help

%prep
%autosetup -n %{name}-%{version} -p1
autoconf

%build
%if "%{version}" <= "5.9.4"
CFLAGS="${RPM_OPT_FLAGS} -std=c99"
%endif
%configure --with-diffutils
%make_build

%install
%make_install
install -m 755 src/rcsfreeze $RPM_BUILD_ROOT%{_bindir}
rm -f $RPM_BUILD_ROOT/%{_infodir}/dir

%check
make check XFAIL_TESTS="`tests/known-failures %{version}`"

%post
/sbin/install-info %{_infodir}/%{name}.info.gz %{_infodir}/dir 2>/dev/null || :

%postun
if [ $1 -eq 0 ]; then
  /sbin/install-info --delete %{_infodir}/%{name}.info.gz %{_infodir}/dir 2>/dev/null || :
fi

%files
%doc ChangeLog COPYING THANKS NEWS README
%{_bindir}/*
%{_infodir}/*

%files help
%{_mandir}/man[15]/*

%changelog
* Tue Aug 10 2021 shixuantong <shixuantong@huawei.com> - 5.9.4-13
- fix build fail for SIGSTKSZ

* Mon Jun 28 2021 shangyibin <shangyibin1@openeuler.org> - 5.9.4-12
- %perp no longer patched with git

* Wed Feb 12 2020 openEuler Buildteam <buildteam@openeuler.org> - 5.9.4-11
- Package init

