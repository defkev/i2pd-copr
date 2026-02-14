Name:          i2pd
Version:       2.59.0
Release:       1%{?dist}
Summary:       I2P router written in C++
Conflicts:     i2pd-git

License:       BSD
URL:           https://github.com/PurpleI2P/i2pd
Source0:       https://github.com/PurpleI2P/i2pd/archive/%{version}/%name-%version.tar.gz

BuildRequires: cmake3

BuildRequires: chrpath
BuildRequires: devtoolset-11-gcc-c++
BuildRequires: zlib-devel
BuildRequires: boost169-devel
BuildRequires: openssl11-devel
BuildRequires: miniupnpc-devel
BuildRequires: systemd-units

Requires:      logrotate
Requires:      systemd
Requires(pre): %{_sbindir}/useradd %{_sbindir}/groupadd


%description
C++ implementation of I2P.


%prep
%setup -q


%build
. /opt/rh/devtoolset-11/enable
cd build
%cmake3 \
  -DWITH_LIBRARY=OFF \
  -DWITH_UPNP=ON \
  -DWITH_HARDENING=ON \
  -DBUILD_SHARED_LIBS:BOOL=OFF \
  -DBOOST_INCLUDEDIR=/usr/include/boost169 \
  -DBOOST_LIBRARYDIR=/usr/lib64/boost169 \
  -DCMAKE_PREFIX_PATH:PATH=/usr/include/openssl11 \
  -DOPENSSL_ROOT_DIR:PATH="%{_includedir}/openssl11;%{_libdir}/openssl11"

make %{?_smp_mflags}

%install
pushd build

chrpath -d i2pd
%{__install} -D -m 755 i2pd %{buildroot}%{_bindir}/i2pd
%{__install} -d -m 755 %{buildroot}%{_datadir}/i2pd
%{__install} -d -m 700 %{buildroot}%{_sharedstatedir}/i2pd
%{__install} -d -m 700 %{buildroot}%{_localstatedir}/log/i2pd
%{__install} -D -m 644 %{_builddir}/%{name}-%{version}/contrib/i2pd.conf %{buildroot}%{_sysconfdir}/i2pd/i2pd.conf
%{__install} -D -m 644 %{_builddir}/%{name}-%{version}/contrib/subscriptions.txt %{buildroot}%{_sysconfdir}/i2pd/subscriptions.txt
%{__install} -D -m 644 %{_builddir}/%{name}-%{version}/contrib/tunnels.conf %{buildroot}%{_sysconfdir}/i2pd/tunnels.conf
%{__install} -D -m 644 %{_builddir}/%{name}-%{version}/contrib/i2pd.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/i2pd
%{__install} -D -m 644 %{_builddir}/%{name}-%{version}/contrib/i2pd.service %{buildroot}%{_unitdir}/i2pd.service
%{__install} -D -m 644 %{_builddir}/%{name}-%{version}/debian/i2pd.1 %{buildroot}%{_mandir}/man1/i2pd.1
%{__cp} -r %{_builddir}/%{name}-%{version}/contrib/certificates/ %{buildroot}%{_datadir}/i2pd/certificates
%{__cp} -r %{_builddir}/%{name}-%{version}/contrib/tunnels.d/ %{buildroot}%{_sysconfdir}/i2pd/tunnels.conf.d
ln -s %{_datadir}/%{name}/certificates %{buildroot}%{_sharedstatedir}/i2pd/certificates


%pre
getent group i2pd >/dev/null || %{_sbindir}/groupadd -r i2pd
getent passwd i2pd >/dev/null || \
  %{_sbindir}/useradd -r -g i2pd -s %{_sbindir}/nologin \
                      -d %{_sharedstatedir}/i2pd -c 'I2P Service' i2pd


%post
%systemd_post i2pd.service


%preun
%systemd_preun i2pd.service


%postun
%systemd_postun_with_restart i2pd.service


%files
%doc LICENSE README.md contrib/i2pd.conf contrib/subscriptions.txt contrib/tunnels.conf contrib/tunnels.d
%{_bindir}/i2pd
%config(noreplace) %{_sysconfdir}/i2pd/*.conf
%config(noreplace) %{_sysconfdir}/i2pd/tunnels.conf.d/*.conf
%config %{_sysconfdir}/i2pd/subscriptions.txt
%doc %{_sysconfdir}/i2pd/tunnels.conf.d/README
%{_sysconfdir}/logrotate.d/i2pd
%{_unitdir}/i2pd.service
%{_mandir}/man1/i2pd.1*
%dir %attr(0700,i2pd,i2pd) %{_sharedstatedir}/i2pd
%dir %attr(0700,i2pd,i2pd) %{_localstatedir}/log/i2pd
%{_datadir}/i2pd/certificates
%{_sharedstatedir}/i2pd/certificates


%changelog
%autochangelog