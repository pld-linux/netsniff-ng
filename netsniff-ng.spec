Summary:	A Swiss army knife for network plumbing
Name:		netsniff-ng
Version:	0.6.3
Release:	1
License:	GPL v2
Group:		Networking/Utilities
Source0:	http://pub.netsniff-ng.org/netsniff-ng/%{name}-%{version}.tar.xz
# Source0-md5:	e892a7f2e025fba07d0f0a330e9917df
URL:		http://netsniff-ng.org/
BuildRequires:	GeoIP-devel
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	libcli-devel
BuildRequires:	libnet-devel
BuildRequires:	libnetfilter_conntrack-devel
BuildRequires:	libnl-devel
BuildRequires:	libpcap-devel
BuildRequires:	libsodium-devel
BuildRequires:	ncurses-devel
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.719
BuildRequires:	userspace-rcu-devel
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
* netsniff-ng, a fast zero-copy analyzer, pcap capturing and replaying tool
* trafgen, a multithreaded low-level zero-copy network packet generator
* mausezahn, high-level packet generator for HW/SW appliances with Cisco-CLI
* bpfc, a Berkeley Packet Filter compiler, Linux BPF JIT disassembler
* ifpps, a top-like kernel networking statistics tool
* flowtop, a top-like netfilter connection tracking tool
* curvetun, a lightweight curve25519-based IP tunnel
* astraceroute, an autonomous system (AS) trace route utility

%prep
%setup -q

%build
NACL_INC_DIR=$(pkg-config --variable=includedir libsodium )/sodium \
NACL_LIB=sodium \
%configure \
	--sysconfdir="%{_sysconfdir}" \
	--prefix="%{_prefix}"
%{__make} \
	%{?debug:DEBUG=1} \
	%{!?debug:HARDENING=1 CPPFLAGS="%{rpmcflags}"} \
	Q=

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{zsh_compdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

for i in *.zsh
	install -p "$i" "%{zsh_compdir}/_${i%.zsh}"
done

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS README REPORTING-BUGS bpf_jit_disasm bpf.vim
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/*
%attr(755,root,root) %{_sbindir}/*
%{zsh_compdir}/_*
%{_mandir}/man8/*.8*
