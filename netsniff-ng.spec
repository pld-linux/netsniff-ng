Summary:	A Swiss army knife for network plumbing
Summary(pl.UTF-8):	"Szwajcarski scyzoryk" do napraw sieci
Name:		netsniff-ng
Version:	0.6.7
Release:	3
License:	GPL v2
Group:		Networking/Utilities
Source0:	http://pub.netsniff-ng.org/netsniff-ng/%{name}-%{version}.tar.xz
# Source0-md5:	2aba9835923c30721fa891a9dc59507c
Patch0:		%{name}-opt.patch
URL:		http://netsniff-ng.org/
BuildRequires:	GeoIP-devel >= 1.4.8
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	libcli-devel
BuildRequires:	libnet-devel
BuildRequires:	libnetfilter_conntrack-devel
BuildRequires:	libnl-devel >= 3.2
BuildRequires:	libpcap-devel
BuildRequires:	libsodium-devel
BuildRequires:	ncurses-devel
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.719
BuildRequires:	sed >= 4.0
BuildRequires:	userspace-rcu-devel
BuildRequires:	zlib-devel
Requires:	GeoIP-libs >= 1.4.8
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
* netsniff-ng, a fast zero-copy analyzer, pcap capturing and replaying
  tool
* trafgen, a multithreaded low-level zero-copy network packet
  generator
* mausezahn, high-level packet generator for HW/SW appliances with
  Cisco-CLI
* bpfc, a Berkeley Packet Filter compiler, Linux BPF JIT disassembler
* ifpps, a top-like kernel networking statistics tool
* flowtop, a top-like netfilter connection tracking tool
* curvetun, a lightweight curve25519-based IP tunnel
* astraceroute, an autonomous system (AS) trace route utility

%description -l pl.UTF-8
* netsniff-ng - szybkie, niekopiujące narzędzie do analizy,
  przechwytywania pakietów przez pcap i odtwarzania
* trafgen - wielowątkowy, niskopoziomowy, niekopiujący generator
  pakietów sieciowych
* mausezahn - wysokopoziomowy generator pakietów do zastosowań HW/SW z
  interfejsem linii poleceń w stylu Cisco
* bpfc - kompilator filtrów BPF (Berkeley Packet Filter), disasembler
  JIT linuksowego BPF
* ifpps - narzędzie do statystyk sieciowych jądra w stylu programu top
* flowtop - narzędzie do śledzenia połączeń netfiltra w stylu topa
* curvetun - lekki tunel IP oparty na curve25519
* astraceroute - narzędzie autonomicznego systemu (AS) do śledzenia
  tras

%prep
%setup -q
%patch -P0 -p1

%build
# not autoconf configure
./configure \
	--sysconfdir="%{_sysconfdir}" \
	--prefix="%{_prefix}"

# as of 0.6.7 code relies on -fcommon behaviour, force it for gcc 10+
%{__make} \
	CC="%{__cc}" \
	CPPFLAGS="%{rpmcflags} %{rpmcppflags} -fcommon" \
	%{?debug:DEBUG=1} \
	Q=

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{zsh_compdir}}

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

for i in *.zsh; do
	cp -p "$i" $RPM_BUILD_ROOT%{zsh_compdir}/_"${i%.zsh}"
done

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS README REPORTING-BUGS bpf_jit_disasm.c bpf.vim
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/*.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/stddef.h
%attr(755,root,root) %{_sbindir}/astraceroute
%attr(755,root,root) %{_sbindir}/bpfc
%attr(755,root,root) %{_sbindir}/curvetun
%attr(755,root,root) %{_sbindir}/flowtop
%attr(755,root,root) %{_sbindir}/ifpps
%attr(755,root,root) %{_sbindir}/mausezahn
%attr(755,root,root) %{_sbindir}/netsniff-ng
%attr(755,root,root) %{_sbindir}/trafgen
%{zsh_compdir}/_astraceroute
%{zsh_compdir}/_bpfc
%{zsh_compdir}/_curvetun
%{zsh_compdir}/_flowtop
%{zsh_compdir}/_ifpps
%{zsh_compdir}/_mausezahn
%{zsh_compdir}/_netsniff-ng
%{zsh_compdir}/_trafgen
%{_mandir}/man8/astraceroute.8*
%{_mandir}/man8/bpfc.8*
%{_mandir}/man8/curvetun.8*
%{_mandir}/man8/flowtop.8*
%{_mandir}/man8/ifpps.8*
%{_mandir}/man8/mausezahn.8*
%{_mandir}/man8/netsniff-ng.8*
%{_mandir}/man8/trafgen.8*
