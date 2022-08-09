# Sailfish OS application sandboxing and permissions

Sailfish OS application sandboxing and permissions system is build on top of
Firejail. The Firejail documentation can be found from [here](https://firejail.wordpress.com/).

The Sailfish OS application permissions are applicable only to sandboxed applications. Since
Sailfish OS 4.4.0 all applications that do not specifically opt-out or define permissions are
sandboxed automatically using a default profile.

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
    Exec=harbour-myapp

    [X-Sailjail]
    Permissions=Internet;Pictures
    OrganizationName=org.foobar
    ApplicationName=MyApp

The Exec line should match the name of the desktop file in _/usr/share/applications_.
If the name does not match, use **/usr/bin/sailjail** to start the application and pass the file
name of the desktop file with **-p** option. If you are developing an app which is intended
for Harbour, you should not use path on the Exec line. In other cases, refer to the application 
binary with the full path.

To declare permissions and data directories you need to add **X-Sailjail** section to the
desktop file. This is called _an application profile_. Under the **X-Sailjail** section add

| Keyword | Description |
| :---    | :---        |
| Permissions | Semi-colon separated list of requested permissions |
| OrganizationName | Application development organization as a reverse domain name |
| ApplicationName | Application name |

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

Applications that are not using the Sailfish App library
([libsailfishapp](https://github.com/sailfishos/libsailfishapp)) for their initialization must
ensure that correct organization and application name is set.

    ...
    QGuiApplication *app = ...;
    app->setOrganizationName(QStringLiteral("org.foobar"));
    app->setApplicationName(QStringLiteral("MyApp"));
    ...

When Sailfish App library is used, these values are set automatically to the values
set in application's Desktop Entry file.

Sandboxed applications cannot use `QSettings` constructed with the default arguments - it would use
an inaccessible path outside `QStandardPaths::AppDataLocation`. A suitable settings file path needs
to be determined explicitly.

    const QString settingsPath =
        QStandardPaths::writableLocation(QStandardPaths::AppConfigLocation)
        + "/" + QCoreApplication::applicationName() + ".conf";
    QSettings settings(settingsPath, QSettings::NativeFormat);

Unless you are creating a new application, it is also necessary to take care about migrating
application data and configuration from the old location outside the sandbox.

An example of how `QSettings`-based configuration may be migrated:

    if (!settings.contains("migrated")) {
        const QString oldSettingsPath =
            QStandardPaths::writableLocation(QStandardPaths::ConfigLocation)
            + "/" + QCoreApplication::applicationName()
            + "/" + QCoreApplication::applicationName() + ".conf";
        QSettings oldSettings(oldSettingsPath, QSettings::NativeFormat);

        for (const QString &key : oldSettings.childKeys())
            settings.setValue(key, oldSettings.value(key));

        settings.setValue("migrated", "true");
    }

Similarly with QML `LocalStorage`:

    QDir dbDir(QStandardPaths::writableLocation(QStandardPaths::AppLocalDataLocation)
            + "/QML/OfflineStorage/Databases/");
    if (!dbDir.exists()) {
        QDir oldDbDir(QStandardPaths::writableLocation(QStandardPaths::GenericDataLocation)
                + "/" + QCoreApplication::applicationName()
                + "/" + QCoreApplication::applicationName()
                + "/QML/OfflineStorage/Databases/");

        dbDir.mkpath(".");

        const QStringList dbFiles = oldDbDir.entryList({"*.sqlite", "*.ini"}, QDir::Files);
        for (const QString &dbFile : dbFiles) {
            if (!QFile::copy(oldDbDir.filePath(dbFile), dbDir.filePath(dbFile)))
                ...
        }
    }

### Files shared with other applications

Directories under user home such as Documents, Downloads, Music, Pictures and Videos contain files that
are available for applications with respective permissions. Those directories must be used when the
data needs to be accessible by other applications.

If application doesn't have a permission for a directory, all data in that directory will be hidden
and the application sees only an empty read-only directory in that path. This allows to regular file
access checks to function in expected way.

## Sandboxing of applications without application profile

If application does not define application profile, i.e. **X-Sailjail** section in its desktop file,
a default profile may be applied. This is defined by configuration (see
_config/50-default-profile.conf_) and applies a relaxed set of permissions which should be
compatible with most existing and well-behaving applications. It specifically does not grant access
to any sensitive data normally protected by _privileged_ group.

Some assumptions about the application are made:
- The application has only one binary as specified by _Exec_ key in desktop file
- The application installs its own files in _/usr/share/\<app binary name\>_
- The application stores its own private data in _~/.local/share/\<app binary name\>_
- The application stores its config data in _~/.config/\<app binary name\>_
- The application stores its cached data in _~/.cache/\<app binary name\>_
- The application stores common data in user directories as specified by UserDirs or on memory card
- The application doesn't need access to other application's data outside those common directories
- The application doesn't need access to privileged data
- The application doesn't need access to privileged or otherwise private D-Bus APIs

## Permissions

Permissions that applications may use (names are subject to change):

|  Permission  | Description |
|  :---        | :---        |
| [Accounts](https://github.com/sailfishos/sailjail-permissions/blob/master/permissions/Accounts.permission) | Using accounts, including editing them. Syncing accounts. |
| [Ambience](https://github.com/sailfishos/sailjail-permissions/blob/master/permissions/Ambience.permission) | Set and edit ambiences. |
| [AppLaunch](https://github.com/sailfishos/sailjail-permissions/blob/master/permissions/AppLaunch.permission) | Launching and stopping systemd services. This is usually needed for background tasks. |
| [ApplicationInstallation](https://github.com/sailfishos/sailjail-permissions/blob/master/permissions/ApplicationInstallation.permission) | Installing and uninstalling applications. |
| [Audio](https://github.com/sailfishos/sailjail-permissions/blob/master/permissions/Audio.permission) | Playing and recording audio (since Pulseaudio streams cannot be separated both are enabled with this, but it is subject to change), changing audio configuration and showing audio controls on lockscreen. |
| [Bluetooth](https://github.com/sailfishos/sailjail-permissions/blob/master/permissions/Bluetooth.permission) | Connecting to and using Bluetooth hardware. |
| [Calendar](https://github.com/sailfishos/sailjail-permissions/blob/master/permissions/Calendar.permission) | Display and editing of calendar events. |
| [CallRecordings](https://github.com/sailfishos/sailjail-permissions/blob/master/permissions/CallRecordings.permission) | Access recorded calls. |
| [Camera](https://github.com/sailfishos/sailjail-permissions/blob/master/permissions/Camera.permission) | Access to camera hardware to take photos or video. |
| [CommunicationHistory](https://github.com/sailfishos/sailjail-permissions/blob/master/permissions/CommunicationHistory.permission) | Access call and message history. |
| [Contacts](https://github.com/sailfishos/sailjail-permissions/blob/master/permissions/Contacts.permission) | Display and editing of contacts data. Access to contact cards. |
| [Documents](https://github.com/sailfishos/sailjail-permissions/blob/master/permissions/Documents.permission) | Access to Documents directory. |
| [Downloads](https://github.com/sailfishos/sailjail-permissions/blob/master/permissions/Downloads.permission) | Access to Downloads directory. |
| [Email](https://github.com/sailfishos/sailjail-permissions/blob/master/permissions/Email.permission) | Reading and sending emails. Access to email attachments. |
| [Internet](https://github.com/sailfishos/sailjail-permissions/blob/master/permissions/Internet.permission) | Using data connection and connecting to internet. |
| [Location](https://github.com/sailfishos/sailjail-permissions/blob/master/permissions/Location.permission) | Use GPS and positioning. |
| [MediaIndexing](https://github.com/sailfishos/sailjail-permissions/blob/master/permissions/MediaIndexing.permission) | Access to Tracker to list files on device. If you have access to a data directory, you may want to use also this. |
| [Messages](https://github.com/sailfishos/sailjail-permissions/blob/master/permissions/Messages.permission) | Access to message data and to send SMS messages. |
| [Microphone](https://github.com/sailfishos/sailjail-permissions/blob/master/permissions/Microphone.permission) | Record audio with microphone. Use Audio permission for playback of the recorded audio (but since Pulseaudio streams cannot be separated this enables also audio playback, which is subject to change). |
| [Music](https://github.com/sailfishos/sailjail-permissions/blob/master/permissions/Music.permission) | Access to Music directory, playlists and coverart cache. |
| [NFC](https://github.com/sailfishos/sailjail-permissions/blob/master/permissions/NFC.permission) | Connecting to and using NFC hardware. |
| [Phone](https://github.com/sailfishos/sailjail-permissions/blob/master/permissions/Phone.permission) | Make Phone calls, either directly or through system voice call UI. |
| [Pictures](https://github.com/sailfishos/sailjail-permissions/blob/master/permissions/Pictures.permission) | Access to Pictures directory and thumbnails. |
| [PublicDir](https://github.com/sailfishos/sailjail-permissions/blob/master/permissions/PublicDir.permission) | Access to Public directory. |
| [RemovableMedia](https://github.com/sailfishos/sailjail-permissions/blob/master/permissions/RemovableMedia.permission) | Use memory cards and USB sticks. |
| [Synchronization](https://github.com/sailfishos/sailjail-permissions/blob/master/permissions/Synchronization.permission) | Access to synchronization framework. |
| [UserDirs](https://github.com/sailfishos/sailjail-permissions/blob/master/permissions/UserDirs.permission) | Access to Documents, Downloads, Music, Pictures, Public and Video directories. |
| [Videos](https://github.com/sailfishos/sailjail-permissions/blob/master/permissions/Videos.permission) | Access to Videos directory and thumbnails. |
| [WebView](https://github.com/sailfishos/sailjail-permissions/blob/master/permissions/WebView.permission) | If you use Gecko based WebView you need this. |

Internal permissions that applications generally should not use directly:
| Permission | Description |
| :---       | :---        |
| [Base](https://github.com/sailfishos/sailjail-permissions/blob/master/permissions/Base.permission)   | Base set of permissions that every application is granted implicitly. |
| [CaptivePortal](https://github.com/sailfishos/sailjail-permissions/blob/master/permissions/CaptivePortal.permission) |
| [Compatibility](https://github.com/sailfishos/sailjail-permissions/blob/master/permissions/Compatibility.permission) | Access to binaries for compatibility. Direct use of binaries should be avoided. Please note that this permission is provided in order to support old applications, new applications should try to use other means. The binaries may disappear in any release, for any reason, but especially if we provide APIs with similar functionality. |
| [Connman](https://github.com/sailfishos/sailjail-permissions/blob/master/permissions/Connman.permission) |
| [FingerprintSensor](https://github.com/sailfishos/sailjail-permissions/blob/master/permissions/FingerprintSensor.permission) |
| [GnuPG](https://github.com/sailfishos/sailjail-permissions/blob/master/permissions/GnuPG.permission) |
| [Notifications](https://github.com/sailfishos/sailjail-permissions/blob/master/permissions/Notifications.permission) |
| [PinQuery](https://github.com/sailfishos/sailjail-permissions/blob/master/permissions/PinQuery.permission) |
| [Secrets](https://github.com/sailfishos/sailjail-permissions/blob/master/permissions/Secrets.permission) |
| [Sensors](https://github.com/sailfishos/sailjail-permissions/blob/master/permissions/Sensors.permission) |
| [Sharing](https://github.com/sailfishos/sailjail-permissions/blob/master/permissions/Sharing.permission) |
| [Thumbnails](https://github.com/sailfishos/sailjail-permissions/blob/master/permissions/Thumbnails.permission) |
| [UDisks](https://github.com/sailfishos/sailjail-permissions/blob/master/permissions/UDisks.permission) | Permissions to call UDisks functions, includes UDisksListen. |
| [UDisksListen](https://github.com/sailfishos/sailjail-permissions/blob/master/permissions/UDisksListen.permission) | Permissions to listen signals and property changes on UDisks2 interfaces. |

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
