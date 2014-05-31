Name:       smack-privilege-config
Summary:    SMACK rules for libprivilege
Version:    1.0.4.SLP
Release:    1
Group:      System/Security
License:    Apache 2.0
Source0:    %{name}-%{version}.tar.gz
Source1:    %{name}.manifest
BuildRequires: cmake
Requires:   /usr/bin/chsmack

%description
SMACK rules package to control privilege of in-house application

%prep
%setup -q

%build
## Build: Wearable ############################################################
%if "%{_repository}" == "wearable"
ln -s permissions_wearable permissions
cp smack_default_rules_wearable smack_default_rules 

%cmake . -DCMAKE_BUILD_TYPE=%{?build_type:%build_type} \
	-DDEVICE_PROFILE="wearable"
%else
## Build: Mobile ##############################################################

ln -s permissions_mobile permissions
cp smack_default_rules_mobile smack_default_rules

%cmake . -DCMAKE_BUILD_TYPE=%{?build_type:%build_type} \
	-DDEVICE_PROFILE="mobile"
%endif
## Build: END #################################################################

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/usr/share/license
cp LICENSE %{buildroot}/usr/share/license/%{name}
cp -a %{SOURCE1} %{buildroot}%{_datadir}/
%make_install

%post
## Post: Wearable #############################################################
%if "%{_repository}" == "wearable"

if [ ! -e "/usr/share/privilege-control" ]
then
    mkdir -p /usr/share/privilege-control/
fi

if [ ! -e "/opt/etc/smack-app/accesses.d" ]
then
    mkdir -p /opt/etc/smack-app/accesses.d
fi

if which api_feature_loader >/dev/null; then
    api_feature_loader --verbose
else
    echo api_feature_loader not present
fi
%else
## Post: Mobile ###############################################################
if [ ! -e "/usr/share/privilege-control" ]
then
    mkdir -p /usr/share/privilege-control/
fi

if [ ! -e "/opt/etc/smack-app/accesses.d" ]
then
    mkdir -p /opt/etc/smack-app/accesses.d
fi

%endif
## Post: END ##################################################################

%files
## File: Wearable #############################################################
%if "%{_repository}" == "wearable"
%{_datarootdir}/privilege-control/*
/opt/etc/smack/accesses.d/*
%manifest %{_datadir}/%{name}.manifest
%{_datadir}/license/%{name}
%else
## File: Mobile ###############################################################
%{_datarootdir}/privilege-control/*
/opt/etc/smack/*
%{_datadir}/license/%{name}
%manifest %{_datadir}/%{name}.manifest
%endif
## File: END ##################################################################
