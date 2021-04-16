# Sailfish OS application sandboxing and permissions

Sailfish OS application sandboxing and permissions system is build on top of
Firejail. The Firejail documentation can be found from [here](https://firejail.wordpress.com/).

The Sailfish OS application permissions are applicable only to sandboxed applications. Target is to
have application sandboxing enforced to all applications but currently we are not there yet. Note
that permission system is only available for 1st and 2nd party application developers.

Application launch happens via standard desktop file that has been augmented
so that it contains necessary metadata (such as a list of requested permissions)
and [Sailjail launcher](https://github.com/sailfishos/sailjail/) is used to execute the application
binary.

Permissions that an application can request are defined in this package, in terms of
files containing standard Firejail directives and Sailfish OS specific metadata.

## Enable sandboxing for an application

There are few changes needed for an application in order to run
it in a sandbox.

### Desktop file changes

Let's go through needed changes via an example.

    [Desktop Entry]
    Type=Application
    Name=MyApplication
    Icon=my-app-icon
    Exec=/usr/bin/sailjail -p org.foobar.myapp.desktop /usr/bin/org.foobar.myapp
    [X-Sailjail]
    Permissions=Internet;Pictures
    OrganizationName=org.foobar
    ApplicationName=myapp

For Exec line use **sailjail** to start the application, pass the file name of the desktop file,
and refer to the application binary with the full path.

To declare permissions and data directories you need to add **X-Sailjail** section to the
desktop file. Under the **X-Sailjail** section add

| Keyword | Description |
| :---    | :---        |
| Permissions | Semi-colon separated list of requested permissions |
| OrganizationName | Application development organization |
| ApplicationName | Application data folder |

Permissions are listed [later in the document](#Permissions). They grant access to certain data
paths, D-Bus interfaces, socket types and application binaries. Currently applications must define
all needed permissions in desktop file and all of them are granted at launch.

OrganizationName and ApplicationName is used for granting for the application write access to

1. $HOME/.local/share/\<OrganizationName\>/\<ApplicationName\>
2. $HOME/.cache/\<OrganizationName\>/\<ApplicationName\>
3. $HOME/.config/\<OrganizationName\>/\<ApplicationName\>

Access above directories from the application through QStandardPaths
1. Application data location - QStandardPaths::writableLocation(QStandardPaths::AppDataLocation)
2. Application cache location - QStandardPaths::writableLocation(QStandardPaths::CacheLocation)
3. Application config location  - QStandardPaths::writableLocation(QStandardPaths::ConfigLocation)

Only these directories can be used for storing application specific data that needs to persist over
application restarts.

### Use correct application data directories

Modify Qt application main function by setting the organization and application name
to match the declaration added to the desktop file.

    QScopedPointer<QGuiApplication> app(Sailfish::createApplication(argc, argv));
    ...
    app->setOrganizationName(QStringLiteral("org.foobar"));
    app->setApplicationName(QStringLiteral("myapp"));
    ...

When Sailfish App library (libsailfishapp) is used these values are set automatically to the values
set in desktop file.

### Files shared with other applications

Directories under user home such as Documents, Downloads, Music, Pictures and Videos contain files that
are available for applications with respective permissions. Those directories must be used when the
data needs to be accessible by other applications.

If application doesn't have a permission for a directory, all data in that directory will be hidden
and the application sees only an empty read-only directory in that path. This allows to regular file
access checks to function in expected way.

## Permissions

Permissions that applications may use (names are subject to change):

| Permission | Description |
| :---       | :---        |
| Accounts   | Using accounts, including editing them. Syncing accounts. |
| Ambience   | Set and edit ambiences. |
| AppLaunch  | Launching and stopping systemd services. This is usually needed for background tasks. |
| ApplicationInstallation | Installing and uninstalling applications. |
| Audio | Playing audio, changing audio configuration and showing audio controls on lockscreen. |
| Bluetooth | Connecting to and using Bluetooth and NFC hardware. |
| Calendar | Display and editing of calendar events. |
| CallRecordings | Access recorded calls. |
| Camera | Access to camera hardware to take photos or video. |
| Contacts | Display and editing of contacts data. Access to contact cards. |
| Documents | Access to Documents directory. |
| Downloads | Access to Downloads directory. |
| Email | Reading and sending emails. Access to email attachments. |
| Internet | Using data connection and connecting to internet. |
| Location | Use GPS and positioning. |
| MediaIndexing | Access to Tracker to list files on device. If you have access to a data directory, you may want to use also this. |
| Messages | Access to message data and to send SMS messages. |
| WebView | If you use Gecko based WebView you need this. |
| Music | Access to Music directory, playlists and coverart cache. |
| Phone | Make Phone calls, either directly or through system voice call UI. |
| Pictures | Access to Pictures directory and thumbnails. |
| PublicDir | Access to Public directory. |
| Sharing | Use of sharing pages in the application to share data via Bluetooth, email or other accounts. |
| Synchronization | Access to synchronization framework. |
| UserDirs | Access to Documents, Downloads, Music, Pictures, Public and Video directories. |
| Videos | Access to Videos directory and thumbnails. |

Internal permissions that applications generally should not use directly:
| Permission | Description |
| :---       | :---        |
| Base       | Base set of permissions that every application is granted implicitly. |
| CaptivePortal |
| Connman |
| DataStorages |
| GnuPG |
| FingerprintSensor |
| Microphone |
| Notifications |
| PinQuery |
| Sensors |
| Thumbnails |
| UDisks | Permissions to call UDisks functions, includes UDisksListen. |
| UDisksListen | Permissions to listen signals and property changes on UDisks2 interfaces. |

### Permission metadata format

The metadata is used to generate translations build time and to display useful
information on UI about the permissions.

Permission files have metadata in their comments. Each metadata line begins
with comment character '#' and key that begins with x-sailjail- followed by '='
character and the value. Below you can find the keys that permissions should
define.

| Keyword | Description |
| :---    | :---        |
| x-sailjail-translation-catalog | This key defines Qt translation catalog name which translations for the metadata should be retrieved from |
| x-sailjail-translation-key-description | This key defines translation key for short description |
| x-sailjail-description | This key defines engineering english text for short description |
| x-sailjail-translation-key-long-description | This key defines translation key for long description |
| x-sailjail-long-description | This key defines engineering english text for long description. |
