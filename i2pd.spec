Name:          i2pd
Version:       2.58.0
Release:       %autorelease
Summary:       I2P router written in C++
Conflicts:     i2pd-git

License:       BSD
URL:           https://github.com/PurpleI2P/i2pd
Source0:       https://github.com/PurpleI2P/i2pd/archive/%{version}/%name-%version.tar.gz
Source1:       i2pd.sysusers.conf

BuildRequires: cmake3

BuildRequires: gcc-c++
BuildRequires: zlib-devel
BuildRequires: boost-devel
BuildRequires: openssl-devel
BuildRequires: miniupnpc-devel
BuildRequires: systemd-units

%if 0%{?fedora} == 41
BuildRequires: openssl-devel-engine
%endif

Requires:      logrotate
Requires:      systemd


%description
C++ implementation of I2P.


%prep
%setup -q

sed -i '0,/endif.*/s//endif\(\)\nlist\(APPEND CMAKE_INSTALL_RPATH "${CMAKE_INSTALL_LIBDIR}"\)/' build/CMakeLists.txt

%build
cd build
%cmake3 \
  -DCMAKE_INSTALL_LIBDIR="%{_libdir}/i2pd" \
  -DWITH_UPNP=ON \
  -DWITH_HARDENING=ON
%cmake_build


%install
pushd build
%cmake_install
popd

%{__install} -d -m 700 %{buildroot}%{_sharedstatedir}/i2pd
%{__install} -d -m 700 %{buildroot}%{_localstatedir}/log/i2pd
%{__install} -d -m 755 %{buildroot}%{_prefix}/lib/sysusers.d
%{__install} -D -m 644 contrib/i2pd.conf %{buildroot}%{_sysconfdir}/i2pd/i2pd.conf
%{__install} -D -m 644 contrib/subscriptions.txt %{buildroot}%{_sysconfdir}/i2pd/subscriptions.txt
%{__install} -D -m 644 contrib/tunnels.conf %{buildroot}%{_sysconfdir}/i2pd/tunnels.conf
%{__install} -D -m 644 contrib/i2pd.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/i2pd
%{__install} -D -m 644 contrib/i2pd.service %{buildroot}%{_unitdir}/i2pd.service
%{__install} -D -m 644 debian/i2pd.1 %{buildroot}%{_mandir}/man1/i2pd.1
%{__install} -D -m 644 %{SOURCE1} %{buildroot}%{_prefix}/lib/sysusers.d/i2pd.conf
mkdir -p %{buildroot}%{_datadir}/i2pd
%{__cp} -r contrib/certificates/ %{buildroot}%{_datadir}/i2pd/certificates
mkdir -p %{buildroot}%{_sysconfdir}/i2pd
%{__cp} -r contrib/tunnels.d/ %{buildroot}%{_sysconfdir}/i2pd/tunnels.conf.d
ln -s %{_datadir}/%{name}/certificates %{buildroot}%{_sharedstatedir}/i2pd/certificates


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
%{_prefix}/lib/sysusers.d/i2pd.conf
%{_sysconfdir}/logrotate.d/i2pd
%{_unitdir}/i2pd.service
%{_mandir}/man1/i2pd.1*
%dir %attr(0700,i2pd,i2pd) %{_sharedstatedir}/i2pd
%dir %attr(0700,i2pd,i2pd) %{_localstatedir}/log/i2pd
%{_datadir}/i2pd/certificates
%{_sharedstatedir}/i2pd/certificates
%{_libdir}/i2pd/*.so


%changelog
%autochangelog
