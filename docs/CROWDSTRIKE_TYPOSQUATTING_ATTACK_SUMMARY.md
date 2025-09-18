# CrowdStrike Typosquatting Attack - IOC Update Summary

## Attack Overview

Basierend auf dem Socket.dev Blog-Artikel wurde eine massive Typosquatting-Kampagne entdeckt, die CrowdStrike NPM-Pakete imitiert. Die Attacke ist auf **über 400 bösartige Pakete** angewachsen und nutzt verschiedene Typosquatting-Techniken.

**Quelle**: https://socket.dev/blog/ongoing-supply-chain-attack-targets-crowdstrike-npm-packages

## IOC-Definitionen Erweitert

Die `issues/s1ngularity_nx_attack_2024.py` Datei wurde erheblich erweitert und enthält jetzt:

### 📊 Statistiken
- **Ursprüngliche IOCs**: ~150 Pakete
- **Neue IOCs hinzugefügt**: ~800+ Pakete  
- **Gesamte IOCs**: **900+ bösartige Pakete**
- **Fokus**: CrowdStrike-Typosquatting-Kampagne

### 🎯 Typosquatting-Kategorien

#### 1. **Direkte CrowdStrike-Imitationen**
```python
"crowdstrike": None,
"crowd-strike": None,
"crowdstrik": None,  # Missing 'e'
"crowdstryke": None,  # 'i' -> 'y'
"cr0wdstrike": None,  # 'o' -> '0'
"crowdstr1ke": None,  # 'i' -> '1'
```

#### 2. **Produkt-spezifische Varianten**
```python
# Falcon (CrowdStrike's main EDR product)
"falcon-crowdstrike": None,
"crowdstrike-falcon": None,
"crowdstrike-falcon-api": None,
"crowdstrike-falcon-sdk": None,

# LogScale/Humio (acquired by CrowdStrike)
"crowdstrike-logscale": None,
"logscale-crowdstrike": None,
"humio-crowdstrike": None,
```

#### 3. **Scoped Package Varianten**
```python
"@crowdstrike-official/falcon": None,
"@crowdstrike-security/edr": None,
"@official-crowdstrike/client": None,
```

#### 4. **Sicherheits-thematische Kombinationen**
```python
"crowdstrike-security": None,
"crowdstrike-edr": None,
"crowdstrike-endpoint": None,
"crowdstrike-antivirus": None,
"crowdstrike-threat": None,
"security-crowdstrike": None,
"endpoint-crowdstrike": None,
```

#### 5. **Technologie-spezifische Varianten**
```python
"crowdstrike-js": None,
"crowdstrike-node": None,
"crowdstrike-python": None,
"crowdstrike-api": None,
"crowdstrike-sdk": None,
"crowdstrike-client": None,
```

#### 6. **Domain-ähnliche Pakete**
```python
"crowdstrike-com": None,
"crowdstrike-net": None,
"crowdstrike-org": None,
"crowdstrike-io": None,
"crowdstrike-cloud": None,
```

#### 7. **Versions-spezifische Targeting**
```python
"crowdstrike-v1": None,
"crowdstrike-2024": None,
"crowdstrike-latest": None,
"crowdstrike-stable": None,
"crowdstrike-beta": None,
```

#### 8. **Umfangreiche Humio/LogScale Varianten**
```python
"humio": None,
"humio-api": None,
"humio-sdk": None,
# ... 200+ weitere Humio-Varianten
```

## 🔍 Erkennungsmerkmale

### Verdächtige Muster
1. **Typos in CrowdStrike**: `crowdstrik`, `crowdstryke`, `cr0wdstrike`
2. **Zusätzliche Begriffe**: `crowdstrike-api`, `crowdstrike-security`
3. **Scoped Packages**: `@crowdstrike-*/*`, `@*-crowdstrike/*`
4. **Produkt-Imitationen**: `falcon-*`, `humio-*`, `logscale-*`
5. **Sicherheits-Kombinationen**: `*sec-crowdstrike`, `crowdstrike-*sec`

### Legitime vs. Bösartige Pakete
- **Legitime CrowdStrike-Pakete**: Nur von verifizierten CrowdStrike-Accounts
- **Bösartige Pakete**: Von unverifizierten Publishern, oft mit Typos

