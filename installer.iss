[Setup]
AppName=SNAP Curator
AppVersion=1.0.0
DefaultDirName={commonpf64}\SNAP Curator
DefaultGroupName=SNAP Curator
OutputBaseFilename=SNAP-Curator-Setup
Compression=lzma
SolidCompression=yes
PrivilegesRequired=lowest
UninstallDisplayIcon={app}\SNAP-Curator.exe
OutputDir=.

[Files]
Source: "dist\SNAP-Curator.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "launch_app.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "launch_app.vbs"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{userdesktop}\SNAP Curator"; Filename: "{app}\launch_app.bat"; IconFilename: "{app}\SNAP-Curator.exe"; WorkingDir: "{app}"
Name: "{group}\SNAP Curator"; Filename: "{app}\launch_app.bat"; IconFilename: "{app}\SNAP-Curator.exe"; WorkingDir: "{app}"

[Run]
Filename: "{app}\launch_app.bat"; Description: "Launch SNAP Curator"; Flags: postinstall nowait
