# Script explanations — VR_Adventures_For_Children

This document lists the C# scripts present in the project and provides a detailed, easy-to-read explanation of what each one does and where it is used (scene or purpose). Use this as a reference when you want to review or modify behavior.

---

## Inferno (fire / extinguisher)

- `Assets/InfernoController.cs`
  - Purpose: Controls the inferno (wildfire) behavior in the Inferno scene. On Start it initializes the wildfire scale and (after the patch) begins a coroutine that activates the wildfire after a 5‑second delay. In Update it increases the wildfire's localScale by `changeInFire`. When the extinguisher is in hand and the wildfire scale falls below a threshold it disables the wildfire. The `pickupExtinguisher()` method toggles the extinguisher objects and reduces the growth rate of the fire.
  - Notes: The script manipulates GameObjects bound in the scene (extinguisherOnWall, extinguisherInHand, wildfire). It uses a coroutine to delay activation.

- `Assets/PlayerInteraction.cs`
  - Purpose: A simple trigger-based interaction helper used by scenes (notably Inferno). When another collider enters the object's trigger it inspects the collider's tag (prints debug messages) and calls `InfernoController.pickupExtinguisher()` to notify the Inferno controller that the player picked up the extinguisher.
  - Notes: The script expects the player GameObject to be tagged `Player` and a reference to the `InfernoController` to be assigned in the Inspector.

---

## Earthquake

- `Assets/Scripts/StartEarthquakeTimer.cs`
  - Purpose: A gaze-interaction timer that triggers earthquake-related actions. It extends `ObjectController` (from `SojaExiles` package or similar) and tracks how long the user gazes at the object; if gaze time exceeds `GazeTime` it calls `btnn()` (which currently logs and could be expanded to start the quake sequence).
  - Notes: Used by Earthquake scene for starting timed interactions via gaze.

- `Assets/Scripts/CameraShaker.cs`
  - Purpose: Drives camera shaking and high-level earthquake flow. It contains logic to compute Perlin-noise-based camera offsets, start/stop earthquake sequences, show a warning message, evaluate whether the player survived depending on position, display the result UI, and return to the home scene. It also orchestrates start/stop timing using `Invoke()`.
  - Notes: Uses a `trauma` parameter to control shake intensity. Tightly coupled to Earthquake scene GameObjects (MainDoor, ComputerTableGround, WarningMessage, ResultUI).

- `Assets/Scripts/GroundShaker.cs`
  - Purpose: Applies physics-free positional shaking to a transform to simulate ground movement. In FixedUpdate it computes a randomized move vector and applies it to the transform's position to mimic an earthquake.
  - Notes: Useful for grounding objects and making a convincing quake.

- `Assets/Scripts/BuildingShaker.cs`
  - Purpose: (Used in Earthquake scene) Shakes building pieces or attached transforms to give the impression of buildings being affected by the earthquake. Usually used together with `GroundShaker` and `CameraShaker`.

---

## Traffic (cars / road / vehicle movement)

- `Assets/AutoMove.cs`
  - Purpose: A generic auto-movement script for rigidbody-driven objects (vehicles). It sets the rigidbody velocity forward at a fixed speed and, on colliding with an object tagged `Boundary`, instantiates a prefab at the initial position then destroys the object (a simple pooling/respawn pattern).
  - Notes: Used by the TrafficSafety scene to make cars move along roads and respawn.

- `Assets/Scripts/CollisionHandler.cs`
  - Purpose: Central collision handling for interactive props (vehicles/pedestrians). Typically used to trigger scoring, to show warnings, or to apply damage/response to collisions between moving objects in the Traffic scene.

---

## Player & Movement (shared)

- `Assets/Scripts/PlayerMovement.cs`
  - Purpose: Primary character controller for the player. It exposes a `CharacterController`, movement speed, rotation speed, gravity, and VR-specific tilt-based movement (angleMove). When the player tilts the headset forward beyond a set pitch it moves forward automatically (tilt-to-walk). Also supports keyboard input, rotation, gravity handling, and optional crouch toggling.
  - Notes: Used across scenes where a first-person viewpoint is required.

- `Assets/Scripts/PlayerMovement2.cs`
  - Purpose: An alternate movement controller similar to `PlayerMovement` that simplifies certain controls and uses `SimpleMove` when angle movement is enabled. It also supports keyboard movement and gravity. Parameters like `toggleAngle` and `speed` are exposed for tuning.
  - Notes: Keep both movement scripts if different scenes or prefabs reference them — decide on a single movement implementation only after checking scene attachments.

- `Assets/Brick Project Studio/_BPS ... /First Person Player/PlayerMovement.cs` (3rd-party)
  - Purpose: Player movement included with the Brick Project Studio asset package. It controls the first-person prefab provided by that asset and is referenced by prefab instances.
  - Notes: Treat this as third-party. Do not edit unless needed — better to override behavior via your own controller.

- `Assets/Square Head Character Free Demo/.../SquareHeadMovement.cs` (sample)
  - Purpose: Movement script for a demo character included with sample assets.

---

## Main Scene / Scene selection & Gaze UI (shared)

