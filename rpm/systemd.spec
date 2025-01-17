%global pkgdir %{_prefix}/lib/systemd
%global system_unit_dir %{pkgdir}/system
%global user_unit_dir %{pkgdir}/user

Name:           systemd
Url:            https://www.freedesktop.org/wiki/Software/systemd
Version:        238
Release:        1
# For a breakdown of the licensing, see README
License:        LGPLv2+ and MIT and GPLv2+
Summary:        A System and Service Manager

Source0:        https://github.com/systemd/systemd/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source2:        tests.xml
Source3:        systemctl-user
# We need to disable false positive rpmlint's error in systemd.pc.
# Can be removed after fixing: https://bugs.merproject.org/show_bug.cgi?id=1341
Source4:        systemd-rpmlintrc

Patch0:         systemd-208-video.patch
Patch2:         systemd-187-remove-display-manager.service.patch
Patch8:         systemd-208-count-only-restarts.patch
Patch9:         systemd-208-do-not-pull-4-megs-from-stack-for-journal-send-test.patch
Patch20:        systemd-Define-__NR_kcmp-if-it-is-not-defined.patch
# Workaround for JB#36605. Should be removed after implementing UDEV events
# handling in initramfs.
Patch24:        systemd-udev-lvm-workaround.patch
Patch25:        systemd-225-add-pam-systemd-timeout-argument.patch
Patch28:        systemd-backport-when-deserializing-always-use-read_line.patch
Patch29:        systemd-backport-enforce-a-limit-on-status-texts-recvd-from-services.patch
Patch30:        systemd-backport-fix-deserialization-of-dev_t.patch
Patch31:        systemd-backport-rework-serialization-v3.patch
Patch32:        systemd-239-dhcp6-client-CVE-2018-15688-fix.patch
Patch35:        systemd-backport-journald-set-a-limit-on-the-number-of-fields-1k.patch
Patch36:        systemd-backport-fuzz-decrease-DATA_SIZE_MAX.patch
Patch37:        systemd-backport-journal-fix-syslog_parse_identifier.patch
Patch38:        systemd-backport-If-the-notification-message-length-is-0-ignore-the-m.patch
Patch39:        systemd-backport-pam-systemd-use-secure_getenv-rather-than-getenv.patch
# JB#49681 related patches
Patch41:        0001-aarch64-Force-udev-path.-Contributes-to-JB-49681.patch
Patch42:        0002-We-do-not-have-a-clean-environment-where-HAVE_SPIT_U.patch
# end
Patch43:        systemd-240-core-undo-the-dependency-inversion-between-unit.h-an.patch
Patch44:        systemd-239-core-don-t-include-libmount.h-in-a-header-file-8580.patch
Patch45:        systemd-pam_selinux-remove.patch
Patch46:        systemd-241-meson-rename-Ddebug-to-Ddebug-extra.patch
Patch47:        systemd-240-meson-unify-linux-stat.h-check-with-other-checks-and.patch
Patch48:        systemd-239-meson-avoid-warning-about-comparison-of-bool-and-str.patch
Patch49:        systemd-240-meson-drop-name-argument-in-cc.has_argument-8878.patch
Patch50:        systemd-240-meson-use-triple-quote-delimition-in-one-more-place.patch
Patch51:        systemd-241-coredump-only-install-coredump.conf-when-ENABLED_COR.patch
Patch52:        systemd-fix-fstab-generator.diff
Patch53:        systemd-240-core-dont-t-remount-sys-fs-cgroup-for-relabel-if-not.patch
Patch54:        systemd-239-core-do-not-free-heap-allocated-strings-8391.patch
Patch55:        systemd-disable-power-key-handling.diff
Patch56:        systemd-239-core-when-reloading-delay-any-actions-on-journal-and.patch
Patch57:        systemd-revert-PID-file-hardening-for-booster-silica-qt5.diff
Patch58:        systemd-240-core-remove-support-for-API-bus-started-outside-our-.patch
Patch59:        systemd-240-units-add-new-system-update-pre.target.patch
Patch60:        systemd-Fix-udev-firmware-events-dependencies.patch
Patch61:        systemd-245-polkit-async-CVE-2020-1712.diff
Patch62:        systemd-pam_limits-fix.patch
Patch63:        systemd-249-journald-Retry-if-posix_fallocate-returned-1-EINTR.patch
Patch64:        systemd-meson-do-not-fail-if-rsync-is-not-installed-with-mes.patch
# This patch serves two purposes: it adds needed "#include <sys/sysmacros.h>"
# and initializes variables with automatic cleanup functions to silence
# compiler warnings.
Patch99:        systemd-238_fix_build_with_glibc228.patch

