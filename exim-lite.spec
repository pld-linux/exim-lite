%define		orig_name exim
Summary:	Lite version of exim Mail Transfer Agent
Summary(pl):	Lekka wersja Agenta Transferu Poczty
Name:		exim-lite
Version:	4.43
Release:	0.2
Epoch:		2
License:	GPL
Group:		Networking/Daemons
Source0:	ftp://ftp.csx.cam.ac.uk/pub/software/email/exim/exim4/%{orig_name}-%{version}.tar.bz2
# Source0-md5:	f8f646d4920660cb5579becd9265a3bf
Source1:	ftp://ftp.csx.cam.ac.uk/pub/software/email/exim/exim4/%{orig_name}-texinfo-4.40.tar.bz2
# Source1-md5:	cc91bd804ee0f7fd70991e2e6b529033
Source2:	%{orig_name}.init
Source3:	%{orig_name}.cron.db
Source4:	%{orig_name}4.conf
Source5:	analyse-log-errors
Source6:	%{orig_name}on.desktop
# 20021016: http://www.logic.univie.ac.at/~ametzler/debian/exim4manpages/
Source7:	%{orig_name}4-man-021016.tar.bz2
# Source7-md5:	b552704ebf853a401946038a2b7e8e98
Source9:	%{orig_name}.aliases
Source10:	newaliases
Source11:	%{orig_name}.logrotate
Source12:	%{orig_name}.sysconfig
Source13:	ftp://ftp.csx.cam.ac.uk/pub/software/email/exim/exim4/FAQ.txt.bz2
# Source13-md5:	7c695675e5e60693916b787001252d56
Source14:	ftp://ftp.csx.cam.ac.uk/pub/software/email/exim/exim4/config.samples.tar.bz2
# Source14-md5:	42c7d5c02d06fdd3d8b6ba124ad9fd05
Source15:	%{orig_name}4-smtp.pamd
Source16:	%{orig_name}on.png
Patch0:		%{orig_name}4-EDITME.patch
Patch1:		%{orig_name}4-monitor-EDITME.patch
Patch2:		%{orig_name}4-texinfo.patch
Patch3:		%{orig_name}4-use_system_pcre.patch
Patch4:		%{orig_name}4-Makefile-Default.patch
Patch5:		%{orig_name}4-exiscan-pld.patch
URL:		http://www.exim.org/
BuildRequires:	XFree86-devel
BuildRequires:	db-devel
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	pam-devel
BuildRequires:	pcre-devel
BuildRequires:	perl-devel >= 1:5.6.0
BuildRequires:	readline-devel
BuildRequires:	rpmbuild(macros) >= 1.159
BuildRequires:	texinfo
PreReq:		rc-scripts
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(post):	fileutils
Requires(post):	/bin/hostname
Requires(post,preun):	/sbin/chkconfig
Requires:	pam >= 0.77.3
Requires:	perl(DynaLoader) = %(%{__perl} -MDynaLoader -e 'print DynaLoader->VERSION')
Provides:	group(exim)
Provides:	smtpdaemon
Provides:	user(exim)
Provides:	exim
Obsoletes:	courier
Obsoletes:	masqmail
Obsoletes:	nullmailer
Obsoletes:	omta
Obsoletes:	postfix
Obsoletes:	qmail
Obsoletes:	qmail-client
Obsoletes:	sendmail
Obsoletes:	sendmail-cf
Obsoletes:	sendmail-doc
Obsoletes:	smail
Obsoletes:	smtpdaemon
Obsoletes:	ssmtp
Obsoletes:	zmailer
Obsoletes:	exim
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Smail like Mail Transfer Agent with single configuration file.
Features: flexible retry algorithms, header & envelope rewriting,
multiple deliveries down single connection or multiple deliveries in
parallel, regular expressions in configuration parameters, file
lookups, supports sender and/or reciever verification, selective
relaying, supports virtual domains, built-in mail filtering and can be
configured to drop root privilleges when possible.

%description -l pl
Agent transferu poczty (MTA) z pojedynczym plikiem konfiguracyjnym.
Jego zalety: ¶wietne algorytmy, mo¿liwo¶æ przepisywania nag³ówków &
koperty, wielokrotne dostarczanie poczty podczas jednego po³±czenia
lub równoleg³e dostarczanie poczty, wyra¿enia regularne w parametrach
konfiguracyjnych, weryfikacja nadawcy i/lub odbiorcy, selektywne
relayowanie, wsparcie dla wirtualnych domen, wbudowany system filtrów,
mo¿liwo¶æ odrzucania praw roota kiedy jest to mo¿liwe.

