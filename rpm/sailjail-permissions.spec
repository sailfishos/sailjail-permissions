Name:     sailjail-permissions
Summary:  Permissions definitions for Sailjail
Version:  1.0.0
Release:  1
License:  BSD
URL:      https://github.com/sailfishos/sailjail-permissions
Source0:  %{name}-%{version}.tar.bz2

BuildRequires: qt5-qmake
BuildRequires: qt5-qttools-linguist
BuildRequires: python3-base

%define permissions_dir %{_sysconfdir}/sailjail/permissions
%define config_dir %{_sysconfdir}/sailjail/config

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
%dir %attr(755,root,root) %{config_dir}
%{config_dir}/*
%{_datadir}/translations/*.qm

%package ts-devel
Summary: Translation source for %{name}

%description ts-devel
%{summary}.

%files ts-devel
%{_datadir}/translations/source/*.ts
