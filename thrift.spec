%define ver 0.7.0

Name:           thrift 
Version:        %{ver}
Release:        kiwi1
Summary:        facebook thrift
Group:          Development/Languages
License:        Apache Software License
URL:            http://thrift.apache.org/
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source:		http://archive.apache.org/dist/thrift/%{ver}/thrift-%{ver}.tar.gz

BuildRequires:	python python-devel php53 php53-devel boost141-devel openssl-devel libevent-devel

%description 
facebook thrift

#%package erlang
#Requires: erlang
#Summary: thrift erlang
#Group: Development/Languages
#%description erlang

%package python
Requires: python=2.4
Summary: thrift python
Group: Development/Languages
Requires: thrift
%description python

%package php53
Requires: php53
Summary: thrift php53
Group: Development/Languages
Requires: thrift
%description php53

%package fb303
Summary: thrift fb303
Group: Development/Languages
Requires: thrift
%description fb303




%prep
%setup -q

# Fix spurious-executable-perm warning
find tutorial/ -type f -exec chmod 0644 {} \;
chmod a+x configure
chmod a+x lib/php/src/ext/thrift_protocol/build/shtool
chmod a+x lib/erl/rebar
chmod a+x lib/php/src/ext/thrift_protocol/configure
chmod a+x contrib/fb303/bootstrap.sh

%build
rm -rf $RPM_BUILD_ROOT
CPPFLAGS=-I%{_includedir}/boost141 \
LDFLAGS=-L%{_libdir}/boost141 \
  ./configure \
  --prefix=%{_prefix} \
  --with-python --with-php
make
make DESTDIR=$RPM_BUILD_ROOT install

cd contrib/fb303/
CPPFLAGS=-I%{_includedir}/boost141 \
LDFLAGS=-L%{_libdir}/boost141 \
  ./bootstrap.sh

CPPFLAGS=-I%{_includedir}/boost141 \
LDFLAGS=-L%{_libdir}/boost141 \
  ./configure \
  --prefix=%{_prefix} \
  --with-thriftpath=$RPM_BUILD_ROOT/usr
make
make DESTDIR=$RPM_BUILD_ROOT install

%install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_includedir}/*
/usr/lib/lib*
/usr/lib/pkgconfig
%exclude %{_includedir}/thrift/fb303*
%{_bindir}/*

%files fb303
/usr/include/thrift/fb303/*
/usr/share/fb303/*
/usr/lib/python*/site-packages/fb303/*
/usr/lib/python*/site-packages/fb303_scripts/*
/usr/lib/libfb303.a

%files python
%{_libdir}/python*

%files php53
%{_libdir}/php/modules
/usr/lib/php
/etc/php.d

#%files erlang
#%{_libdir}/erlang/

%changelog
* Tue Nov 08 2011 Naresh V. <nareshov@gmail.com> - 0.7.0-kiwi1 
- Initial spec adapted to 0.7.0 based off of SRPMs found from dev.shopex.cn (thanks!)
