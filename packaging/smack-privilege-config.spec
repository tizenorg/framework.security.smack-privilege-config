Name:       smack-privilege-config
Summary:    SMACK rules for libprivilege
Version:    1.0.0.SLP
Release:    1
Group:      System/Security
License:    Apache 2.0
Source0:    %{name}-%{version}.tar.gz
BuildRequires: cmake
Requires:   /usr/bin/chsmack

%description
SMACK rules package to control privilege of in-house application

%prep
%setup -q

%build
%cmake . -DCMAKE_BUILD_TYPE=%{?build_type:%build_type}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/usr/share/license
cp LICENSE %{buildroot}/usr/share/license/%{name}
%make_install

%post

if [ ! -e "/usr/share/privilege-control" ]
then
    mkdir -p /usr/share/privilege-control/
fi

if [ ! -e "/opt/etc/smack-app/accesses.d" ]
then
    mkdir -p /opt/etc/smack-app/accesses.d
fi

%files
%{_datarootdir}/privilege-control/*
/opt/etc/smack/*
%{_datadir}/license/%{name}
