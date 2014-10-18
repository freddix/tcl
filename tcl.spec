# based on PLD Linux spec git://git.pld-linux.org/packages/tcl.git
%define		major	8.6
%define		minor	2
#
Summary:	Tool Command Language embeddable scripting language, with shared libraries
Name:		tcl
Version:	%{major}.%{minor}
Release:	1
License:	BSD
Group:		Development/Languages/Tcl
Source0:	http://downloads.sourceforge.net/tcl/%{name}%{version}-src.tar.gz
# Source0-md5:	8103eaf6d71acb716a64224492f09d5f
Patch0:		%{name}-autopath.patch
Patch1:		%{name}-conf.patch
Patch2:		%{name}-hidden.patch
URL:		http://www.tcl.tk/
BuildRequires:	autoconf
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Tcl is a simple scripting language that is designed to be embedded in
other applications. This package includes tclsh, a simple example of a
tcl application. Tcl is very popular for writing small graphical
applications because of the Tk widget set which is closely tied to it.

%package devel
Summary:	Tool Command Language header files and development documentation
Group:		Development/Languages/Tcl
Requires:	%{name} = %{version}-%{release}

%description devel
Tool Command Language embeddable scripting language header files and
develpment documentation.

%prep
%setup -qn %{name}%{version}
# Fedora patches from http://pkgs.fedoraproject.org/cgit/tcl.git
%patch0 -p1
%patch1 -p1
%patch2 -p1

%{__rm} -r pkgs/sqlite3* compat/zlib

%build
cd unix
%{__autoconf}
%configure \
%ifarch %{x8664}
	--enable-64bit		\
%endif
	--enable-langinfo	\
	--enable-shared		\
	--enable-threads	\
	--without-tzdata
%{__make} \
        TCL_LIBRARY=%{_datadir}/tcl%{major}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -j1 -C unix install \
	INSTALL_ROOT=$RPM_BUILD_ROOT	\
        TCL_LIBRARY=%{_datadir}/tcl%{major}

ln -sf libtcl%{major}.so $RPM_BUILD_ROOT%{_libdir}/libtcl.so
mv -f $RPM_BUILD_ROOT%{_bindir}/{tclsh%{major},tclsh}

