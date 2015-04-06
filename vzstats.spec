Summary:	OpenVZ stats collection daemon
Summary(pl.UTF-8):	Demon do zbierania statystyk OpenVZ
Name:		vzstats
Version:	0.5
Release:	1
License:	GPL v2+
Group:		Applications/System
Source0:	http://download.openvz.org/utils/vzstats/%{version}/src/%{name}-%{version}.tar.bz2
# Source0-md5:	71f524032ab4dc935808274c620a925e
URL:		http://stats.openvz.org/
Requires:	curl
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is an OpenVZ component to gather OpenVZ usage and hardware
statistics, in order to improve the project.

Statistics gathered and reported include the following:
1) Hardware info:
 - CPU, disk, memory/swap
2) Software info:
 - host distribution, versions of OpenVZ components, kernel version
3) Containers info:
 - number of containers existing/running/using ploop/using vswap
 - OS templates of containers.

For more details, check the scripts in %{_libexecdir}/vzstats
directory.

All submissions are anonymous and are not including IP or MAC
addresses, hostnames etc. Global data are available at
<http://stats.openvz.org/>.

%description -l pl.UTF-8
Ten komponent OpenVZ służy do zbierania statystyk wykorzystania OpenVZ
oraz sprzętu w celu poprawienia jakości projektu.

Zbeirane i zgłaszane statystyki obejmują następujące informacje:
1) Informacje o sprzęcie:
- CPU, dysk, pamięć/swap
2) Informacje o oprogramowaniu:
 - dystrybucja, wersje komponentów OpenVZ, wersja jądra
3) Informacje o kontenerach:
 - liczba kontenerów istniejących/działających/wykorzystujecych ploop/
   wykorzystujących vswap
 - szablony systemów operacyjnych kontenerów.

Więcej szczegółów można znaleźć w skryptach w katalogu
%{_libexecdir}/vzstats.

Informacje są wysyłane anonimowo i nie zawierają adresów IP ani MAC,
nazw hostów itp. Dane globalne są dostępne pod adresem
<http://stats.openvz.org/>.

%package -n bash-completion-vzstats
Summary:	Bash completion for vzstats
Summary(pl.UTF-8):	Bashowe uzupełnianie parametrów dla polecenia vzstats
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	bash-completion

%description -n bash-completion-vzstats
Bash completion for vzstats.

%description -n bash-completion-vzstats -l pl.UTF-8
Bashowe uzupełnianie parametrów dla polecenia vzstats.

%prep
%setup -q

%build
%{__make} \
	REPDIR=%{_libexecdir}/%{name}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install-all \
	DESTDIR=$RPM_BUILD_ROOT \
	REPDIR=%{_libexecdir}/%{name}

touch $RPM_BUILD_ROOT%{_sysconfdir}/vz/.vzstats-uuid

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- vzctl,vzctl-lib,vzquota,ploop,ploop-libs
%{_sbindir}/vzstats &

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_sbindir}/vzstats
%{_mandir}/man8/vzstats.8*
%dir %{_sysconfdir}/vz
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/vz/vzstats.conf
%{_sysconfdir}/vz/EssentialSSLCA_2.crt
%ghost %{_sysconfdir}/vz/.vzstats-uuid
%dir %{_libexecdir}/%{name}
%attr(755,root,root) %{_libexecdir}/%{name}/*
%attr(755,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/cron.monthly/vzstats

%files -n bash-completion-vzstats
%defattr(644,root,root,755)
%{_sysconfdir}/bash_completion.d/vzstats