BuildRequires:  audit-libs-devel
BuildRequires:  cmake
BuildRequires:  fdupes
BuildRequires:  glib2-devel
BuildRequires:  gperf
BuildRequires:  intltool >= 0.40.0
BuildRequires:  kmod-devel >= 15
BuildRequires:  libacl-devel
BuildRequires:  libcap-devel
BuildRequires:  libgcrypt-devel
BuildRequires:  libmount-devel
BuildRequires:  libselinux-devel
BuildRequires:  libtool
BuildRequires:  libxslt
BuildRequires:  meson
BuildRequires:  pam-devel
BuildRequires:  pkgconfig(blkid) >= 2.20
BuildRequires:  pkgconfig(dbus-1) >= 1.3.2
BuildRequires:  pkgconfig(dbus-glib-1)
BuildRequires:  pkgconfig(libcryptsetup) >= 1.6.0
BuildRequires:  xz-devel
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Requires:       %{name}-libs = %{version}-%{release}
Requires:       dbus
Requires:       filesystem >= 3
Requires:       systemd-config
# fsck with -l option was introduced in 2.21.2 packaging
Requires:       util-linux >= 2.21.2
Requires:       which
# pidof command
Requires:       psmisc
# For vgchange tool and LVM udev rules. Workaround for JB#36605.
# Should be removed after implementing UDEV events handling in initramfs.
Requires:       lvm2

Provides:       udev = %{version}
Obsoletes:      udev < 184
Provides:       systemd-sysv = %{version}
Obsoletes:      systemd-sysv < %{version}

%description
systemd is a system and service manager for Linux, compatible with
SysV and LSB init scripts. systemd provides aggressive parallelization
capabilities, uses socket and D-Bus activation for starting services,
offers on-demand starting of daemons, keeps track of processes using
Linux cgroups, supports snapshotting and restoring of the system
state, maintains mount and automount points and implements an
elaborate transactional dependency-based service control logic. It can
work as a drop-in replacement for sysvinit.

%package config-mer
Summary:    Default configuration for systemd
Requires:   %{name} = %{version}-%{release}
Provides:   systemd-config

%description config-mer
This package provides default configuration for systemd

%package analyze
Summary:    Analyze systemd startup timing
Requires:   %{name} = %{version}-%{release}
Provides:   %{name}-tools = %{version}
Obsoletes:  %{name}-tools <= 187

%description analyze
This package installs the systemd-analyze tool, which allows one to
inspect and graph service startup timing in table or graph format.

%package libs
Summary:        systemd libraries
License:        LGPLv2+ and MIT
Provides:       libudev = %{version}
Obsoletes:      libudev < %{version}
Obsoletes:      systemd <= 187
Conflicts:      systemd <= 187
Requires:       pam >= 1.3.1

%description libs
Libraries for systemd and udev, as well as the systemd PAM module.

%package devel
Summary:        Development headers for systemd
License:        LGPLv2+ and MIT
Requires:       %{name}-libs = %{version}-%{release}
# For macros.systemd
Requires:       %{name} = %{version}-%{release}
Provides:       libudev-devel = %{version}
Obsoletes:      libudev-devel < %{version}

%description devel
Development headers and auxiliary files for developing applications linking
to libudev or libsystemd.

%package doc
Summary:   System and session manager documentation
Requires:  %{name} = %{version}-%{release}
Obsoletes: %{name}-docs

%description doc
%{summary}.

%package tests
Summary:   Systemd tests
Requires:  %{name} = %{version}-%{release}
Requires:  blts-tools
Requires:  acl

%description tests
This package includes tests for systemd.

%prep
%autosetup -p1 -n %{name}-%{version}/systemd

%build
ntp_servers=({0..3}.sailfishos.pool.ntp.org)

