# VR Adventures For Children

Quick start and build instructions for the project.

## Prerequisites
- Unity Editor version : Unity 2025
- Visual Studio or VS Code (for editing scripts).
- Git (to clone repository).
- For Android builds: Android Build Support installed via Unity Hub.
- For VR hardware: relevant XR Plugin packages configured (OpenXR, Oculus, SteamVR as required).

## Clone the repository
```bash
git clone https://github.com/lankireddyhiteshreddy/ARVR_PROJECT.git
cd VR_Adventures_For_Children
```

## Open and run in Unity Editor
1. Open Unity Hub and add the `VR_Adventures_For_Children` folder as a project.
2. Open the project in Unity Editor.
3. Open `TestingGround.unity` or any scenario scene (Earthquake, Traffic, Inferno) you want to test.
4. Press Play to run in the Editor.

## Build for Windows
1. File > Build Settings
2. Add desired scenes to the "Scenes in Build" list.
3. Select PC, Mac & Linux Standalone and target Windows.
4. Click Build and choose output folder.

## Build for Android
1. Install Android Build Support in Unity Hub for the Editor version used.
2. File > Build Settings > Switch Platform to Android.
3. Configure Player Settings (package id, min SDK).
4. Connect Android device or emulator, then click Build and Run.

## XR / VR notes
- If you plan to run with VR hardware, go to Project Settings > XR Plug-in Management and enable the appropriate plugin for your hardware.
- Confirm input bindings and controllers in the Input Manager or the XR Interaction package.

## Sample Test Case (Earthquake safe-zone)
1. Open `EarthquakeScene.unity` in the Editor.
2. Press Play.
3. Wait for instructions, then move to the safe zone when the earthquake starts.
4. Verify that the UI shows success when you reach the safe zone in time.

## Files of interest
- `Assets/Scripts/PlayerInteraction.cs` — handles object interactions.
- `Assets/Scripts/TrackedMovement.cs`, `Assets/Scripts/Move.cs` — player movement and tracking.
- `Assets/Scripts/InfernoController.cs` — inferno/fire simulation logic.
- `Assets/Scripts/CollisionHandler.cs` — collision and trigger events.

## Contributions
- Hitesh — Earthquake module and UI feedback.
- Rohit — Traffic module and NPC movement.
- Kalyan — Inferno/fire module and extinguish interactions.