install -d $RPM_BUILD_ROOT%{_includedir}/%{name}-private/{generic,unix}
find generic unix -name '*.h' -exec cp -p '{}' $RPM_BUILD_ROOT%{_includedir}/%{name}-private/'{}' ';'
for h in $RPM_BUILD_ROOT%{_includedir}/*.h; do
        rh=$(basename "$h")
        if [ -f "$RPM_BUILD_ROOT%{_includedir}/%{name}-private/generic/$rh" ]; then
                ln -sf "../../$rh" $RPM_BUILD_ROOT%{_includedir}/%{name}-private/generic
        fi
done

%{__sed} -i -e "s|%{_builddir}/%{name}%{version}/unix|%{_libdir}|; \
        s|%{_builddir}/%{name}%{version}|%{_includedir}/tcl-private|;
	s|%{rpmcflags}||" $RPM_BUILD_ROOT%{_libdir}/tclConfig.sh

%if 0
%check
cd unix
%{__make} test
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /usr/sbin/ldconfig
%postun -p /usr/sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/tclsh
%attr(755,root,root) %{_libdir}/libtcl%{major}.so

%dir %{_datadir}/tcl%{major}
%dir %{_datadir}/tcl%{major}/msgs

%{_datadir}/tcl%{major}/*.tcl
%{_datadir}/tcl%{major}/encoding
%{_datadir}/tcl%{major}/http1.0
%{_datadir}/tcl%{major}/opt0.4
%{_datadir}/tcl%{major}/tclIndex
%{_datadir}/tcl[0-9]

%lang(af) %{_datadir}/tcl%{major}/msgs/af.msg
%lang(af_ZA) %{_datadir}/tcl%{major}/msgs/af_za.msg
%lang(ar) %{_datadir}/tcl%{major}/msgs/ar.msg
%lang(ar_IN) %{_datadir}/tcl%{major}/msgs/ar_in.msg
%lang(ar_JO) %{_datadir}/tcl%{major}/msgs/ar_jo.msg
%lang(ar_LB) %{_datadir}/tcl%{major}/msgs/ar_lb.msg
%lang(ar_SY) %{_datadir}/tcl%{major}/msgs/ar_sy.msg
%lang(be) %{_datadir}/tcl%{major}/msgs/be.msg
%lang(bg) %{_datadir}/tcl%{major}/msgs/bg.msg
%lang(bn) %{_datadir}/tcl%{major}/msgs/bn.msg
%lang(bn_IN) %{_datadir}/tcl%{major}/msgs/bn_in.msg
%lang(ca) %{_datadir}/tcl%{major}/msgs/ca.msg
%lang(cs) %{_datadir}/tcl%{major}/msgs/cs.msg
%lang(da) %{_datadir}/tcl%{major}/msgs/da.msg
%lang(de) %{_datadir}/tcl%{major}/msgs/de.msg
%lang(de_AT) %{_datadir}/tcl%{major}/msgs/de_at.msg
%lang(de_BE) %{_datadir}/tcl%{major}/msgs/de_be.msg
%lang(el) %{_datadir}/tcl%{major}/msgs/el.msg
%lang(en_AU) %{_datadir}/tcl%{major}/msgs/en_au.msg
%lang(en_BE) %{_datadir}/tcl%{major}/msgs/en_be.msg
%lang(en_BW) %{_datadir}/tcl%{major}/msgs/en_bw.msg
%lang(en_CA) %{_datadir}/tcl%{major}/msgs/en_ca.msg
%lang(en_GB) %{_datadir}/tcl%{major}/msgs/en_gb.msg
%lang(en_HK) %{_datadir}/tcl%{major}/msgs/en_hk.msg
%lang(en_IE) %{_datadir}/tcl%{major}/msgs/en_ie.msg
%lang(en_IN) %{_datadir}/tcl%{major}/msgs/en_in.msg
%lang(en_NZ) %{_datadir}/tcl%{major}/msgs/en_nz.msg
%lang(en_PH) %{_datadir}/tcl%{major}/msgs/en_ph.msg
%lang(en_SG) %{_datadir}/tcl%{major}/msgs/en_sg.msg
%lang(en_ZA) %{_datadir}/tcl%{major}/msgs/en_za.msg
%lang(en_ZW) %{_datadir}/tcl%{major}/msgs/en_zw.msg
%lang(eo) %{_datadir}/tcl%{major}/msgs/eo.msg
%lang(es) %{_datadir}/tcl%{major}/msgs/es.msg
%lang(es_AR) %{_datadir}/tcl%{major}/msgs/es_ar.msg
%lang(es_BO) %{_datadir}/tcl%{major}/msgs/es_bo.msg
%lang(es_CL) %{_datadir}/tcl%{major}/msgs/es_cl.msg
%lang(es_CO) %{_datadir}/tcl%{major}/msgs/es_co.msg
%lang(es_CR) %{_datadir}/tcl%{major}/msgs/es_cr.msg
%lang(es_DO) %{_datadir}/tcl%{major}/msgs/es_do.msg
%lang(es_EC) %{_datadir}/tcl%{major}/msgs/es_ec.msg
%lang(es_GT) %{_datadir}/tcl%{major}/msgs/es_gt.msg
%lang(es_HN) %{_datadir}/tcl%{major}/msgs/es_hn.msg
%lang(es_MX) %{_datadir}/tcl%{major}/msgs/es_mx.msg
%lang(es_NI) %{_datadir}/tcl%{major}/msgs/es_ni.msg
%lang(es_PA) %{_datadir}/tcl%{major}/msgs/es_pa.msg
%lang(es_PE) %{_datadir}/tcl%{major}/msgs/es_pe.msg
%lang(es_PR) %{_datadir}/tcl%{major}/msgs/es_pr.msg
%lang(es_PY) %{_datadir}/tcl%{major}/msgs/es_py.msg
%lang(es_SV) %{_datadir}/tcl%{major}/msgs/es_sv.msg
%lang(es_UY) %{_datadir}/tcl%{major}/msgs/es_uy.msg
%lang(es_VE) %{_datadir}/tcl%{major}/msgs/es_ve.msg
%lang(et) %{_datadir}/tcl%{major}/msgs/et.msg
%lang(eu) %{_datadir}/tcl%{major}/msgs/eu.msg
%lang(eu_ES) %{_datadir}/tcl%{major}/msgs/eu_es.msg
%lang(fa) %{_datadir}/tcl%{major}/msgs/fa.msg
%lang(fa_IN) %{_datadir}/tcl%{major}/msgs/fa_in.msg
%lang(fa_IR) %{_datadir}/tcl%{major}/msgs/fa_ir.msg
%lang(fi) %{_datadir}/tcl%{major}/msgs/fi.msg
%lang(fo) %{_datadir}/tcl%{major}/msgs/fo.msg
%lang(fo_FO) %{_datadir}/tcl%{major}/msgs/fo_fo.msg
%lang(fr) %{_datadir}/tcl%{major}/msgs/fr.msg
%lang(fr_BE) %{_datadir}/tcl%{major}/msgs/fr_be.msg
%lang(fr_CA) %{_datadir}/tcl%{major}/msgs/fr_ca.msg
%lang(fr_CH) %{_datadir}/tcl%{major}/msgs/fr_ch.msg
%lang(ga) %{_datadir}/tcl%{major}/msgs/ga.msg
%lang(ga_IE) %{_datadir}/tcl%{major}/msgs/ga_ie.msg
%lang(gl) %{_datadir}/tcl%{major}/msgs/gl.msg
%lang(gl_ES) %{_datadir}/tcl%{major}/msgs/gl_es.msg
%lang(gv) %{_datadir}/tcl%{major}/msgs/gv.msg
%lang(gv_GB) %{_datadir}/tcl%{major}/msgs/gv_gb.msg
%lang(he) %{_datadir}/tcl%{major}/msgs/he.msg
%lang(hi) %{_datadir}/tcl%{major}/msgs/hi.msg
%lang(hi_IN) %{_datadir}/tcl%{major}/msgs/hi_in.msg
%lang(hr) %{_datadir}/tcl%{major}/msgs/hr.msg
%lang(hu) %{_datadir}/tcl%{major}/msgs/hu.msg
%lang(id) %{_datadir}/tcl%{major}/msgs/id.msg
%lang(id_ID) %{_datadir}/tcl%{major}/msgs/id_id.msg
%lang(is) %{_datadir}/tcl%{major}/msgs/is.msg
%lang(it) %{_datadir}/tcl%{major}/msgs/it.msg
%lang(it_CH) %{_datadir}/tcl%{major}/msgs/it_ch.msg
%lang(ja) %{_datadir}/tcl%{major}/msgs/ja.msg
%lang(kl) %{_datadir}/tcl%{major}/msgs/kl.msg
%lang(kl_GL) %{_datadir}/tcl%{major}/msgs/kl_gl.msg
%lang(ko) %{_datadir}/tcl%{major}/msgs/ko.msg
%lang(ko) %{_datadir}/tcl%{major}/msgs/ko_kr.msg
%lang(kok) %{_datadir}/tcl%{major}/msgs/kok.msg
%lang(kok_IN) %{_datadir}/tcl%{major}/msgs/kok_in.msg
%lang(kw) %{_datadir}/tcl%{major}/msgs/kw.msg
%lang(kw_GB) %{_datadir}/tcl%{major}/msgs/kw_gb.msg
%lang(lt) %{_datadir}/tcl%{major}/msgs/lt.msg
%lang(lv) %{_datadir}/tcl%{major}/msgs/lv.msg
%lang(mk) %{_datadir}/tcl%{major}/msgs/mk.msg
%lang(mr) %{_datadir}/tcl%{major}/msgs/mr.msg
%lang(mr_IN) %{_datadir}/tcl%{major}/msgs/mr_in.msg
%lang(ms) %{_datadir}/tcl%{major}/msgs/ms.msg
%lang(ms_MY) %{_datadir}/tcl%{major}/msgs/ms_my.msg
%lang(mt) %{_datadir}/tcl%{major}/msgs/mt.msg
%lang(nb) %{_datadir}/tcl%{major}/msgs/nb.msg
%lang(nl) %{_datadir}/tcl%{major}/msgs/nl.msg
%lang(nl_BE) %{_datadir}/tcl%{major}/msgs/nl_be.msg
%lang(nn) %{_datadir}/tcl%{major}/msgs/nn.msg
%lang(pl) %{_datadir}/tcl%{major}/msgs/pl.msg
%lang(pt) %{_datadir}/tcl%{major}/msgs/pt.msg
%lang(pt_BR) %{_datadir}/tcl%{major}/msgs/pt_br.msg
%lang(ro) %{_datadir}/tcl%{major}/msgs/ro.msg
%lang(ru) %{_datadir}/tcl%{major}/msgs/ru.msg
%lang(ru_UA) %{_datadir}/tcl%{major}/msgs/ru_ua.msg
%lang(sh) %{_datadir}/tcl%{major}/msgs/sh.msg
%lang(sk) %{_datadir}/tcl%{major}/msgs/sk.msg
%lang(sl) %{_datadir}/tcl%{major}/msgs/sl.msg
%lang(sq) %{_datadir}/tcl%{major}/msgs/sq.msg
%lang(sr) %{_datadir}/tcl%{major}/msgs/sr.msg
%lang(sv) %{_datadir}/tcl%{major}/msgs/sv.msg
%lang(sw) %{_datadir}/tcl%{major}/msgs/sw.msg
%lang(ta) %{_datadir}/tcl%{major}/msgs/ta.msg
%lang(ta_IN) %{_datadir}/tcl%{major}/msgs/ta_in.msg
%lang(te) %{_datadir}/tcl%{major}/msgs/te.msg
%lang(te_IN) %{_datadir}/tcl%{major}/msgs/te_in.msg
%lang(th) %{_datadir}/tcl%{major}/msgs/th.msg
%lang(tr) %{_datadir}/tcl%{major}/msgs/tr.msg
%lang(uk) %{_datadir}/tcl%{major}/msgs/uk.msg
%lang(vi) %{_datadir}/tcl%{major}/msgs/vi.msg
%lang(zh) %{_datadir}/tcl%{major}/msgs/zh.msg
%lang(zh_CN) %{_datadir}/tcl%{major}/msgs/zh_cn.msg
%lang(zh_HK) %{_datadir}/tcl%{major}/msgs/zh_hk.msg
%lang(zh_SG) %{_datadir}/tcl%{major}/msgs/zh_sg.msg
%lang(zh_TW) %{_datadir}/tcl%{major}/msgs/zh_tw.msg
%{_mandir}/man1/tclsh.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/tclConfig.sh
%attr(755,root,root) %{_libdir}/tclooConfig.sh
%attr(755,root,root) %{_libdir}/libtcl%{major}.so
%attr(755,root,root) %{_libdir}/libtcl.so
%{_libdir}/libtclstub%{major}.a
%{_includedir}/tcl*.h
%{_includedir}/tcl-private
%{_datadir}/tcl%{major}/tclAppInit.c
%{_pkgconfigdir}/tcl.pc

%{_mandir}/man3/TCL_*.3*
%{_mandir}/man3/Tcl_*.3*
%{_mandir}/man3/attemptck*alloc.3*
%{_mandir}/man3/ck*.3*
%{_mandir}/mann/*.n*

