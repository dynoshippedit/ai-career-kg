---
lesson_id: a-windows-concepts
slug: windows-concepts
stage: A
level: 2
prerequisites: [a-linux-cli]
roles: [soc-analyst, security-analyst, pentester]
map_refs: []
test_date: 2026-10-09
description: "Windows concepts for security: the registry, services, event logs and PowerShell — the Linux lesson's concepts in Windows form, taught from Microsoft's own docs with exact reader procedures. A free lesson in the security guidebook."
dateline: "Hands-on steps not run by us (no Windows on the build machine) · Microsoft docs fetched and verified 2026-10-09 · deepened 2026-10-10 (execution policy section from Microsoft's PowerShell-Docs; fixed §7 duplicate URL with registry-value-types reference)"
---
# Windows concepts for security


**Map refs:** Stage A foundation; pairs with `a-linux-cli`; feeds `c-log-sources` (Windows event IDs) and `d-malware-analysis` (Windows-native analysis).

---

## 1. Where this shows up

The servers you will attack in Stage B are Linux. The *victims* in Stage C and D are very often Windows: the workstation that got phished, the domain controller, the server running the business application. Incident response, malware analysis, and SOC triage all assume you can navigate a Windows machine the way `a-linux-cli` taught you to navigate Linux — and the concepts transfer directly, because both systems answer the same questions: where is configuration stored, what is running, who did what, and where is it written down. The answers just live in different places with different names. This lesson is that translation table, taught from Microsoft's own documentation. Nothing below was executed on the build machine — there is no Windows here — so every hands-on step is written as an exact procedure for *your* Windows VM, marked **not run by us**.

## 2. Before you start

- A Windows machine you own: a VM (VirtualBox/UTM/Hyper-V) or a spare laptop. Never practice on someone else's system.
- `a-linux-cli` finished — this lesson constantly says "the Windows equivalent of *that Linux thing*."
- PowerShell (ships with Windows — no install). You will use PowerShell, not CMD: it is the shell Microsoft documents and the one every modern tool speaks.
- Administrator access on your VM for the log-reading steps (Windows, like Linux, gates its security logs behind privilege).

## 3. How it works

