# Move Docker Desktop to External SSD on Windows

## Overview

This guide shows you how to move Docker Desktop’s data from your C: drive to an external SSD on Windows. This is necessary because the built-in Docker Desktop setting for changing disk image location often doesn’t work properly.

## Why Move Docker Data?

- Docker images and containers can consume 50GB+ of space
- Free up your system drive (C:) for better performance
- Use your larger external SSD for Docker storage
- All downloaded images, containers, and volumes will use the new location

## Prerequisites

- Docker Desktop installed on Windows
- External SSD connected and formatted (e.g., D: or E: drive)
- Administrator access to PowerShell or Command Prompt
- **Important**: This process will preserve your existing Docker data

## Step-by-Step Process

### Step 1: Check Current Docker WSL Distributions

Open PowerShell or Command Prompt and run:

```powershell
wsl --list --verbose
```

You should see something like:

```
NAME                   STATE           VERSION
docker-desktop         Running         2
docker-desktop-data    Running         2
```

**Note**: `docker-desktop-data` is the large distribution containing all your images, containers, and volumes. This is what we’ll move.

### Step 2: Shut Down Docker and WSL

Close Docker Desktop completely, then run:

```powershell
wsl --shutdown
```

Wait a few seconds to ensure everything has stopped.

### Step 3: Create Target Directory on External SSD

Replace `D:` with your external drive letter:

```powershell
mkdir D:\Docker\data
```

### Step 4: Export Docker Data Distribution

This creates a backup tar file of your Docker data:

```powershell
wsl --export docker-desktop-data D:\Docker\docker-desktop-data.tar
```

**This may take several minutes** depending on how much Docker data you have (images, containers, volumes). Be patient!

### Step 5: Unregister the Old Distribution

This removes the distribution from the C: drive:

```powershell
wsl --unregister docker-desktop-data
```

**Warning**: Make sure Step 4 completed successfully before running this command!

### Step 6: Import to New Location

Import the distribution to your external SSD:

```powershell
wsl --import docker-desktop-data D:\Docker\data D:\Docker\docker-desktop-data.tar --version 2
```

This recreates the distribution on your external drive.

### Step 7: Clean Up Temporary File

Delete the temporary tar file to save space:

```powershell
del D:\Docker\docker-desktop-data.tar
```

### Step 8: Verify the Move

Check that the distribution is now in the new location:

```powershell
wsl --list --verbose
```

You should still see both distributions listed.

### Step 9: Start Docker Desktop

Launch Docker Desktop normally. It should start without issues and recognize all your existing containers and images.

### Step 10: Test Everything Works

Pull a test image to verify it’s using the external drive:

```powershell
docker pull hello-world
docker run hello-world
```

## Verification

To confirm Docker is using your external drive:

1. Check the file size of `D:\Docker\data\ext4.vhdx`
1. This file will grow as you add more Docker images and containers
1. Your C: drive should have significantly more free space

## Optional: Move docker-desktop Distribution (Usually Not Needed)

The `docker-desktop` distribution is typically small (< 1GB) and doesn’t need to be moved. But if you want to move it anyway:

```powershell
wsl --shutdown
wsl --export docker-desktop D:\Docker\docker-desktop.tar
wsl --unregister docker-desktop
wsl --import docker-desktop D:\Docker\desktop D:\Docker\docker-desktop.tar --version 2
del D:\Docker\docker-desktop.tar
```

## Troubleshooting

### Docker Desktop won’t start after moving

1. Make sure your external drive is connected and powered on
1. Run `wsl --list --verbose` to check distributions are registered
1. Try `wsl --shutdown` and restart Docker Desktop

### “Cannot create a specific network” error during import

Simply re-run the import command:

```powershell
wsl --import docker-desktop-data D:\Docker\data D:\Docker\docker-desktop-data.tar --version 2
```

### Lost all my Docker data

If you still have the `.tar` file from Step 4, you can re-import it:

```powershell
wsl --import docker-desktop-data D:\Docker\data D:\Docker\docker-desktop-data.tar --version 2
```

### External drive letter changed

If your external drive letter changes (e.g., from D: to E:), you’ll need to:

1. Export the distribution again
1. Unregister it
1. Import to the new drive letter

## Moving Back to C: Drive

If you need to move back:

```powershell
wsl --shutdown
wsl --export docker-desktop-data C:\Users\YourUsername\docker-desktop-data.tar
wsl --unregister docker-desktop-data
wsl --import docker-desktop-data C:\Users\YourUsername\AppData\Local\Docker\wsl\data C:\Users\YourUsername\docker-desktop-data.tar --version 2
del C:\Users\YourUsername\docker-desktop-data.tar
```

## Important Notes

- **Always keep your external drive connected** when using Docker
- If you disconnect the drive, Docker Desktop will fail to start
- The external drive should be formatted as NTFS
- For SSDs, consider one with good write endurance as Docker writes frequently

## Alternative: Symbolic Links (Advanced)

Some users prefer creating symbolic links instead. This is more complex and riskier, so the export/import method above is recommended.

## Summary

After completing these steps:

- ✅ All Docker images will be stored on your external SSD
- ✅ All new containers will use the external drive
- ✅ Your C: drive will have more free space
- ✅ Docker Desktop will work normally with the external drive connected

-----

**Questions or issues?** Check the Docker Desktop logs at:
`C:\Users\YourUsername\AppData\Local\Docker\log.txt`