CONFIGURE_OPTS=(
        -Drootprefix=/usr
        -Dacl=true
        -Dapparmor=false
        -Daudit=true
        -Dbacklight=false
        -Dblkid=true
        -Db_pie=true
        -Dbzip2=false
        -Dcoredump=false
        -Ddbus=true
        -Defi=false
        -Delfutils=false
        -Dfirstboot=false
        -Dgcrypt=true
        -Dglib=false
        -Dgnu-efi=false
        -Dgnutls=false
        -Dhibernate=false
        -Dimportd=false
        -Dinstall-tests=true
        -Dkmod=true
        -Dlibcryptsetup=true
        -Dlibcurl=false
        -Dlibidn=false
        -Dlibiptc=false
        -Dlocaled=false
        -Dlz4=false
        -Dmachined=false
        -Dman=false
        -Dmicrohttpd=false
        -Dmyhostname=false
        -Dnetworkd=false
        -Dntp-servers="${ntp_servers[*]}"
        -Dpam=true
        -Dqrencode=false
        -Dquotacheck=false
        -Dresolve=false
        -Drfkill=false
        -Dseccomp=false
        -Dselinux=true
        -Dsmack=false
        -Dsplit-usr=false
        -Dsystem-gid-max=999
        -Dsystem-uid-max=999
        -Dsysusers=false
        -Dsysvinit-path=
        -Dsysvrcnd-path=
        -Dtests=true
        -Dtimedated=false
        -Dtimesyncd=false
        -Dtpm=false
        -Dusers-gid=100
        -Dxkbcommon=false
        -Dxz=true
        -Dzlib=false
        -Dzshcompletiondir=no
)

%meson "${CONFIGURE_OPTS[@]}"
%meson_build

%install
%meson_install

# udev links
mkdir -p %{buildroot}%{_sbindir}
ln -sf ../..%{_bindir}/udevadm %{buildroot}%{_sbindir}/udevadm
# legacy link to keep things working while we move to bindir
mkdir -p %{buildroot}/bin
ln -sf ..%{_bindir}/udevadm %{buildroot}/bin/udevadm

# Compatiblity and documentation files
touch %{buildroot}%{_sysconfdir}/crypttab
chmod 600 %{buildroot}%{_sysconfdir}/crypttab

# Create SysV compatibility symlinks. systemctl/systemd are smart
# enough to detect in which way they are called.
mkdir -p %{buildroot}/sbin
ln -s ..%{pkgdir}/systemd %{buildroot}/sbin/init

# Make sure these directories are properly owned
mkdir -p %{buildroot}%{system_unit_dir}/basic.target.wants
mkdir -p %{buildroot}%{system_unit_dir}/default.target.wants
mkdir -p %{buildroot}%{system_unit_dir}/dbus.target.wants
mkdir -p %{buildroot}%{system_unit_dir}/getty.target.wants
mkdir -p %{buildroot}%{system_unit_dir}/syslog.target.wants
mkdir -p %{buildroot}%{system_unit_dir}/graphical.target.wants
mkdir -p %{buildroot}%{system_unit_dir}/network.target.wants
mkdir -p %{buildroot}%{_localstatedir}/run
mkdir -p %{buildroot}%{_localstatedir}/log
touch %{buildroot}%{_localstatedir}/run/utmp
touch %{buildroot}%{_localstatedir}/log/{w,b}tmp

# Make sure the user generators dir exists too
mkdir -p %{buildroot}%{pkgdir}/system-generators
mkdir -p %{buildroot}%{pkgdir}/user-generators

# Require network to be enabled with multi-user.target
mkdir -p %{buildroot}%{system_unit_dir}/multi-user.target.wants/
ln -s ../network.target %{buildroot}%{system_unit_dir}/multi-user.target.wants/network.target

# Install Fedora default preset policy
mkdir -p %{buildroot}%{pkgdir}/system-preset/
mkdir -p %{buildroot}%{pkgdir}/user-preset/

# Make sure the shutdown/sleep drop-in dirs exist
mkdir -p %{buildroot}%{pkgdir}/system-shutdown/
mkdir -p %{buildroot}%{pkgdir}/system-sleep/

# Make sure the NTP units dir exists
mkdir -p %{buildroot}%{pkgdir}/ntp-units.d/

# Make sure directories in /var exist
mkdir -p %{buildroot}%{_localstatedir}/lib/systemd/coredump
mkdir -p %{buildroot}%{_localstatedir}/lib/systemd/catalog
mkdir -p %{buildroot}%{_localstatedir}/log/journal
touch %{buildroot}%{_localstatedir}/lib/systemd/catalog/database
touch %{buildroot}%{_sysconfdir}/udev/hwdb.bin
touch %{buildroot}%{_localstatedir}/lib/systemd/random-seed