**The registry: configuration as a database.** Linux scatters configuration across text files in `/etc`; Windows centralizes it in the registry — a hierarchical database of keys, subkeys, and values. The top level has five hives (Microsoft's "Registry Hives" reference, fetched 2026-10-09): `HKEY_LOCAL_MACHINE` (HKLM — the whole machine: hardware, drivers, services, machine-wide software), `HKEY_CURRENT_USER` (HKCU — the signed-in user's settings; a live view into that user's branch under `HKEY_USERS`), `HKEY_USERS` (all loaded user profiles), `HKEY_CLASSES_ROOT` (file associations — a merged view of machine and user classes), and `HKEY_CURRENT_CONFIG` (the current hardware profile, assembled at boot). The security-relevant fact Microsoft's own page states plainly: most hive files live in `%SystemRoot%\System32\Config` (SAM, SECURITY, SOFTWARE, SYSTEM), while each user's hive is their `NTUSER.DAT`. Two things follow that matter for security work: first, *persistence* — malware and legitimate software alike register themselves to start at boot via `Run` keys under HKLM or HKCU, which is why "check the Run keys" is a first-response reflex; second, *evidence* — the registry records what was installed, what ran, and who logged on, which is why forensic analysis reads hives from disk images.

**Values have types.** `REG_SZ` (string), `REG_DWORD` (32-bit number), `REG_BINARY`, `REG_MULTI_SZ` (string list), `REG_QWORD`, `REG_EXPAND_SZ` (string with expandable `%variables%`). When you read a value, the type tells you how to interpret the bytes — a `REG_DWORD` of `1` under a policy key usually means "enabled." Misreading the type is the registry equivalent of misreading a permission bit.

**Services: the Windows daemon.** Linux has systemd units; Windows has services — background processes managed by the Service Control Manager. `Get-Service` lists them; each has a name, display name, status (Running/Stopped), and start type (Automatic/Manual/Disabled). The security angle is identical to Linux daemons: a service runs with an *account* (LocalSystem is effectively root — maximum privilege), starts automatically, and is a persistence mechanism. An unfamiliar service set to Automatic, running as LocalSystem, pointing at an executable in a user-writable directory, is the Windows shape of "investigate this now." The registry backs this too: service definitions live under `HKLM\SYSTEM\CurrentControlSet\Services`.

**Event logs: where Windows writes everything down.** Linux has `/var/log` and the journal; Windows has the Event Log — structured records in channels, each event with an ID, a provider, and XML details. The three classic channels: **Application**, **System**, and **Security**. The Security channel is the crown jewel: logon events (4624 success, 4625 failure — the pair every SOC analyst knows), account management (4720 created, 4726 deleted), privilege use (4672), and 1102 (the audit log was cleared — the "someone is covering tracks" event). `c-log-sources` builds the full ID vocabulary on this foundation; this lesson is where you learn the log *exists* and how to query it.

**PowerShell: the shell that returns objects.** This is the deep difference from bash. Where Linux pipes *text* (`ps | grep`), PowerShell pipes *objects* with named properties: `Get-WinEvent -LogName Security -MaxEvents 10` returns event objects, and `| Select-Object TimeCreated, Id, Message` picks properties — no `cut -d' ' -f7` fragility, because fields are named, not positional. Microsoft's `Get-WinEvent` documentation (fetched 2026-10-09) shows the query patterns: `-ListLog *` inventories the logs; `-FilterHashtable @{LogName='Security'; ID=4625}` filters server-side (fast) instead of pulling everything and filtering client-side (slow) — the exact performance discipline `c-log-sources`' awk pipelines teach for Linux logs. Verbs are standardized (`Get-`, `Set-`, `Start-`, `Stop-`), so `Get-Service`, `Get-Process`, `Get-EventLog` are guessable once you know the pattern.

**PowerShell execution policy: the gate in front of every script.** Before any `.ps1` in this lesson runs on your VM, you will meet the **execution policy** — PowerShell's safety feature controlling when scripts may run (Microsoft's `about_Execution_Policies` reference, fetched 2026-10-10). The policies that matter: `Restricted` (the effective default on Windows clients — individual commands work, no script files run), `RemoteSigned` (scripts you wrote locally run; scripts downloaded from the internet must be signed by a trusted publisher or explicitly unblocked with `Unblock-File`), `AllSigned` (everything signed), and `Bypass` (nothing blocked). Two facts make this a security lesson rather than a configuration note. First, Microsoft states plainly that the execution policy **is not a security boundary** — it is defense in depth; anything it stops can be re-typed at the prompt or launched with `pwsh.exe -ExecutionPolicy Bypass`, and malware does exactly that. Second, it is *scoped*: `Get-ExecutionPolicy -List` shows the policy per scope — `MachinePolicy`/`UserPolicy` (Group Policy, highest precedence), `Process` (this session only, gone when it closes), `CurrentUser`, `LocalMachine`. The reader's move is `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`: it permits your own scripts without touching other users or weakening the machine default, and it needs no administrator rights. The analyst's move is the inverse: when you find `Bypass` set at a wide scope, or scripts launching with `-ExecutionPolicy Bypass` in scheduled tasks and logon scripts, that is a *finding* — someone (or something) chose to drop the gate.

**The translation table.** Keep this beside you until it's reflex:

| Linux (`a-linux-cli`) | Windows (this lesson) | Same question |
|---|---|---|
| `/etc` text files | Registry hives | Where is configuration? |
| systemd services | Windows services (`Get-Service`) | What runs at boot, as whom? |
| `/var/log`, `journalctl` | Event Log (`Get-WinEvent`) | Who did what, when? |
| `ps`, `kill` | `Get-Process`, `Stop-Process` | What is running now? |
| file permissions (rwx) | NTFS ACLs | Who can touch this file? |
| `sudo` / setuid | "Run as administrator" / UAC | How does privilege escalate? |

**NTFS permissions and UAC, briefly.** Windows files carry access-control *lists* (who: allow/deny) rather than the triple-bitmask — finer-grained, harder to read at a glance, same purpose. Privilege escalation prompts through UAC (User Account Control): the "do you want to allow this" dialog is the boundary between your user token and the administrator token. Malware's first job is often getting past it silently — which is why unexpected UAC prompts are a detection signal, not an annoyance.

### Worked example: reading the machine (procedure)

On your Windows VM, as Administrator, in PowerShell — each step marked **not run by us** (no Windows on the build bench):

1. **Inventory the logs.** `Get-WinEvent -ListLog * | Select-Object LogName, RecordCount, IsEnabled | Format-Table -AutoSize` — the Windows equivalent of `ls /var/log/`. Note which logs are enabled and which have records.
2. **Read the registry's shape.** Open `regedit`, navigate `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services` — count the subkeys (each is a service definition). Then `HKCU\Software\Microsoft\Windows\CurrentVersion\Run` — the current user's persistence point. *Look, don't change.*
3. **List services as objects.** `Get-Service | Where-Object {$_.Status -eq 'Running'} | Select-Object Name, DisplayName, StartType` — compare against the registry count from step 2. Same data, two views.
4. **Query failed logons.** `Get-WinEvent -FilterHashtable @{LogName='Security'; ID=4625} -MaxEvents 5 | Select-Object TimeCreated, Message` — the exact command Microsoft's own community uses for this question. If your VM has no failures yet, deliberately mistype your password at the lock screen once, then re-run: *cause* the event, then *find* it. That loop — act, then detect — is the whole of defensive learning.
5. **Check a process.** `Get-Process | Sort-Object CPU -Descending | Select-Object -First 5 Name, Id, CPU` — the `ps` equivalent, with objects instead of text columns.

## 4. Walkthrough

**Not run by us** — no Windows machine exists on the build bench, and this lesson will not invent command output. The transcript (`runs/a-windows-concepts.log`) records the in-session verification that *was* possible: both Microsoft documentation pages fetched and their key claims confirmed (registry hive definitions and supporting-file table; `Get-WinEvent` syntax, `-FilterHashtable` filtering, and the 4624/4625 logon event IDs). Every hands-on step below is an exact procedure for your own Windows VM.