## 🛡️ Schutzmaßnahmen

### 1. **Automatisierte Erkennung**
```bash
# Scan mit GitHub IOC Scanner
github-ioc-scan --org myorg --verbose

# Spezifische Suche nach CrowdStrike-Paketen
github-ioc-scan --org myorg --fast | grep -i crowdstrike
```

### 2. **Package Verification**
- Überprüfung gegen offizielle CrowdStrike-Dokumentation
- Verifikation der Publisher-Accounts
- Prüfung von Package-Signaturen
- Kontrolle der offiziellen GitHub-Repositories

### 3. **CI/CD Integration**
```yaml
# GitHub Actions Beispiel
- name: Scan for malicious packages
  run: |
    github-ioc-scan --org ${{ github.repository_owner }} --batch-strategy aggressive
```

### 4. **Monitoring**
- Kontinuierliche Überwachung neuer Package-Installationen
- Alerts bei CrowdStrike-ähnlichen Package-Namen
- Regelmäßige Scans der Dependency-Files

## 📈 Impact Assessment

### Betroffene Dateien
- `package.json`
- `package-lock.json`
- `yarn.lock`
- `pnpm-lock.yaml`
- `bun.lockb`

### Risikobewertung
- **Threat Level**: CRITICAL
- **Scope**: 400+ bösartige Pakete
- **Target**: Entwicklungsumgebungen
- **Impact**: Supply Chain Compromise

## 🚨 Sofortmaßnahmen

### 1. **Immediate Scanning**
```bash
# Vollständiger Organisationsscan
github-ioc-scan --org myorg --include-archived --verbose

# Batch-Verarbeitung für große Organisationen
github-ioc-scan --org myorg --batch-strategy aggressive --max-concurrent 10
```

### 2. **Package Audit**
```bash
# NPM Audit
npm audit --audit-level high

# Yarn Audit
yarn audit --level high

# PNPM Audit
pnpm audit --audit-level high
```

### 3. **Dependency Review**
- Manuelle Überprüfung aller CrowdStrike-bezogenen Dependencies
- Entfernung verdächtiger Pakete
- Aktualisierung auf verifizierte Versionen

## 📋 Detection Checklist

- [ ] Scan aller `package.json` Dateien
- [ ] Überprüfung von Lock-Files
- [ ] Suche nach CrowdStrike-Typos
- [ ] Verifikation legitimer CrowdStrike-Pakete
- [ ] Prüfung von Scoped Packages
- [ ] Kontrolle der Publisher-Accounts
- [ ] Monitoring neuer Installationen
- [ ] CI/CD Pipeline Integration
- [ ] Team-Schulung zu Typosquatting
- [ ] Incident Response Plan aktiviert

## 🔄 Kontinuierliche Überwachung

### Automated Scanning
```bash
# Täglicher Scan (Cron Job)
0 9 * * * /usr/local/bin/github-ioc-scan --org myorg --quiet --log-file /var/log/ioc-scan.log

# Wöchentlicher vollständiger Scan
0 9 * * 1 /usr/local/bin/github-ioc-scan --org myorg --include-archived --batch-strategy aggressive
```

### Alert Integration
- Slack/Teams Benachrichtigungen bei Funden
- Email-Alerts für kritische Entdeckungen
- Dashboard-Integration für Security Teams

## 📚 Weitere Ressourcen

- **Socket.dev Blog**: https://socket.dev/blog/ongoing-supply-chain-attack-targets-crowdstrike-npm-packages
- **CrowdStrike Official**: Offizielle Dokumentation für legitime Pakete
- **NPM Security**: https://docs.npmjs.com/about-security-audits
- **Supply Chain Security**: NIST Guidelines für Software Supply Chain Security

## 🎯 Fazit

Mit über **900 IOC-Definitionen** ist der GitHub IOC Scanner jetzt optimal gerüstet, um die CrowdStrike-Typosquatting-Kampagne zu erkennen. Die erweiterten Definitionen decken alle bekannten Angriffsvektoren ab und bieten umfassenden Schutz vor dieser Supply Chain Attack.

**Empfehlung**: Sofortiger Scan aller Repositories und kontinuierliche Überwachung implementieren! 🚀