mkdir -p %{buildroot}%{_sysconfdir}/sysctl.d
mkdir -p %{buildroot}%{_sysconfdir}/modules-load.d
mkdir -p %{buildroot}%{_sysconfdir}/binfmt.d

mv %{buildroot}/%{_docdir}/systemd{,-%{version}}/

mkdir -p %{buildroot}/etc/systemd/system/basic.target.wants

# Add systemctl-user helper script
install -D -m 754 %{SOURCE3} %{buildroot}%{_bindir}/systemctl-user

%fdupes  %{buildroot}/%{_datadir}/man/

# Install tests.xml
install -d -m 755 %{buildroot}/opt/tests/systemd-tests
install -m 644 %{SOURCE2} %{buildroot}/opt/tests/systemd-tests

# systemd macros
# Old rpm versions assume macros in /etc/rpm/
# New ones support /usr/lib/rpm/macros.d/
# Systemd naturually uses later one
# But we support both by adding link
mkdir -p %{buildroot}%{_sysconfdir}/rpm
ln -s %{_libdir}/rpm/macros.d/macros.systemd %{buildroot}%{_sysconfdir}/rpm/macros.systemd

# Remove unneeded files
rm %{buildroot}%{_sysconfdir}/X11/xinit/xinitrc.d/50-systemd-user.sh

%find_lang %{name}

%check
#% meson_test

%pre
getent group cdrom >/dev/null 2>&1 || groupadd -r -g 11 cdrom >/dev/null 2>&1 || :
getent group utmp >/dev/null 2>&1 || groupadd -r -g 22 utmp >/dev/null 2>&1 || :
getent group tape >/dev/null 2>&1 || groupadd -r -g 33 tape >/dev/null 2>&1 || :
getent group dialout >/dev/null 2>&1 || groupadd -r -g 18 dialout >/dev/null 2>&1 || :
getent group input >/dev/null 2>&1 || groupadd -r input >/dev/null 2>&1 || :
getent group kvm &>/dev/null || groupadd -r -g 36 kvm &>/dev/null || :
getent group render &>/dev/null || groupadd -r render &>/dev/null || :
getent group systemd-journal >/dev/null 2>&1 || groupadd -r -g 190 systemd-journal 2>&1 || :

#getent group systemd-coredump &>/dev/null || groupadd -r systemd-coredump 2>&1 || :
#getent passwd systemd-coredump &>/dev/null || useradd -r -l -g systemd-coredump -d / -s /sbin/nologin -c "systemd Core Dumper" systemd-coredump &>/dev/null || :

getent group systemd-network >/dev/null 2>&1 || groupadd -r systemd-network 2>&1 || :
getent passwd systemd-network >/dev/null 2>&1 || useradd -r -l -g systemd-network -d / -s /sbin/nologin -c "systemd Network Management" systemd-network >/dev/null 2>&1 || :

#getent group systemd-resolve >/dev/null 2>&1 || groupadd -r systemd-resolve 2>&1 || :
#getent passwd systemd-resolve >/dev/null 2>&1 || useradd -r -l -g systemd-resolve -d / -s /sbin/nologin -c "systemd Resolver" systemd-resolve >/dev/null 2>&1 || :

systemctl stop systemd-udevd-control.socket systemd-udevd-kernel.socket systemd-udevd.service >/dev/null 2>&1 || :

%post
touch /etc/machine-id || :
%{pkgdir}/systemd-random-seed save >/dev/null 2>&1 || :
systemctl daemon-reexec >/dev/null 2>&1 || :
systemctl start systemd-udevd.service >/dev/null 2>&1 || :
udevadm hwdb --update >/dev/null 2>&1 || :
journalctl --update-catalog >/dev/null 2>&1 || :
systemd-tmpfiles --create >/dev/null 2>&1 || :

# Make sure new journal files will be owned by the "systemd-journal" group
chgrp systemd-journal /run/log/journal/ /run/log/journal/`cat /etc/machine-id 2> /dev/null` /var/log/journal/ /var/log/journal/`cat /etc/machine-id 2> /dev/null` >/dev/null 2>&1 || :
chmod g+s /run/log/journal/ /run/log/journal/`cat /etc/machine-id 2> /dev/null` /var/log/journal/ /var/log/journal/`cat /etc/machine-id 2> /dev/null` >/dev/null 2>&1 || :

