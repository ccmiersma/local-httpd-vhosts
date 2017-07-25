%define author Christopher Miersma


%{!?local_prefix:%define local_prefix local}
%if "%{local_prefix}" != "false"
%define _prefix /opt/%{local_prefix}
%define _sysconfdir /etc%{_prefix}
%define _datadir %{_prefix}/share
%define _docdir %{_datadir}/doc
%define _mandir %{_datadir}/man
%define _bindir %{_prefix}/bin
%define _sbindir %{_prefix}/sbin
%define _libdir %{_prefix}/lib
%define _libexecdir %{_prefix}/libexec
%define _includedir %{_prefix}/include
%endif

Name:		local-httpd-vhosts
Version:        0.1.1

Release:        2.local

Summary:	Local Apache httpd name based vhosts
Group:		local
License:	MIT
URL:		https://gitlab.com/ccmiersma/%{name}/
Source0:	%{name}-%{version}.tar.gz
BuildArch:      noarch
Requires:       httpd local-sw-dist
BuildRequires:  pandoc


%description
This package will install name based vhosts into apache's configuration. It adds directories and scripts for managing webapps.


%prep
%setup

%build


echo "Creating man page from README..."

# If a README.md is found, create a man page
if [ -e "README.md" ]; then
  cat README.md | \
  sed -e 1i"\%% %{name}(7)\n\%% %{author} \n\%% $(date +\%B\ \%Y)\n#NAME\n%{name} - %{summary}\n" | \
  pandoc -s -t man - | \
  gzip > %{name}.7.gz
fi

%install

mkdir -p %buildroot%_prefix
mkdir -p %buildroot%_datadir
mkdir -p %buildroot%_docdir
mkdir -p %buildroot%_mandir
mkdir -p %buildroot%_bindir
mkdir -p %buildroot%_sbindir
mkdir -p ${RPM_BUILD_ROOT}%_libdir/scripts
mkdir -p ${RPM_BUILD_ROOT}%_libexecdir 
mkdir -p ${RPM_BUILD_ROOT}%_includedir 
mkdir -p ${RPM_BUILD_ROOT}/etc/httpd/conf.d/local-vhosts.d
mkdir -p ${RPM_BUILD_ROOT}/etc/httpd/conf.d/local-webapps.d
mkdir -p ${RPM_BUILD_ROOT}/var/www/local-vhosts.d
mkdir -p ${RPM_BUILD_ROOT}/var/www/local-webapps.d

mkdir -p ${RPM_BUILD_ROOT}%_mandir/man7


#Pre-config file in sysconfig.
cp local-vhosts.conf ${RPM_BUILD_ROOT}/etc/httpd/conf.d/


cp %{name}.7.gz ${RPM_BUILD_ROOT}%_mandir/man7/

cp README.md %buildroot%_docdir/

#Manually defined files and dirs that need special designation.
#This will end up in the files section.
cat > %{name}-defined-files-list << EOF
%defattr(-,root,root, -)
%dir /etc/httpd/conf.d/local-vhosts.d
%dir /etc/httpd/conf.d/local-webapps.d
%dir /var/www/local-vhosts.d
%dir /var/www/local-webapps.d
%config /etc/httpd/conf.d/local-vhosts.conf
%docdir %{_mandir}
%docdir %{_docdir}
EOF

#Convoluted stuff to combine the manual list above with any new files we find, into a correct list with no duplicates
find %buildroot -type f -o -type l | sed -e "s#${RPM_BUILD_ROOT}##g"|sed -e "s#\(.*\)#\"\1\"#" > %{name}-all-files-list
cat %{name}-defined-files-list | cut -f2 -d' ' | sed -e "s#\(.*\)#\"\1\"#" | sort > %{name}-defined-files-list.tmp
cat %{name}-all-files-list | sort > %{name}-auto-files-list.tmp
diff -e %{name}-defined-files-list.tmp %{name}-auto-files-list.tmp | grep "^\"" > %{name}-auto-files-list
cat %{name}-defined-files-list %{name}-auto-files-list > %{name}-files-list

%clean
%__rm -rf ${RPM_BUILD_ROOT}

%files -f %{name}-files-list


# The post and postun update the man page database
%post

mandb

%postun

mandb

%changelog
* Mon Jul 24 2017 Christopher Miersma <ccmiersma@gmail.com> 0.1.1-2.local
- new package built with tito

* Mon Mar 27 2017 Christopher Miersma - 0.1.0-1
- Initial Release
