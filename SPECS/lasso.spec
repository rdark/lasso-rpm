%{!?python_sitearch: %define python_sitearch %(%{__python} -c 'from distutils import sysconfig; print sysconfig.get_python_lib(1)')}

%define with_java %{?_without_java: 0} %{?!_without_java: 1}
%define with_php %{?_without_php: 0} %{?!_without_php: 1}
%define with_python %{?_without_python: 0} %{?!_without_python: 1}
%define with_wsf %{?_without_wsf: 0} %{?!_without_wsf: 1}
%define with_perl %{?_without_perl: 0} %{?!_without_perl: 1}

%define with_java 0
%define with_php 0
%define with_python 0
%define with_wsf 0
%define with_perl 0

Summary: Liberty Alliance Single Sign On
Name: lasso
Version: 2.4.1
Release: 1%{?dist}
License: GPL
Group: System Environment/Libraries
Source: https://dev.entrouvert.org/releases/lasso/lasso-%{version}.tar.gz
Buildroot: %{_tmppath}/%{name}-%{version}-%(id -u -n)
%if %{with_wsf}
BuildRequires: cyrus-sasl-devel
%endif
BuildRequires: glib2-devel, tar, libtool-ltdl-devel
BuildRequires: libxml2-devel, xmlsec1-devel >= 1.2.6
BuildRequires: openssl-devel, xmlsec1-openssl-devel >= 1.2.6
Requires: libxml2, xmlsec1 >= 1.2.6
Requires: openssl, xmlsec1-openssl >= 1.2.6
Url: http://lasso.entrouvert.org/

%description
Lasso is the first GPLed implementation library of the Liberty Alliance standards.

Lasso allows to manage the federation of scattered identities and Single Sign On.
Using Lasso and respecting the Liberty Alliance standards, is the way to couple
the needs for a strong authentication with an absolute respect of the users private life.

%package devel
Summary: Header files and libraries for %{name} development.
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: libxml2-devel, libxslt-devel, pkgconfig, xmlsec1-devel
Requires: glib2-devel

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

%if %{with_perl}
%package perl
Summary: Perl Bindings for %{name}
Group: Development/Libraries
BuildRequires: perl(ExtUtils::MakeMaker)
Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires: %{name} = %{version}-%{release}
Obsoletes: perl-%{name} < %{version}-%{release}
Provides: perl-%{name} = %{version}-%{release}

%description perl
The %{name}-perl package contains a module that permits applications
written in Perl programming language to use the interface
supplied by %{name}.
%endif

%if %{with_java}
%package java
Summary: Java module for %{name}
Group: Development/Libraries
BuildRequires: java-devel >= 1.4.2
BuildRequires: python-lxml
Requires: jre-gcj >= 1.4.2, jpackage-utils >= 1.5
Requires: %{name} = %{version}-%{release}
Obsoletes: java-%{name} < %{version}-%{release}
Provides: java-%{name} = %{version}-%{release}

%description java
The %{name}-java package contains a module that permits applications
written in Java programming language to use the interface
supplied by %{name}.
%endif

%if %{with_php}
%package php
Summary: PHP module for %{name}
Group: Development/Libraries
BuildRequires: php-devel >= 5.0, expat-devel
BuildRequires: python-lxml
Requires: php >= 5.0
Requires: %{name} = %{version}-%{release}
Obsoletes: php-%{name} < %{version}-%{release}
Provides: php-%{name} = %{version}-%{release}

%description php
The %{name}-php package contains a module that permits applications
written in PHP programming language to use the interface
supplied by %{name}.
%endif

%if %{with_python}
%package python
Summary: Python Bindings for %{name}
Group: Development/Libraries
BuildRequires: python-devel
BuildRequires: python-lxml
Requires: python >= 2.0
Requires: %{name} = %{version}-%{release}
Obsoletes: python-%{name} < %{version}-%{release}
Provides: python-%{name} = %{version}-%{release}

%description python
The %{name}-python package contains a module that permits applications
written in the Python programming language to use the interface
supplied by %{name}.
%endif

%prep
%setup -q -n %{name}-%{version}

%build
%configure --prefix=%{_prefix} \
	%if !%{with_java}
	   --disable-java \
	%endif
	%if !%{with_perl}
	   --disable-perl\
	%endif
	%if !%{with_python}
	   --disable-python \
	%endif
	%if %{with_php}
	   --enable-php5=yes \
           --with-php5-config-dir=%{_sysconfdir}/php.d \
	%else
	   --enable-php5=no \
	%endif
	%if %{with_wsf}
           --enable-wsf \
           --with-sasl2=%{_prefix}/sasl2 \
	%endif
	   --with-html-dir=%{_datadir}/gtk-doc/html 
