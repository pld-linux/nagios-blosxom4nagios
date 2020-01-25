%define		pkg	blosxom4nagios
Summary:	A flexible, powerful RSS/Atom notification handler for Nagios
Name:		nagios-%{pkg}
Version:	0.2.3
Release:	0.3
License:	MIT
Group:		Applications/WWW
Source0:	http://www.openfusion.com.au/labs/dist/%{pkg}-%{version}.tar.gz
# Source0-md5:	bd4b036b7318c63e487d544c2950f525
URL:		http://www.openfusion.net/blosxom/blosxom4nagios
BuildRequires:	rpm-perlprov >= 4.1-13
Requires:	nagios-cgi
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapp		blosxom
%define		_webapps	/etc/webapps
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_libexecdir	%{_prefix}/lib/nagios
%define		appdir		%{_datadir}/nagios/%{_webapp}
%define		cgidir		%{_libdir}/nagios/cgi

%description
Blosxom4Nagios is a special purpose Blosxom instance for handling
Nagios notifications and producing RSS and atom feeds of them, as well
as a pretty web interface. It differs from some of the other
RSS-handlers in that all notifications are 'tagged' with hostnames,
hostgroup names, service names, servicegroup names, etc., allowing you
to slice and dice your views and your feeds however you wish.

%prep
%setup -q -n %{pkg}-%{version}

for a in config/*.dist; do
	mv $a ${a%.dist}
done

mv config/{blosxom4nagios.conf,apache.conf}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{appdir},%{cgidir},%{_libexecdir},/etc/nagios/plugins}

cp -a images lib plugins posts state themes $RPM_BUILD_ROOT%{appdir}
cp -a config/* $RPM_BUILD_ROOT%{_sysconfdir}
cp -p $RPM_BUILD_ROOT%{_sysconfdir}/{apache,httpd}.conf

# cgi
install -p cgi/* $RPM_BUILD_ROOT%{cgidir}

# notify scripts
install -p bin/blosxom-post $RPM_BUILD_ROOT%{_libexecdir}
mv $RPM_BUILD_ROOT{%{_sysconfdir}/commands_blosxom.cfg,/etc/nagios/plugins/blosxom.cfg}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc INSTALL LICENCE README TODO VERSION

# web app
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/blosxom.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/plugin_list.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/atomfeed
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/b4n
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/entries_timestamp
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/metamail
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/rss20
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/tags
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/theme

%attr(755,root,root) %{cgidir}/%{_webapp}.cgi

%{appdir}

# notify command
%attr(640,root,nagios) %config(noreplace) %verify(not md5 mtime size) /etc/nagios/plugins/blosxom.cfg
%attr(755,root,root) %{_libexecdir}/blosxom-post