- `Assets/Scripts/MainSceneGazes.cs`
  - Purpose: Main menu / scene-selection gaze controller. When the player gazes at interactive objects for `GazeTime`, it checks distance and the object's name to decide which scene to load: `Car_B1` → `TrafficSafety`, `Building` → `Earthquake`, `Extinguisher` → `Inferno`. Provides `OnPointerEnter()` and `OnPointerExit()` for gaze state.
  - Notes: The scene names are hard-coded here and are the entry points to each mini-experience.

- `Assets/Scripts/GazeReticle.cs`
  - Purpose: Renders and updates the reticle (gaze cursor) and manages visual feedback during gaze interactions.

- `Assets/Scripts/TableGaze.cs`
  - Purpose: Gaze logic for table-scene interactions — likely used for selecting objects on a table or triggering local actions.

- `Assets/Scripts/PopUpController.cs`
  - Purpose: Controls on-screen popups and instructional overlays. It is used to display guidance and to show/hide messages based on game state.

- `Assets/Scripts/UIPositionFront.cs`
  - Purpose: Keeps UI elements positioned in front of the player camera; useful in VR to ensure canvas elements remain reachable/visible.

- `Assets/Scripts/UIInteractions.cs`
  - Purpose: Generic UI helper for button presses, gaze button handling, and other input-to-UI glue.

---

## Utilities & small helpers (shared)

- `Assets/Scripts/CameraMovement.cs`
  - Purpose: Helper to move the camera or switch camera behavior during play (editor/testing and some cutscenes). Not the same as the `CameraShaker` which produces earthquake noise.

- `Assets/Scripts/TrackedMovement.cs`
  - Purpose: Generic scripted movement for objects that must follow a path or be tracked to a moving target; used by scene props.

- `Assets/Scripts/TurnLightOnOff.cs`
  - Purpose: Toggles light GameObjects on/off. Handy for creating night/day or switchable lamps in scenes.

- `Assets/Scripts/ChummaMove.cs` and `Assets/Scripts/ChummaCollisionHandler.cs`
  - Purpose: Small utility/test scripts used for prototyping or local demonstrations. They provide simple move and collision handling for test objects.

---

## Effects / Visual plugins / third-party packages

These files are part of imported packages or visual plugins. I list them with short purpose notes — they are generally not authored by you and often belong to packages such as Brick Project Studio, Unity's ParticlePack, QuickOutline, and other asset store packages.

- `Assets/QuickOutline/Scripts/Outline.cs` — Visual outline component used to highlight objects when selected or focused.

- `Assets/UnityTechnologies/ParticlePack/Shared/Scripts/SimpleCameraController.cs` — Part of the ParticlePack sample. Provides a camera controller for sample scenes.
- `Assets/UnityTechnologies/ParticlePack/Shared/Scripts/ProximityActivate.cs` — Activates particle effects when the player is nearby.
- `Assets/UnityTechnologies/ParticlePack/Shared/Scripts/SimpleCharacterMotor.cs` — Sample character motor used in the ParticlePack demos.
- `Assets/UnityTechnologies/ParticlePack/EffectExamples/Misc Effects/Scripts/SpawnEffect.cs` — Demonstration script to spawn a particle effect on trigger.
- `Assets/UnityTechnologies/ParticlePack/Shared/Ramps/...` — editor/runtime support for particle ramp assets.

- Brick Project Studio scripts (many files under `Assets/Brick Project Studio/...`) — these include `opencloseDoor.cs`, `opencloseWindow.cs`, drawer scripts, `SceneSwitchGen.cs`, and more. Purpose: provide interactive furniture/building behaviors for the building prefabs (doors, drawers, flipping tables, etc.).

- Square Head Character demo scripts and readme helpers — included to support the demo character prefabs.

---

## XR / Cardboard sample scripts

- `Assets/Samples/Google Cardboard XR Plugin for Unity/.../VrModeController.cs` — Cardboard VR bootstrap; it toggles VR mode and initializes XR subsystems. Useful if you want consistent VR initialization across scenes (add it to a persistent manager or main menu).
- `Assets/Samples/Google Cardboard XR Plugin for Unity/.../CardboardStartup.cs` — Cardboard sample start logic.
- Several other Cardboard sample scripts are present (ObjectController, GraphicsAPITextController) used by the sample scenes.

---

## Editor / sample-specific / README helpers

- `Assets/Square Head Character Free Demo/Readme/Scripts/Readme.cs` and `Editor/ReadmeEditor.cs` — helper and editor-time code for the demo package README.
- `Assets/Samples/XR Plugin Management/.../Editor/*` — editor helpers and sample settings for the XR Plugin Management sample.

---

## How to request edits

If you want any of these explanations expanded into more detail (for example, showing method-by-method breakdowns, public fields and their Inspector use, or where the script is attached in scenes), tell me which script(s) you want deeper documentation for and I will add that to this file or produce separate per-script docs.

If you'd like, I can also generate a per-scene map that shows exactly which GameObjects reference which script (scene → GameObject → MonoBehaviour), which helps ensure you only change scripts that are actually used by each scene.

---

_Last updated: 2025-11-01_