%package X11
Summary:	X11 based Exim administration tool
Summary(pl):	Narzêdzia administracyjne exima dla X11
Summary(pt_BR):	Monitor X11 para o exim
Group:		X11/Applications

%description X11
X11 based monitor & administration utility for the Exim Mail Transfer
Agent.

%description X11 -l pl
Bazuj±ce na X11 narzêdzia dla Exima - monitor i program
administracyjny.

%prep
%setup -n %{orig_name}-%{version} -q -a1 -a7
%patch0 -p1
%patch1 -p1
%patch2 -p0
%patch3 -p1
%patch4 -p1
%patch5 -p0

install %{SOURCE13} doc/FAQ.txt.bz2
install %{SOURCE14} doc/config.samples.tar.bz2

install -d Local
cp -f src/EDITME Local/Makefile
cp -f exim_monitor/EDITME Local/eximon.conf

%build

%{__make} -j1 \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}" \
	LOOKUP_CDB=yes \
	XLFLAGS=-L%{_prefix}/X11R6/%{_lib} \
	X11_LD_LIB=%{_prefix}/X11R6/%{_lib} \
	LOOKUP_LIBS="" \
	LOOKUP_INCLUDE=""

makeinfo --force exim-texinfo-*/doc/*.texinfo

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/mail
install -d $RPM_BUILD_ROOT/etc/{cron.{daily,weekly},logrotate.d,rc.d/init.d,sysconfig,pam.d}
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_mandir}/man8,/usr/lib}
install -d $RPM_BUILD_ROOT%{_var}/{spool/exim/{db,input,msglog},log/{archiv,}/exim,mail}
install -d $RPM_BUILD_ROOT{%{_infodir},%{_desktopdir},%{_pixmapsdir}}

install build-Linux-*/exim{,_fixdb,_tidydb,_dbmbuild,on.bin,_dumpdb,_lock} \
	build-Linux-*/exi{cyclog,next,what} %{SOURCE10} \
	build-Linux-*/{exigrep,eximstats,exiqsumm,convert4r4} \
	util/unknownuser.sh \
	$RPM_BUILD_ROOT%{_bindir}
install build-Linux-*/eximon.bin $RPM_BUILD_ROOT%{_bindir}
install build-Linux-*/eximon $RPM_BUILD_ROOT%{_bindir}

