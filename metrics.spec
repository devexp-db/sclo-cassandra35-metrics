Name:          metrics
Version:       3.0.1
Release:       6%{?dist}
Summary:       Java library which gives you what your code does in production
License:       ASL 2.0
URL:           http://metrics.dropwizard.io
Source0:       https://github.com/dropwizard/metrics/archive/v%{version}.tar.gz

BuildRequires: maven-local
BuildRequires: mvn(ch.qos.logback:logback-classic)
BuildRequires: mvn(com.fasterxml.jackson.core:jackson-databind)
BuildRequires: mvn(com.sun.jersey:jersey-server:1.19)
BuildRequires: mvn(info.ganglia.gmetric4j:gmetric4j)
BuildRequires: mvn(javax.servlet:javax.servlet-api)
BuildRequires: mvn(log4j:log4j:1.2.17)
BuildRequires: mvn(net.sf.ehcache:ehcache-core)
BuildRequires: mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires: mvn(org.apache.httpcomponents:httpclient)
BuildRequires: mvn(org.jdbi:jdbi)
BuildRequires: mvn(org.slf4j:slf4j-api)

%if 0
# metrics-jetty9 deps
BuildRequires: mvn(org.eclipse.jetty:jetty-client)
BuildRequires: mvn(org.eclipse.jetty:jetty-server)

# metrics-benchmarks deps
BuildRequires: mvn(com.google.caliper:caliper:1.0-beta-1)
BuildRequires: mvn(com.google.guava:guava:14.0.1)

# Test deps
BuildRequires: mvn(com.sun.jersey.jersey-test-framework:jersey-test-framework-inmemory:1.19)
BuildRequires: mvn(junit:junit)
BuildRequires: mvn(org.easytesting:fest-assert-core:2.0M10)
BuildRequires: mvn(org.eclipse.jetty:jetty-servlet)
BuildRequires: mvn(org.mockito:mockito-all)
BuildRequires: mvn(org.slf4j:slf4j-simple)
%endif

# Docs deps
BuildRequires: python-sphinx
BuildRequires: /usr/bin/pdflatex

BuildArch:     noarch

%description
Metrics is a Java library which gives you unparalleled insight
into what your code does in production.

Developed by Yammer to instrument their JVM-based back-end services,
Metrics provides a powerful toolkit of ways to measure the behavior
of critical components in your production environment.

With modules for common libraries like Jetty, Logback, Log4j,
Apache HttpClient, Ehcache, JDBI, Jersey and reporting back-ends like
Ganglia and Graphite, Metrics provides you with full-stack visibility.

For more information, please see the documentation.

This package provides the Metrics Core Library.

%package annotation
Summary:       Annotations for Metrics

%description annotation
A dependency-less package of just the
annotations used by other Metrics modules.

%if 0
%package benchmarks
Summary:       Benchmarks for Metrics

%description benchmarks
A development module for performance benchmarks of
Metrics classes.
%endif

%package ehcache
Summary:       Metrics Integration for Ehcache

%description ehcache
An Ehcache wrapper providing Metrics instrumentation of caches.

%package ganglia
Summary:       Ganglia Integration for Metrics

%description ganglia
A reporter for Metrics which announces measurements
to a Ganglia cluster.

%package graphite
Summary:       Graphite Integration for Metrics

%description graphite
A reporter for Metrics which announces measurements
to a Graphite server.

%package healthchecks
Summary:       Metrics Health Checks

%description healthchecks
An addition to Metrics which provides the ability to
run application-specific health checks, allowing you
to check your application's heath in production.

%package httpclient
Summary:       Metrics Integration for Apache HttpClient

%description httpclient
An Apache HttpClient wrapper providing Metrics
instrumentation of connection pools, request
durations and rates, and other useful information.

%package jdbi
Summary:       Metrics Integration for JDBI

%description jdbi
A JDBI wrapper providing Metrics instrumentation of
query durations and rates.

%package jersey
Summary:       Metrics Integration for Jersey

%description jersey
A set of class providing Metrics integration for Jersey,
the reference JAX-RS implementation.

%if 0
%package jetty
Summary:       Metrics Integration for Jetty 9

%description jetty
A set of extensions for Jetty 9 which provide instrumentation of
thread pools, connector metrics, and application latency and
utilization.
%endif

%package json
Summary:       Jackson Integration for Metrics

%description json
A set of Jackson modules which provide serializers
for most Metrics classes.

%package jvm
Summary:       JVM Integration for Metrics

%description jvm
A set of classes which allow you to monitor
critical aspects of your Java Virtual Machine
using Metrics.

%package log4j
Summary:       Metrics Integration for Log4j
%if %{?fedora} > 20
Requires:      log4j12
%endif

