; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!
; Generates install script for Windows 7

#define MyAppName "AutoInventory"
#define MyAppVersion "0.6.1"
#define MyAppPublisher "Scott"
#define MyAppExeName "AutoInventory.exe"
#define Dir "E:\AutoInventory"

[Setup]
; NOTE: The value of AppId uniquely identifies this application. Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{DAA11DFC-2825-4D6B-B0D4-B4D0447BD9E6}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DisableProgramGroupPage=yes
; Uncomment the following line to run in non administrative install mode (install for current user only.)
PrivilegesRequired=lowest
;PrivilegesRequiredOverridesAllowed=dialog
OutputDir={#Dir}\Setup Scripts\Inno Setup
OutputBaseFilename=AutoInventory-Installer-win7
SetupIconFile={#Dir}\Images\pizza_hut_logo.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
MinVersion=6.1.7600

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "{#Dir}\Setup Scripts\dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#Dir}\Setup Scripts\dist\update.exe"; DestDir: "{app}"; Flags: onlyifdoesntexist
Source: "{#Dir}\config_default_win7.ini"; DestDir: "{app}"; DestName: "config.ini"; Flags: onlyifdoesntexist
Source: "{#Dir}\VERSION.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#Dir}\README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#Dir}\Images\settings_button.png"; DestDir: "{app}\Images"; Flags: ignoreversion
Source: "{#Dir}\chromedriver.exe"; DestDir: "{app}"; Flags: onlyifdoesntexist
Source: "{#Dir}\LICENSE.chromedriver"; DestDir: "{app}"; Flags: onlyifdoesntexist
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall

