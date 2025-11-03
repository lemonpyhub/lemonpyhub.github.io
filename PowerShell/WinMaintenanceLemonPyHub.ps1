# ╔════════════════════════════════════════════════════════════╗
# ║     Windows Maintenance Tool v4.1.0 - LΣⱮØπPy              ║
# ║     Developer: LemonPyHub                                  ║
# ╚════════════════════════════════════════════════════════════╝
# Designed to be run with:
#   iwr -useb https://git.io/WinMaintenanceLemonPyHub | iex
# or saved as a .ps1 and run locally.
#
# PowerShell classic (Windows PowerShell 5.x) compatible.
# ==================================================================

# Ensure UTF-8 output
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# ---------------- Configuration ----------------
# The public shortlink / raw URL to re-run when self-elevating in piped mode.
# Update this if you host raw elsewhere.
$OnlineLauncherShortLink = 'https://git.io/WinMaintenanceLemonPyHub'
# (If you later change shortlink, update the hosted raw target accordingly.)

# ---------------- Helpers ----------------
function Write-Log {
    param($Text, $Color = 'White')
    Write-Host $Text -ForegroundColor $Color
}

function Pause-WaitForKey {
    param($Message = 'Press any key to continue...')
    Write-Host $Message -ForegroundColor Cyan
    # Use RawUI so piped contexts still wait
    try { $null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown') } catch { Read-Host | Out-Null }
}

function SafeStartAndWait {
    param($ExePath, $Args)
    try {
        Start-Process -FilePath $ExePath -ArgumentList $Args -Wait -ErrorAction Stop
        return $true
    } catch {
        Write-Log "❌ Error running $ExePath $Args : $($_.Exception.Message)" Red
        return $false
    }
}

# Prevent silent exit: trap all terminating errors and show info
$global:ErrorActionPreference = 'Continue'
trap {
    Write-Log "❌ Unhandled error: $($_.Exception.Message)" Red
    Write-Log "Stack: $($_.ScriptStackTrace)" DarkRed
    Write-Log "Script will remain open for debugging. Press Enter to continue..." Yellow
    Read-Host | Out-Null
    continue
}

# ---------------- OS detection & capability flags ----------------
function Get-OSInfo {
    try {
        $os = Get-CimInstance Win32_OperatingSystem -ErrorAction Stop
        $ver = [version]$os.Version
        return @{ Caption = $os.Caption; Version = $ver; Build = [int]$os.BuildNumber }
    } catch {
        return @{ Caption = 'Unknown'; Version = [version]'0.0.0.0'; Build = 0 }
    }
}

function Detect-OSAndCapabilities {
    $info = Get-OSInfo
    $v = $info.Version
    $caps = @{
        OSName = 'Unknown'
        SupportsOptimizeVolume = $false
        SupportsGetPhysicalDisk = $false
        SupportsCheckpointComputer = $false
        SupportsClearRecycleBinCmdlet = $false
    }

    if ($v.Major -ge 10) {
        $caps.OSName = 'Windows 10/11'
        $caps.SupportsOptimizeVolume = $true
        $caps.SupportsGetPhysicalDisk = $true
        $caps.SupportsCheckpointComputer = $true
        # Clear-RecycleBin is part of Shell in some PS versions; attempt to check
        if (Get-Command -Name Clear-RecycleBin -ErrorAction SilentlyContinue) { $caps.SupportsClearRecycleBinCmdlet = $true }
        else { $caps.SupportsClearRecycleBinCmdlet = $false }
    } elseif ($v.Major -eq 6 -and $v.Minor -eq 1) {
        $caps.OSName = 'Windows 7'
        # many modern modules not available
    } elseif ($v.Major -eq 6 -and ($v.Minor -eq 2 -or $v.Minor -eq 3)) {
        $caps.OSName = 'Windows 8/8.1'
        $caps.SupportsOptimizeVolume = $true  # usually available in 8+ (but be cautious)
        $caps.SupportsGetPhysicalDisk = $false
    } else {
        $caps.OSName = 'Unknown/Older'
    }

    # try to detect Get-PhysicalDisk availability at runtime
    if (Get-Command -Name Get-PhysicalDisk -ErrorAction SilentlyContinue) { $caps.SupportsGetPhysicalDisk = $true }

    return @{ Info = $info; Caps = $caps }
}

$detected = Detect-OSAndCapabilities
$OSInfo = $detected.Info
$Caps = $detected.Caps

# ---------------- Self-elevation that works for piped (iex) & file modes ----------------
function Ensure-RunAsAdmin-OnlineFriendly {
    try {
        $isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
    } catch {
        $isAdmin = $false
    }

    if (-not $isAdmin) {
        Write-Log "Requesting administrative privileges..." Yellow

        # if running from a saved file path, relaunch with -File (safe)
        if ($MyInvocation.MyCommand.Path) {
            $scriptFile = $MyInvocation.MyCommand.Path
            $args = @('-NoProfile','-ExecutionPolicy','Bypass','-File',$scriptFile)
            Start-Process -FilePath (Get-Command powershell).Source -ArgumentList $args -Verb RunAs
            # exit non-elevated instance
            exit
        } else {
            # piped/iex mode — relaunch elevated and re-download the script using the configured shortlink
            # Build a single -Command argument safely
            $cmd = "iwr -useb '$OnlineLauncherShortLink' | iex"
            $args = @('-NoProfile','-ExecutionPolicy','Bypass','-Command',$cmd)
            Start-Process -FilePath (Get-Command powershell).Source -ArgumentList $args -Verb RunAs
            exit
        }
    }
}

# Run Ensure-RunAsAdmin-OnlineFriendly early so the elevated re-run will fetch the same URL
Ensure-RunAsAdmin-OnlineFriendly

# ---------------- UI helpers ----------------
function Print-Header {
    Clear-Host
    $t = (Get-Date).ToString('HH:mm:ss')
    Write-Host ""
    Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor DarkCyan
    Write-Host "║     Windows Maintenance Tool v4.1.0 - LΣⱮØπPy             ║" -ForegroundColor Yellow
    Write-Host "║     Developer: LemonPyHub                                  ║" -ForegroundColor Yellow
    Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor DarkCyan
    Write-Host ""
    Write-Host "[$t] Detected OS: $($OSInfo.Caption) (Version: $($OSInfo.Version))" -ForegroundColor Cyan
    if ($Caps.OSName -eq 'Windows 7') {
        Write-Host "⚠️  Detected Windows 7 — some features are disabled or show guidance for compatible commands." -ForegroundColor Yellow
    }
    Write-Host ""
}

# ---------------- Menu & actions ----------------
function Show-Menu-And-Run {
    while ($true) {
        Print-Header

        # Build menu items conditional on capabilities (hide items for Win7)
        $itemsLeft = @()
        $itemsRight = @()

        # core items always available
        $items = @()
        $items += @{Id=1; Text='[1] Clear files in Temp folder'}
        $items += @{Id=2; Text='[2] Clear files in Prefetch folder'}
        $items += @{Id=3; Text='[3] Clear files in Windows Temp folder'}
        $items += @{Id=4; Text='[4] Run Disk Cleanup'}
        $items += @{Id=5; Text='[5] Empty Recycle Bin'}
        $items += @{Id=6; Text='[6] Run SFC'}
        $items += @{Id=7; Text='[7] Run DISM'}

        # conditional items
        if ($Caps.OSName -ne 'Windows 7') {
            $items += @{Id=8; Text='[8] Optimize Storage (Defrag/Trim)'}
            $items += @{Id=9; Text='[9] Drive Health Check'}
            $items += @{Id=10; Text='[10] Create System Restore Point'}
        } else {
            # For Win7 show alternate text or guidance
            $items += @{Id=8; Text='[8] Optimize Storage (NOT SUPPORTED on Win7)'}
            $items += @{Id=9; Text='[9] Drive Health (limited on Win7)'}
            $items += @{Id=10; Text='[10] Create Restore Point (Use System Protection GUI on Win7)'}
        }

        $items += @{Id=11; Text='[11] Open Msconfig'}
        $items += @{Id=12; Text='[12] IP Release'}
        $items += @{Id=13; Text='[13] Flush DNS'}
        $items += @{Id=14; Text='[14] IP Renew'}
        $items += @{Id=15; Text='[15] Exit'}

        # split into two columns (1..7 left, others right) but preserve ordering
        $colLeft = $items | Where-Object { $_.Id -le 7 }
        $colRight = $items | Where-Object { $_.Id -ge 8 }

        $maxLines = [math]::Max($colLeft.Count, $colRight.Count)
        for ($i = 0; $i -lt $maxLines; $i++) {
            $leftTxt = if ($i -lt $colLeft.Count) { $colLeft[$i].Text } else { "" }
            $rightTxt = if ($i -lt $colRight.Count) { $colRight[$i].Text } else { "" }
            "{0,-50}{1}" -f $leftTxt, $rightTxt
        }

        Write-Host ""
        $choice = Read-Host "Enter your choice (1-15)"

        try {
            switch ($choice) {
                1 {
                    Write-Log "`nCleaning: $env:LOCALAPPDATA\Temp" Cyan
                    try { Get-ChildItem "$env:LOCALAPPDATA\Temp" -Recurse -Force -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue; Write-Log "Temp folder cleaned." Green } catch { Write-Log "Error cleaning Temp: $($_.Exception.Message)" Red }
                }
                2 {
                    Write-Log "`nCleaning: C:\Windows\Prefetch" Cyan
                    try { Get-ChildItem "C:\Windows\Prefetch" -Recurse -Force -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue; Write-Log "Prefetch cleaned." Green } catch { Write-Log "Error cleaning Prefetch: $($_.Exception.Message)" Red }
                }
                3 {
                    Write-Log "`nCleaning: C:\Windows\Temp" Cyan
                    try { Get-ChildItem "C:\Windows\Temp" -Recurse -Force -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue; Write-Log "Windows Temp cleaned." Green } catch { Write-Log "Error cleaning Windows Temp: $($_.Exception.Message)" Red }
                }
                4 {
                    Write-Log "`nRunning Disk Cleanup (no prompt)..." Cyan
                    # Note: /verylowdisk requests minimal UI and more aggressive cleanup on modern Windows
                    SafeStartAndWait "$env:SystemRoot\System32\cleanmgr.exe" "/verylowdisk"
                }
                5 {
                    Write-Log "`nEmptying Recycle Bin..." Cyan
                    if (Get-Command -Name Clear-RecycleBin -ErrorAction SilentlyContinue) {
                        try { Clear-RecycleBin -Force -ErrorAction SilentlyContinue; Write-Log "Recycle Bin emptied." Green } catch { Write-Log "Error emptying Recycle Bin: $($_.Exception.Message)" Red }
                    } else {
                        # Fallback for older systems: use shell object
                        try {
                            $shell = New-Object -ComObject Shell.Application
                            $recycle = $shell.Namespace(0xA)
                            $items = $recycle.Items()
                            if ($items.Count -gt 0) { $recycle.InvokeVerb("empty") }
                            Write-Log "Recycle Bin emptied (COM fallback)." Green
                        } catch { Write-Log "Recycle Bin empty failed: $($_.Exception.Message)" Red }
                    }
                }
                6 {
                    Write-Log "`nRunning SFC /scannow..." Cyan
                    SafeStartAndWait (Get-Command sfc -ErrorAction SilentlyContinue).Source "/scannow"
                }
                7 {
                    Write-Log "`nRunning DISM /RestoreHealth..." Cyan
                    # DISM may not be fully available on older OS; the command wrapper will surface errors
                    SafeStartAndWait (Get-Command DISM -ErrorAction SilentlyContinue).Source "/Online","/Cleanup-Image","/RestoreHealth"
                }
                8 {
                    if ($Caps.OSName -eq 'Windows 7') {
                        Write-Log "`nOptimize Storage is not supported on Windows 7.`nUse third-party tools or built-in Disk Defragmenter GUI." Yellow
                    } else {
                        Write-Log "`nStarting Optimize Storage (Detect SSD/HDD, Trim/Defrag)..." Cyan
                        # Only target fixed local disks
                        $logical = Get-CimInstance Win32_LogicalDisk -ErrorAction SilentlyContinue | Where-Object { $_.DriveType -eq 3 }
                        if (-not $logical) { Write-Log "No local fixed drives found." Yellow } else {
                            # Determine SSD/HDD best-effort
                            foreach ($ld in $logical) {
                                $driveLetter = $ld.DeviceID.TrimEnd(':')
                                $isSSD = $false
                                if ($Caps.SupportsGetPhysicalDisk) {
                                    try {
                                        $pdisks = Get-PhysicalDisk -ErrorAction SilentlyContinue
                                        if ($pdisks -and ($pdisks | Where-Object { $_.MediaType -eq 'SSD' })) { $isSSD = $true }
                                    } catch {}
                                } else {
                                    # fallback heuristic: check drive model / media via Win32_DiskDrive mapping (not always reliable)
                                    try {
                                        $disk = Get-WmiObject Win32_DiskDrive -ErrorAction SilentlyContinue | Where-Object { $_.Partitions -gt 0 } | Select-Object -First 1
                                        if ($disk -and $disk.Model -match 'SSD|Solid State') { $isSSD = $true }
                                    } catch {}
                                }

                                if ($isSSD) {
                                    Write-Log "🔵 SSD detected on $driveLetter — running Optimize-Volume -ReTrim" Cyan
                                    try { Optimize-Volume -DriveLetter $driveLetter -ReTrim -ErrorAction Stop; Write-Log "SSD optimized for $driveLetter" Green } catch { Write-Log "SSD optimize error for $driveLetter: $($_.Exception.Message)" Red }
                                } else {
                                    Write-Log "🟡 Treating $driveLetter as HDD — running defrag" Yellow
                                    SafeStartAndWait (Join-Path $env:SystemRoot 'System32\defrag.exe') "$driveLetter /O /U"
                                }
                            }
                        }
                    }
                }
                9 {
                    if ($Caps.OSName -eq 'Windows 7') {
                        Write-Log "`nDrive health checks on Win7 are limited. Use chkdsk or manufacturer tools." Yellow
                        Write-Log "Example: chkdsk C: /F (requires reboot if busy)" Cyan
                    } else {
                        Write-Log "`nRunning basic drive health reports..." Cyan
                        # Quick health read using Get-PhysicalDisk or SMART via WMI
                        if ($Caps.SupportsGetPhysicalDisk) {
                            try {
                                Get-PhysicalDisk | Select-Object FriendlyName, SerialNumber, MediaType, HealthStatus | Format-Table -AutoSize
                            } catch {
                                Write-Log "Error retrieving physical disk info: $($_.Exception.Message)" Red
                            }
                        } else {
                            try {
                                Get-WmiObject -Class Win32_DiskDrive | Select-Object Model, InterfaceType, MediaType | Format-Table -AutoSize
                            } catch {
                                Write-Log "Drive query failed: $($_.Exception.Message)" Red
                            }
                        }
                        Pause-WaitForKey
                    }
                }
                10 {
                    if ($Caps.SupportsCheckpointComputer -and $Caps.OSName -ne 'Windows 7') {
                        Write-Log "`nCreating system restore point..." Cyan
                        try { Checkpoint-Computer -Description "ManualRestorePoint" -RestorePointType "MODIFY_SETTINGS" -ErrorAction Stop; Write-Log "Restore point created." Green } catch { Write-Log "Restore point failed: $($_.Exception.Message)" Red }
                    } else {
                        Write-Log "`nSystem Restore point creation not supported on this OS via this script." Yellow
                        Write-Log "On Windows 7: open System -> System Protection -> Create..." Cyan
                    }
                }
                11 {
                    Write-Log "`nOpening msconfig..." Cyan
                    try { Start-Process msconfig -ErrorAction Stop } catch { Write-Log "Failed to open msconfig: $($_.Exception.Message)" Red }
                }
                12 {
                    Write-Log "`nReleasing IP..." Cyan
                    try { ipconfig /release | Out-Null; Write-Log "IP released." Green } catch { Write-Log "IP release error: $($_.Exception.Message)" Red }
                }
                13 {
                    Write-Log "`nFlushing DNS cache..." Cyan
                    try { ipconfig /flushdns | Out-Null; Write-Log "DNS flushed." Green } catch { Write-Log "Flush DNS failed: $($_.Exception.Message)" Red }
                }
                14 {
                    Write-Log "`nRenewing IP..." Cyan
                    try { ipconfig /renew | Out-Null; Write-Log "IP renewed." Green } catch { Write-Log "IP renew failed: $($_.Exception.Message)" Red }
                }
                15 {
                    Write-Log "`nThank you for using Windows Maintenance Tool!" Cyan
                    Write-Log "Exiting in 2 seconds..." Yellow
                    Start-Sleep -Seconds 2
                    return
                }
                Default {
                    Write-Log "Invalid choice. Try again." Red
                    Start-Sleep -Seconds 1
                }
            }
        } catch {
            Write-Log "❌ Unexpected error while processing choice: $($_.Exception.Message)" Red
            Start-Sleep -Seconds 2
        }

        # brief pause then loop
        Start-Sleep -Milliseconds 300
    }
}

# ---------------- Main ----------------
try {
    Show-Menu-And-Run
} catch {
    Write-Log "Critical error: $($_.Exception.Message)" Red
    Write-Log "Script will pause for debugging (60s)..." Yellow
    Start-Sleep -Seconds 60
} finally {
    Write-Log "`nSession ended." Cyan
}