make exec_prefix=%{_prefix} DESTDIR=%{buildroot}

%install
rm -rf %{buildroot}

install -m 755 -d %{buildroot}%{_datadir}/gtk-doc/html

make install exec_prefix=%{_prefix} DESTDIR=%{buildroot}
find %{buildroot} -type f -name '*.la' -exec rm -f {} \;
find %{buildroot} -type f -name '*.a' -exec rm -f {} \;

# Perl subpackage
%if %{with_perl}
find %{buildroot} \( -name perllocal.pod -o -name .packlist \) -exec rm -v {} \;

find %{buildroot}/usr/lib/perl5 -type f -print |
        sed "s@^%{buildroot}@@g" |
        grep -v perllocal.pod |
        grep -v "\.packlist" > %{name}-perl-filelist
if [ "$(cat %{name}-perl-filelist)X" = "X" ] ; then
    echo "ERROR: EMPTY FILE LIST"
    exit -1
fi
%endif

# PHP subpackage
%if %{with_php}
install -m 755 -d %{buildroot}%{_datadir}/php/%{name}
mv %{buildroot}%{_datadir}/php/*.php %{buildroot}%{_datadir}/php/%{name}
%endif

%post
/sbin/ldconfig 2>/dev/null

%postun
/sbin/ldconfig 2>/dev/null

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog COPYING INSTALL NEWS README
%{_libdir}/*.so*

%files devel
%defattr(-,root,root)
%doc %{_defaultdocdir}/%{name}
%doc %{_datadir}/gtk-doc/html/%{name}
%{_libdir}/pkgconfig/lasso.pc
%{_includedir}/%{name}

%if %{with_perl}
%files perl -f %{name}-perl-filelist
%defattr(-,root,root)
%endif

%if %{with_java}
%files java
%defattr(-,root,root)
%{_libdir}/java/*.so
%{_datadir}/java/*.jar
%endif

%if %{with_php}
%files php
%defattr(-,root,root)
%attr(755,root,root) %{_libdir}/php/modules/*
%config(noreplace) %attr(644,root,root) %{_sysconfdir}/php.d/%{name}.ini
%attr(755,root,root) %{_datadir}/php/%{name}/*
%endif

%if %{with_python}
%files python
%defattr(-,root,root)
%{python_sitearch}/*
%endif

%changelog
* Fri Aug 29 2014 Richard Clark <rclark@telnic.org> 2.4.1-1%{?dist}
- Updated to 2.4.1

* Mon Sep 10 2012 Benjamin Dauvergne <bdauvergne@entrouvert.com> 2.3.6-1%{?dist}
- Updated to final 2.3.6
* Mon Jan 10 2011 Jean-Marc Liger <jmliger@siris.sorbonne.fr> 2.3.5-1%{?dist}
- Updated to final 2.3.5
- Removed --enable-gtk-doc, use doc already been built in tarball instead
- Rebuilt on CentOS 5

* Tue Oct 30 2010 Jean-Marc Liger <jmliger@siris.sorbonne.fr> 2.3.4-1%{?dist}
- Updated to final 2.3.4
- Updated g_hash_table patch (Benjamin Dauvergne)
- Removed --with-php5-extension-dir obsolete option
- Removed --enable-php4 obsolete option
- Rebuilt on CentOS 5

* Wed Jan 20 2010 Jean-Marc Liger <jmliger@siris.sorbonne.fr> 2.2.90-1%{?dist}
- Updated to final 2.2.90
- Updated BuildRequires gtk-doc >= 1.9
- Added g_hash_table patch
- Rebuilt on CentOS 4,5

* Wed Jan 20 2010 Jean-Marc Liger <jmliger@siris.sorbonne.fr> 2.2.2-1%{?dist}
- Updated to final 2.2.2 (Imported missing lasso/xml/soap_binding.h from SVN)
- Added patch for glib2 < 2.14
- Added missing BuildRequires perl(ExtUtils::MakeMaker) for perl package
- Rebuilt on CentOS 4,5

* Fri Dec 16 2008 Jean-Marc Liger <jmliger@siris.sorbonne.fr> 2.2.1-2%{?dist}
- Added php5 data files
- Rebuilt on CentOS 4,5 and Fedora 9

* Fri Oct 03 2008 Jean-Marc Liger <jmliger@siris.sorbonne.fr> 2.2.1-1%{?dist}
- Updated to final 2.2.1
- Rebuilt on CentOS 4,5 and Fedora 9

* Mon May 05 2008 Jean-Marc Liger <jmliger@siris.sorbonne.fr> 2.2.0-1%{?dist}
- Updated to final 2.2.0
- Rebuilt on CentOS 4,5 and Fedora 8

* Mon Apr 28 2008 Jean-Marc Liger <jmliger@siris.sorbonne.fr> 2.1.98-1%{?dist}
- Updated to test 2.1.98 (Fix CentOS 4 build)
- Rebuilt on CentOS 4,5 and Fedora 8

* Mon Apr 21 2008 Jean-Marc Liger <jmliger@siris.sorbonne.fr> 2.1.97-1%{?dist}
- Updated to test 2.1.97
- Added missing BuildRequires expat-devel for php package
- Added missing BuildRequires python-devel for python package
- Rebuilt on CentOS 4,5 and Fedora 8

* Tue Apr 08 2008 Jean-Marc Liger <jmliger@siris.sorbonne.fr> 2.1.96-1%{?dist}
- Updated to test 2.1.96 (Fix ElementTree build)
- Added missing BuildRequires python-lxml instead of
  python-elementtree for java, php and python packages
- Added missing BuildRequires glib2-devel
- Added missing BuildRequires cyrus-sasl-devel and
  added conditionnal build support for ID-WSF
- Rebuilt on CentOS 5 and Fedora 8

* Mon Apr 07 2008 Jean-Marc Liger <jmliger@siris.sorbonne.fr> 2.1.95-1%{?dist}
- Updated to test 2.1.95 (Fix ID-WSF changes)
- Changed BuildRequires gcc-java to java-devel
- Rebuilt on CentOS 5

* Wed Apr 02 2008 Jean-Marc Liger <jmliger@siris.sorbonne.fr> 2.1.94-1%{?dist}
- Updated to test 2.1.94 (Fix ID-WSF changes)
- Rebuilt on CentOS 5

* Fri Mar 28 2008 Jean-Marc Liger <jmliger@siris.sorbonne.fr> 2.1.93-1%{?dist}
- Updated to test 2.1.93 (Fix for Java Bindings and WSF changes)
- Rebuilt on CentOS 5

* Fri Mar 14 2008 Jean-Marc Liger <jmliger@siris.sorbonne.fr> 2.1.92-1%{?dist}
- Updated to test 2.1.92 (Fix for Java Bindings)
- Rebuilt on CentOS 5

* Fri Mar 14 2008 Jean-Marc Liger <jmliger@siris.sorbonne.fr> 2.1.91-1%{?dist}
- Updated to test 2.1.91 (Fix for Java Bindings)
- Rebuilt on CentOS 5

* Thu Feb 28 2008 Jean-Marc Liger <jmliger@siris.sorbonne.fr> 2.1.9-1%{?dist}
- Updated to test 2.1.9 (New Java and PHP Bindings !)
- Rebuilt on CentOS 5

* Mon Aug 23 2007 Jean-Marc Liger <jmliger@siris.sorbonne.fr> 2.1.1-1%{?dist}
- Updated to 2.1.1 
- Rebuilt on CentOS 5

* Mon Aug 13 2007 Jean-Marc Liger <jmliger@siris.sorbonne.fr> 2.1.0-1%{?dist}
- Updated to 2.1.0 
- Removed static librairies
- Rebuilt on CentOS 5

* Mon Jan 22 2007 Jean-Marc Liger <jmliger@siris.sorbonne.fr> 2.0.0-1%{?dist}
- Updated to 2.0.0 
- Disabled swig broken support for PHP version 5
- Changed %doc to %{_datadir}/gtk-doc/html/lasso/* in devel subpackage
- Built on Fedora Core 3 / RHEL 4 and Fedora Core 6 / RHEL 5

* Wed Dec 20 2006 Jean-Marc Liger <jmliger@siris.sorbonne.fr> 1.9.9-1
- Updated to test 1.9.9 (SAML 2.0 full support !)
- Changed Provides/Obsoletes to follow new Fedora naming rules
- Choosed BuildRequires to be more OpenSUSE/Mandriva compliant
- Added php_extdir macro to support both PHP version 4 and 5
- Built on Fedora Core 3 / RHEL 4 and Fedora Core 6 / RHEL 5

* Mon Oct 23 2006 Jean-Marc Liger <jmliger@siris.sorbonne.fr> 0.6.6-1
- Updated to 0.6.6
- Added conditional build for java, php, python
- Built on Fedora Core 3 / RHEL 4

* Mon Jun 12 2006 Jean-Marc Liger <jmliger@siris.sorbonne.fr> 0.6.5-1
- First 0.6.5
- Built on Fedora Core 3 / RHEL 4