1. **Verify the hive table.** Open Microsoft's "Registry Hives" page (link in §7). Confirm the five hives and their supporting files match the table in §3. This is primary-source reading as a lab exercise.
2. **Inventory event logs** — `Get-WinEvent -ListLog *` on your VM (Administrator PowerShell). Record which of Application/System/Security has the highest `RecordCount`.
3. **Find the Run keys** — in `regedit`, visit both `HKLM\...\Run` and `HKCU\...\Run`. List every value. For each, note the executable path and ask: do I know what this is?
4. **Generate and find a 4625** — mistype your password once at the lock screen, then run the `Get-WinEvent -FilterHashtable @{LogName='Security'; ID=4625}` query. Confirm your attempt appears with the right timestamp.
5. **Compare service views** — count subkeys under the Services registry key; count `Get-Service` output. They should agree; if they don't, you have found something worth understanding.
6. **Meet the execution-policy gate.** `Get-ExecutionPolicy -List` — read every scope and identify the effective policy and which scope wins. If it is `Restricted`, your `.ps1` files will not run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` (no admin needed), then re-run the list to confirm. Save a one-line script (`"hello-policy"` in `hello.ps1`) and run it — note that it now works, and that `-Scope Process` would have given you the same result for this session only. Then find where the gate is *not*: run `pwsh -ExecutionPolicy Bypass -Command '"the gate is a suggestion"'` and say out loud what this proves about who the policy protects against — hint: not malware. **Not run by us** (no Windows on the bench); exact procedure for your VM.

## 5. On your own

**Task:** On your Windows VM: (a) export the list of Automatic-start services to a CSV (`Get-Service | Where-Object {$_.StartType -eq 'Automatic'} | Export-Csv auto.csv`), open it, and identify every service whose executable path you cannot explain — research each one until you can; (b) find the most recent 4624 (successful logon) in your Security log and identify the logon type; (c) pick one registry value under `HKCU` and trace what application behavior it controls (change nothing — read only).

**Success test:** Your service list has no unexplained entries; you can state what logon type your 4624 was and what that type means; your registry trace names the application and the setting.

**Hints:** `Get-WinEvent -FilterHashtable @{LogName='Security'; ID=4624} -MaxEvents 1 | Format-List -Property *` shows all properties including Logon Type. Service executable paths: `Get-CimInstance Win32_Service | Select-Object Name, PathName`.

## 6. Where it goes wrong

- **Editing the registry to "fix" things.** The registry has no undo and no validation — a wrong value can make the machine unbootable. Read freely; change only with a backup (`reg export`) and a reason. Tutorials that tell you to delete keys are telling you to risk the OS.
- **Disabling UAC.** The prompt is the privilege boundary made visible. Disabling it for convenience removes the one interactive check between you and silent elevation.
- **Running everything as Administrator.** The Windows twin of running as root: it hides permission errors and makes every mistake system-wide. Elevate per-task, not per-session.
- **Trusting the GUI alone.** Event Viewer shows the same data `Get-WinEvent` returns, but the GUI doesn't scale and doesn't script. Learn the cmdlet form from the start — your future SIEM queries are the same shape.
- **"Fixing" scripts with `Set-ExecutionPolicy Bypass`.** When a script won't run, the wrong answer is dropping the gate machine-wide — it trains you to dismantle a safety feature and it protects against nothing determined anyway. The right answer is `RemoteSigned` at `CurrentUser` scope: your own scripts run, internet downloads still get questioned, nobody else is affected. A `Bypass` at `LocalMachine` scope is something you *investigate*, not something you set.
- **Assuming "Windows is different" means "the concepts don't transfer."** Every row of the translation table is the same question. The analyst who knows *what to ask* learns the new names in a day; the one who memorized commands starts over.

## 7. Read the source

Primary documents first — Microsoft documents its own system:

- **Registry Hives** (learn.microsoft.com/en-us/windows/win32/sysinfo/registry-hives — verified 2026-10-09) — *read* the hive definitions and the supporting-files table; this is the authoritative statement of what lives where on disk.
- **Get-WinEvent** (learn.microsoft.com/en-us/powershell/module/microsoft.powershell.diagnostics/get-winevent — verified 2026-10-09) — *read* the Description and the `-FilterHashtable`/`-FilterXPath` parameter sets; *skim* the examples. This is the cmdlet reference for every log query in this lesson.
- **Registry value types** (learn.microsoft.com/en-us/windows/win32/sysinfo/registry-value-types — verified 2026-10-10) — the authoritative type table: `REG_SZ`, `REG_DWORD`, `REG_MULTI_SZ`, `REG_EXPAND_SZ`, `REG_QWORD`, `REG_BINARY`. *Read* the type definitions; *skim* the string-handling notes. This is what §3's "values have types" paragraph summarizes — now check it against the source.
- **about_Execution_Policies** (Microsoft's PowerShell-Docs repo, `reference/7.4/Microsoft.PowerShell.Core/About/about_Execution_Policies.md` — verified 2026-10-10) — *read* the policy list (Restricted/RemoteSigned/AllSigned/Bypass/Undefined), the scope-and-precedence section, and the "isn't a security boundary" paragraph. This is the source behind §3's execution-policy section; read it before you decide what `Bypass` in a logon script means.

Then at most three free resources:

1. **Microsoft Learn — PowerShell modules** (learn.microsoft.com/powershell — the docs hub, verified via the Get-WinEvent page 2026-10-09) — the reference for every cmdlet in this lesson; learn to read a cmdlet page the way you learned to read a man page.
2. **The Ultimate Windows Event Log guide** — deliberately *not* listed: most online "complete event ID" lists are unverified aggregations. Use `c-log-sources` in this program instead, which builds its ID table from primary sources.
3. *(Third slot intentionally empty — the two Microsoft primary documents above plus the docs hub are the authoritative core; padding the list would dilute it.)*

## 8. Check yourself

1. `HKCU` is described as "a shortcut." Explain, precisely, what it is a shortcut *to*, and why editing `HKCU\Software\...` and the corresponding `HKU\<SID>\Software\...` key shows the same data.
2. A service runs as LocalSystem with StartType Automatic and its executable in `C:\Users\Public\`. Name the three facts that make this worth investigating, in the order you'd check them.
3. Why is `-FilterHashtable @{LogName='Security'; ID=4625}` preferable to `Get-WinEvent -LogName Security | Where-Object {$_.Id -eq 4625}`? (Two reasons: performance and one more.)
4. Event 1102 appears in the Security log. What does it mean, and why does its *presence* matter more than most events' presence?
5. Translate this Linux triage pipeline into its PowerShell equivalent, naming what changes about the data between the pipes: `grep 'Failed password' /var/log/auth.log | cut -d' ' -f11 | sort | uniq -c | sort -rn`.
6. A scheduled task on a server you are reviewing launches `pwsh.exe -ExecutionPolicy Bypass -File C:\Tools\sync.ps1`. Name two things that are wrong with this picture — one about what the flag proves, one about where you'd look next — and state the correct scope/policy pair for letting your own maintenance scripts run.

## 9. Prove it

**Artifact:** A "Windows first-look" report on your VM: the Automatic-service inventory with every entry explained, the Run-key contents with verdicts, and the three most recent 4624/4625 events interpreted (who, when, what logon type). Written up, with the commands you ran.

**Honest claim:** "I can navigate a Windows system's configuration, services, and event logs from PowerShell, explain the execution policy and set it safely at the right scope, and explain what I find — demonstrated on my own VM, report linked here."

**You cannot yet claim:** forensic analysis of a compromised Windows host (disk images, timeline analysis, malware behavior) — that's `d-malware-analysis` and Stage D incident-response work, which build on this foundation.

## 10. Leads to

- `c-log-sources` — the full Windows event-ID vocabulary (4624/4625/4720/1102 and friends) in the SOC context.
- `d-malware-analysis` — Windows-native analysis: the registry and services knowledge becomes persistence-hunting.
- `c-soc-triage` — where the 4625 query becomes an alert you triage.
