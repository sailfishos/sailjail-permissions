Name:     sailjail-permissions
Summary:  Permissions definitions for Sailjail
Version:  1.0.0
Release:  1
License:  BSD
URL:      https://github.com/sailfishos/sailjail-permissions
Source0:  %{name}-%{version}.tar.bz2

BuildRequires: qt5-qmake

%define permissions_dir %{_sysconfdir}/sailjail/permissions

%description
%{summary}.

%prep
%setup -q -n %{name}-%{version}

%build
%qmake5
make %{?_smp_mflags}

%install
%qmake5_install

%files
%defattr(-,root,root,-)
%license COPYING
%dir %attr(755,root,root) %{permissions_dir}
%{permissions_dir}/*
