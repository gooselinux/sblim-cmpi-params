%define tog_pegasus_version 2:2.6.1-1
%define provider_dir %{_libdir}/cmpi

Name:           sblim-cmpi-params
Version:        1.3.0
Release:        1%{?dist}
Summary:        SBLIM params instrumentation

Group:          Applications/System
License:        EPL
URL:            http://sblim.wiki.sourceforge.net/
Source0:        http://downloads.sourceforge.net/sblim/%{name}-%{version}.tar.bz2
Patch0:         sblim-cmpi-params-1.2.4-no-abi-params.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  tog-pegasus-devel >= %{tog_pegasus_version}
BuildRequires:  sblim-cmpi-base-devel
Requires:       tog-pegasus >= %{tog_pegasus_version}
Requires:       sblim-cmpi-base

%description
Standards Based Linux Instrumentation Params Providers

%package        test
Summary:        SBLIM Params Instrumentation Testcases
Group:          Applications/System
Requires:       sblim-cmpi-params = %{version}-%{release}
Requires:       sblim-testsuite
Requires:       tog-pegasus

%description -n sblim-cmpi-params-test
SBLIM Base Params Testcase Files for SBLIM Testsuite

%prep
%setup -q
%patch0 -p1 -b .no-abi-params

%build
%configure \
        TESTSUITEDIR=%{_datadir}/sblim-testsuite \
        CIMSERVER=pegasus \
        PROVIDERDIR=%{provider_dir}
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
# remove unused libtool files
rm -f $RPM_BUILD_ROOT/%{_libdir}/*a
rm -f $RPM_BUILD_ROOT/%{provider_dir}/*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,0755)
%{provider_dir}/*Parameter.so*
%{_datadir}/%{name}
%docdir %{_datadir}/doc/%{name}-%{version}
%{_datadir}/doc/%{name}-%{version}

%files test
%defattr(-,root,root,0755)
%{_datadir}/sblim-testsuite/sblim-cmpi-params-test.sh
%{_datadir}/sblim-testsuite/cim/Linux_*Parameter.cim
%{_datadir}/sblim-testsuite/system/linux/Linux_*Parameter.system
%{_datadir}/sblim-testsuite/system/linux/Linux_*Parameter.sh

%define PARAMS_SCHEMA %{_datadir}/sblim-cmpi-params/Linux_ABIParameter.mof %{_datadir}/sblim-cmpi-params/Linux_FileSystemParameter.mof  %{_datadir}/sblim-cmpi-params/Linux_KernelParameter.mof %{_datadir}/sblim-cmpi-params/Linux_NetworkCoreParameter.mof %{_datadir}/sblim-cmpi-params/Linux_NetworkIPv4Parameter.mof %{_datadir}/sblim-cmpi-params/Linux_NetworkUnixParameter.mof  %{_datadir}/sblim-cmpi-params/Linux_VirtualMemoryParameter.mof
%define PARAMS_REGISTRATION %{_datadir}/sblim-cmpi-params/Linux_ABIParameter.registration %{_datadir}/sblim-cmpi-params/Linux_FileSystemParameter.registration  %{_datadir}/sblim-cmpi-params/Linux_KernelParameter.registration %{_datadir}/sblim-cmpi-params/Linux_NetworkCoreParameter.registration %{_datadir}/sblim-cmpi-params/Linux_NetworkIPv4Parameter.registration \%{_datadir}/sblim-cmpi-params/Linux_NetworkUnixParameter.registration %{_datadir}/sblim-cmpi-params/Linux_VirtualMemoryParameter.registration

%pre
if [ $1 -gt 1 ]; then
  %{_datadir}/sblim-cmpi-params/provider-register.sh -d \
        -t pegasus -r %{PARAMS_REGISTRATION} -m %{PARAMS_SCHEMA} > /dev/null 2>&1 || :;
fi

%post
/sbin/ldconfig
if [ $1 -ge 1 ]; then
   %{_datadir}/sblim-cmpi-params/provider-register.sh \
        -t pegasus -r %{PARAMS_REGISTRATION} -m %{PARAMS_SCHEMA} > /dev/null 2>&1 || :;
fi

%preun
if [ $1 -eq 0 ]; then
   %{_datadir}/sblim-cmpi-params/provider-register.sh -d \
        -t pegasus -r %{PARAMS_REGISTRATION} -m %{PARAMS_SCHEMA} > /dev/null 2>&1 || :;
fi

%postun -p /sbin/ldconfig

%changelog
* Wed Jun 30 2010 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.3.0-1
- Update to sblim-cmpi-params-1.3.0

* Mon Jun  1 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.2.6-1
- Initial support
