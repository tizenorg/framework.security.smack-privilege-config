Name:       smack-privilege-config
Summary:    SMACK rules for libprivilege
Version:    1.0.8
Release:    1
Group:      System/Security
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1:    %{name}.manifest
BuildRequires: cmake
Requires:   /usr/bin/chsmack

%description
SMACK rules package to control privilege of in-house application

%prep
%setup -q

%build
%if %{?tizen_profile_name} == "wearable"
        __PROFILE_TYPE="WEARABLE"
%elseif %{?tizen_profile_name} == "mobile"
        __PROFILE_TYPE="MOBILE"
%endif

%cmake . -DCMAKE_BUILD_TYPE=%{?build_type:%build_type} \
	 -DPROFILE_TYPE="${__PROFILE_TYPE}"

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/usr/share/license
mkdir -p %{buildroot}/usr/share/privilege-control
mkdir -p %{buildroot}/etc/smack-app/accesses.d
cp LICENSE %{buildroot}/usr/share/license/%{name}
cp -a %{SOURCE1} %{buildroot}%{_datadir}/
%make_install

%post
if which api_feature_loader >/dev/null; then
    api_feature_loader --verbose
else
    echo api_feature_loader not present
fi

%files
%{_datarootdir}/privilege-control/*
%{_sysconfdir}/smack/accesses.d/*
%manifest %{_datadir}/%{name}.manifest
%{_datadir}/license/%{name}
%dir %{_datadir}/privilege-control
%dir /etc/smack-app/accesses.d