# Apply ACL to the journal directory
setfacl -Rnm g:wheel:rx,d:g:wheel:rx,g:adm:rx,d:g:adm:rx /var/log/journal/ >/dev/null 2>&1 || :

# remove obsolete systemd-readahead file
rm -f /.readahead > /dev/null 2>&1 || :

%posttrans
# Make sure all symlinks in /etc/systemd/system point to the new units in
# /usr/lib/systemd/system and not in /lib/systemd/system
# This will find all broken symlinks and disable and enable each service
# JB#51560
for a in `find /etc/systemd/system -type l ! -exec test -e {} \; -print`; do stat -t -c%N $a | sed "s/'//g" | awk -F "/" '{print $NF" "$NF}' | xargs printf "systemctl disable %s; systemctl enable %s;\n" | sh; done || :

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root,-)
%dir %{_sysconfdir}/systemd
%dir %{_sysconfdir}/systemd/system
%exclude %{_sysconfdir}/systemd/system/getty.target.wants/getty@tty1.service
%dir %{_sysconfdir}/systemd/user
%dir %{_sysconfdir}/tmpfiles.d
%dir %{_sysconfdir}/sysctl.d
%dir %{_sysconfdir}/modules-load.d
%dir %{_sysconfdir}/binfmt.d
%dir %{_sysconfdir}/udev
%dir %{_sysconfdir}/udev/rules.d
# Include everything inside /usr/lib/systemd
%{pkgdir}
%dir %{_prefix}/lib/tmpfiles.d
%dir %{_prefix}/lib/sysctl.d
%dir %{_prefix}/lib/modules-load.d
%dir %{_prefix}/lib/binfmt.d
%dir %{_localstatedir}/log/journal
%dir %{_localstatedir}/lib/systemd
%dir %{_localstatedir}/lib/systemd/catalog
%dir %{_localstatedir}/lib/systemd/coredump
%ghost %{_localstatedir}/lib/systemd/random-seed
%ghost %{_localstatedir}/lib/systemd/catalog/database
%ghost %{_localstatedir}/log/btmp
%ghost %{_localstatedir}/log/wtmp
%ghost %{_localstatedir}/run/utmp
%dir %{_datadir}/dbus-1/system.d
%{_datadir}/dbus-1/system.d/org.freedesktop.systemd1.conf
%{_datadir}/dbus-1/system.d/org.freedesktop.hostname1.conf
%{_datadir}/dbus-1/system.d/org.freedesktop.login1.conf
%{_sysconfdir}/pam.d/systemd-user
%ghost %{_sysconfdir}/udev/hwdb.bin
%{_rpmconfigdir}/macros.d/macros.systemd
%dir %{_sysconfdir}/xdg/systemd
%{_sysconfdir}/rpm/macros.systemd
%{_bindir}/systemctl
%{_bindir}/systemd-notify
%{_bindir}/systemd-escape
%{_bindir}/systemd-ask-password
%{_bindir}/systemd-tty-ask-password-agent
%{_bindir}/systemd-machine-id-setup
%{_bindir}/loginctl
%{_bindir}/journalctl
%{_sysconfdir}/xdg/systemd/user
%ghost %{_sysconfdir}/crypttab
%{_sysconfdir}/systemd/system/*
%{_prefix}/lib/sysctl.d/50-default.conf
/lib/udev
%{_bindir}/systemctl-user
%{_bindir}/busctl
%{_bindir}/systemd-tmpfiles
%{_bindir}/kernel-install
%{_bindir}/systemd-nspawn
%{_bindir}/systemd-stdio-bridge
%{_bindir}/systemd-cat
%{_bindir}/systemd-cgls
%{_bindir}/systemd-cgtop
%{_bindir}/systemd-delta
%{_bindir}/systemd-mount
%{_bindir}/systemd-umount
%{_bindir}/systemd-socket-activate
%{_bindir}/systemd-run
%{_bindir}/systemd-detect-virt
%{_bindir}/systemd-inhibit
%{_bindir}/systemd-path
%{_bindir}/systemd-hwdb
%{_bindir}/hostnamectl
%{_prefix}/lib/tmpfiles.d/systemd.conf
%{_prefix}/lib/tmpfiles.d/systemd-nologin.conf
%{_prefix}/lib/tmpfiles.d/x11.conf
%{_prefix}/lib/tmpfiles.d/tmp.conf
%{_prefix}/lib/tmpfiles.d/var.conf
%{_prefix}/lib/tmpfiles.d/etc.conf
%{_prefix}/lib/tmpfiles.d/home.conf
%{_prefix}/lib/tmpfiles.d/systemd-nspawn.conf
%{_prefix}/lib/tmpfiles.d/journal-nocow.conf
%{_bindir}/udevadm
# legacy symlink
/bin/udevadm
%dir %{_prefix}/lib/kernel
%dir %{_prefix}/lib/kernel/install.d
%{_prefix}/lib/kernel/install.d/50-depmod.install
%{_prefix}/lib/kernel/install.d/90-loaderentry.install
/sbin/init
%{_sbindir}/init
%{_sbindir}/reboot
%{_sbindir}/halt
%{_sbindir}/poweroff
%{_sbindir}/shutdown
%{_sbindir}/telinit
%{_sbindir}/runlevel
%{_sbindir}/udevadm
%{_datadir}/factory
%{_datadir}/dbus-1/*/org.freedesktop.systemd1.service
%{_datadir}/dbus-1/system-services/org.freedesktop.hostname1.service
%{_datadir}/dbus-1/system-services/org.freedesktop.login1.service
%{_datadir}/polkit-1/actions/org.freedesktop.systemd1.policy
%{_datadir}/polkit-1/actions/org.freedesktop.hostname1.policy
%{_datadir}/polkit-1/actions/org.freedesktop.login1.policy
%{_datadir}/bash-completion/completions/*
# These 2 files should land in /usr/lib without depending on 32/64 bits.
%{_prefix}/lib/environment.d/99-environment.conf
%{_prefix}/lib/modprobe.d/systemd.conf
%license LICENSE.GPL2
%license LICENSE.LGPL2.1

# Just make sure we don't package these by default
%exclude %{_prefix}/lib/systemd/system/default.target
%exclude %{user_unit_dir}/default.target
%exclude %{_sysconfdir}/systemd/system/multi-user.target.wants/remote-fs.target
%exclude %{system_unit_dir}/user@.service

# This directory belongs to the tests subpackage
%exclude %{pkgdir}/tests

%files config-mer
%defattr(-,root,root,-)
%{_sysconfdir}/systemd/journald.conf
%{_sysconfdir}/systemd/logind.conf
%{_sysconfdir}/systemd/system.conf
%{_sysconfdir}/systemd/user.conf
%{_sysconfdir}/udev/udev.conf
%{system_unit_dir}/default.target
%{system_unit_dir}/user@.service

%files doc
%defattr(-,root,root,-)
%{_docdir}/%{name}-%{version}

%files tests
%defattr(-,root,root,-)
%dir /opt/tests/systemd-tests
/opt/tests/systemd-tests/tests.xml
%{pkgdir}/tests

%files analyze
%defattr(-,root,root,-)
%{_bindir}/systemd-analyze

%files libs
%{_libdir}/security/pam_systemd.so
%{_libdir}/libudev.so.*
%{_libdir}/libsystemd.so.*
%{_libdir}/libnss_systemd.so.*

%files devel
%dir %{_includedir}/systemd
%{_libdir}/libudev.so
%{_libdir}/libsystemd.so
%{_includedir}/systemd/sd-daemon.h
%{_includedir}/systemd/sd-login.h
%{_includedir}/systemd/sd-journal.h
%{_includedir}/systemd/sd-id128.h
%{_includedir}/systemd/sd-messages.h
%{_includedir}/systemd/sd-bus-protocol.h
%{_includedir}/systemd/sd-bus-vtable.h
%{_includedir}/systemd/sd-bus.h
%{_includedir}/systemd/sd-event.h
%{_includedir}/systemd/_sd-common.h
%{_includedir}/libudev.h
%{_libdir}/pkgconfig/libudev.pc
%{_libdir}/pkgconfig/libsystemd.pc
%{_datadir}/pkgconfig/systemd.pc
%{_datadir}/pkgconfig/udev.pc