install %{SOURCE5} .
install %{SOURCE3} $RPM_BUILD_ROOT/etc/cron.weekly
install %{SOURCE12} $RPM_BUILD_ROOT/etc/sysconfig/%{orig_name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{orig_name}
install	%{SOURCE11} $RPM_BUILD_ROOT/etc/logrotate.d/%{orig_name}
install %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/mail/exim.conf
install {doc,man}/*.8 $RPM_BUILD_ROOT%{_mandir}/man8
install %{SOURCE9} $RPM_BUILD_ROOT%{_sysconfdir}/mail/aliases
install	*.info* $RPM_BUILD_ROOT%{_infodir}
install %{SOURCE15} $RPM_BUILD_ROOT/etc/pam.d/smtp

ln -sf %{_bindir}/exim $RPM_BUILD_ROOT%{_sbindir}/sendmail
ln -sf %{_bindir}/exim $RPM_BUILD_ROOT/usr/lib/sendmail
ln -sf %{_bindir}/exim $RPM_BUILD_ROOT%{_sbindir}/mailq
ln -sf %{_bindir}/exim $RPM_BUILD_ROOT%{_sbindir}/rsmtp
ln -sf %{_bindir}/exim $RPM_BUILD_ROOT%{_sbindir}/rmail
ln -sf %{_bindir}/exim $RPM_BUILD_ROOT%{_sbindir}/runq

install %{SOURCE6} $RPM_BUILD_ROOT%{_desktopdir}
install %{SOURCE16} $RPM_BUILD_ROOT%{_pixmapsdir}

touch $RPM_BUILD_ROOT%{_var}/log/exim/{main,reject,panic,process}.log

%clean
rm -rf $RPM_BUILD_ROOT

%pre
if [ -n "`/usr/bin/getgid exim`" ]; then
	if [ "`/usr/bin/getgid exim`" != 79 ]; then
		echo "Warning: group exim haven't gid=79. Correct this before installing exim" 1>&2
		exit 1
	fi
else
	/usr/sbin/groupadd -g 79 exim 1>&2
fi

if [ -n "`/bin/id -u exim 2>/dev/null`" ]; then
	if [ "`/bin/id -u exim`" != 79 ]; then
		echo "Warning: user exim doesn't have uid=79. Correct this before installing exim" 1>&2
		exit 1
	fi
else
	/usr/sbin/useradd -u 79 -d /var/spool/exim -s /bin/false \
		-c "Exim pseudo user" -g exim exim 1>&2
fi

%post
umask 022
/sbin/chkconfig --add %{orig_name}
if [ -f /var/lock/subsys/exim ]; then
	/etc/rc.d/init.d/%{orig_name} restart >&2
else
	echo "Run \"/etc/rc.d/init.d/%{orig_name} start\" to start exim daemon."
fi

if [ ! -f /etc/mail/mailname ]; then
	rm -f /etc/mail/mailname && hostname -f > /etc/mail/mailname
	chmod 644 /etc/mail/mailname
fi
newaliases
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/exim ]; then
		/etc/rc.d/init.d/exim stop >&2
	fi
	/sbin/chkconfig --del %{orig_name}
fi

%postun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1
if [ "$1" = "0" ]; then
	%userremove exim
	%groupremove exim
fi

%triggerpostun -- exim < 3.90
if [ -f /etc/mail/exim.conf ]; then
	umask 022
	mv /etc/mail/exim.conf /etc/mail/exim.conf.3
	/usr/bin/convert4r4 < /etc/mail/exim.conf.3 > /etc/mail/exim.conf
fi

%files
%defattr(644,root,root,755)
%doc README* NOTICE LICENCE analyse-log-errors doc/{ChangeLog,NewStuff,dbm.discuss.txt,filter.txt,spec.txt,Exim*.upgrade,OptionLists.txt%{?with_exiscan:,exiscan-*.txt}} build-Linux-*/transport-filter.pl
%dir %{_sysconfdir}/mail
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mail/exim.conf
%{?with_saexim:%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mail/sa-exim.conf}
%attr(644,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mail/aliases
%attr(644,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/exim
%attr(644,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/exim
%attr(754,root,root) /etc/rc.d/init.d/exim
%attr(4755,root,root) %{_bindir}/exim
%attr(770,root,exim) %dir %{_var}/spool/exim
%attr(750,exim,exim) %dir %{_var}/spool/exim/db
%attr(700,exim,root) %dir %{_var}/spool/exim/input
%attr(750,exim,root) %dir %{_var}/spool/exim/msglog
%attr(755,root,root) %{_bindir}/exim_*
%attr(755,root,root) %{_bindir}/exinext
%attr(755,root,root) %{_bindir}/exiwhat
%attr(755,root,root) %{_bindir}/exicyclog
%attr(755,root,root) %{_bindir}/exigrep
%attr(755,root,root) %{_bindir}/eximstats
%attr(755,root,root) %{_bindir}/exiqsumm
%attr(755,root,root) %{_bindir}/unknownuser.sh
%attr(755,root,root) %{_bindir}/newaliases
%attr(755,root,root) %{_bindir}/convert4r4
%attr(755,root,root) %{_sbindir}/mailq
%attr(755,root,root) %{_sbindir}/rmail
%attr(755,root,root) %{_sbindir}/rsmtp
%attr(755,root,root) %{_sbindir}/runq
%attr(755,root,root) %{_sbindir}/sendmail
%attr(755,root,root) /usr/lib/sendmail
%attr(754,root,root) /etc/cron.weekly/exim.cron.db
%attr(750,exim,root) %dir %{_var}/log/exim
%attr(750,exim,root) %dir %{_var}/log/archiv/exim
%attr(640,exim,root) %ghost %{_var}/log/exim/*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/smtp
%{_infodir}/*.info*
%{_mandir}/man8/*

%files X11
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/eximon
%attr(755,root,root) %{_bindir}/eximon.bin
%{_desktopdir}/eximon.desktop
%{_pixmapsdir}/eximon.png