%description log4j
An instrumented appender for Log4j.

%package logback
Summary:       Metrics Integration for Logback

%description logback
An instrumented appender for Logback.

%package servlet
Summary:       Metrics Integration for Servlets

%description servlet
An instrumented filter for servlet environments.

%package servlets
Summary:       Metrics Utility Servlets

%description servlets
A set of utility servlets for Metrics, allowing you
to expose valuable information about your production
environment.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%package doc
Summary:       Metrics's user manual

%description doc
This package contains %{name}'s user manual.

%prep
%setup -q -n %{name}-%{version}

find . -name "*.class" -delete
find . -name "*.jar" -type f -delete

# Unavailable build deps:
%pom_disable_module metrics-jetty8
%pom_disable_module metrics-benchmarks

# TODO see rhbz#861502#c3 rhbz#861502#c5 disable jetty9 sub-module (use jetty 9.0.4.v20130625) org.eclipse.jetty.server.HttpChannelState.isDispatched method was removed
%pom_disable_module metrics-jetty9

# org.easytesting:fest-assert-core:2.0M10 *
%pom_remove_dep org.easytesting:fest-assert-core

%pom_remove_plugin :findbugs-maven-plugin
%pom_remove_plugin :maven-enforcer-plugin

# Disable javadoc jar
%pom_xpath_remove "pom:plugins/pom:plugin[pom:artifactId='maven-javadoc-plugin']/pom:executions"
# Disable source jar
%pom_remove_plugin :maven-source-plugin

%pom_xpath_set "pom:properties/pom:jersey.version" 1.19 %{name}-jersey

%mvn_package ":%{name}-core" %{name}
%mvn_package ":%{name}-parent" %{name}
%if 0
%mvn_package ":%{name}-jetty9" %{name}-jetty
%endif

%build

# Unavailable test dep *
%mvn_build -s -f

(
  cd docs
%if 0
  make %{?_smp_mflags} latexpdf
%endif
  make %{?_smp_mflags} singlehtml
  make %{?_smp_mflags} man
)

%install
%mvn_install

mkdir -p %{buildroot}%{_mandir}/man1
install -pm 644 docs/target/man/%{name}.1 %{buildroot}%{_mandir}/man1/

rm -rf docs/target/singlehtml/.buildinfo

%files  -f .mfiles-%{name}
%dir %{_javadir}/%{name}
%doc README.md
%license LICENSE NOTICE

%files annotation -f .mfiles-%{name}-annotation
%license LICENSE NOTICE

%if 0
%files benchmarks -f .mfiles-%{name}-benchmarks
%license LICENSE NOTICE
%endif

%files ehcache -f .mfiles-%{name}-ehcache
%license LICENSE NOTICE

%files ganglia -f .mfiles-%{name}-ganglia
%license LICENSE NOTICE

%files graphite -f .mfiles-%{name}-graphite
%license LICENSE NOTICE

%files healthchecks -f .mfiles-%{name}-healthchecks
%license LICENSE NOTICE

%files httpclient -f .mfiles-%{name}-httpclient
%license LICENSE NOTICE

%files jdbi -f .mfiles-%{name}-jdbi
%license LICENSE NOTICE

%files jersey -f .mfiles-%{name}-jersey
%license LICENSE NOTICE

%if 0
%files jetty -f .mfiles-%{name}-jetty
%license LICENSE NOTICE
%endif

%files json -f .mfiles-%{name}-json
%license LICENSE NOTICE

%files jvm -f .mfiles-%{name}-jvm
%license LICENSE NOTICE

%files log4j -f .mfiles-%{name}-log4j
%license LICENSE NOTICE

%files logback -f .mfiles-%{name}-logback
%license LICENSE NOTICE

%files servlet -f .mfiles-%{name}-servlet
%license LICENSE NOTICE

%files servlets -f .mfiles-%{name}-servlets
%license LICENSE NOTICE

%files javadoc -f .mfiles-javadoc
%license LICENSE NOTICE

%files doc
%{_mandir}/man1/%{name}.*
%license LICENSE NOTICE
%doc docs/target/singlehtml
%if 0
%doc docs/target/latex/*.pdf
%endif

%changelog
* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri May 29 2015 gil cattaneo <puntogil@libero.it> 3.0.1-5
- rebuilt with jersey 1.19

* Tue Feb 10 2015 gil cattaneo <puntogil@libero.it> 3.0.1-4
- introduce license macro

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 3.0.1-2
- Use Requires: java-headless rebuild (#1067528)

* Sat Aug 03 2013 gil cattaneo <puntogil@libero.it> 3.0.1-1
- update to 3.0.1

* Fri Sep 28 2012 gil cattaneo <puntogil@libero.it> 2.1.3-1
- initial rpm
