# HabitQuit

HabitQuit is a personal computer-vision project that uses a laptop camera to help reduce vaping by detecting hand-to-mouth behavior in real time. The goal is not surveillance or strict enforcement, but gentle behavioral awareness — surfacing moments that would otherwise happen unconsciously.

Below is an example of what the system currently detects.

<img width="1512" height="982" alt="Hand-to-mouth proximity alert" src="https://github.com/user-attachments/assets/b29bcd96-4c72-45ce-8ac1-ae2ef8e289ff" />

---

## What’s happening in the image

The app is running live on a webcam feed.

- The green dot marks the estimated center of the mouth, computed from facial landmarks.
- The circular radius represents a configurable proximity threshold.
- Hand landmarks are detected and tracked in real time.
- When any hand landmark enters the proximity zone around the mouth, the system raises an alert and increments a counter.

In the screenshot above, the system has detected a hand close enough to the mouth to be considered a potential vaping action and displays a warning accordingly.

---

## How it works (v0)

HabitQuit is built using:
- **OpenCV** for camera access, rendering, and real-time visualization
- **MediaPipe** for face mesh and hand landmark detection
- **Spotify Web API** for behavioral feedback

At a high level:
1. Each video frame is processed to detect facial landmarks.
2. A mouth center is estimated using upper and lower lip landmarks.
3. Hands are detected and tracked using MediaPipe’s hand model.
4. If a hand enters the mouth’s proximity zone, a “hand-to-mouth” event is recorded.
5. Once a configurable limit is reached, the app triggers Spotify playback on the active device.

The feedback mechanism is intentionally simple: when the limit is hit, a song the user strongly dislikes is played as a reminder to stop. This makes the habit interruption noticeable without being punitive.

Version 0 focuses on proving the full end-to-end pipeline:
- Real-time vision works
- Events are tracked correctly
- Spotify playback can be triggered reliably

---

## Current limitations

At the moment, the system only detects **hand proximity**, not **intent**.

This means:
- Bringing your hand near your mouth for unrelated reasons (scratching your face, resting your hand, etc.) can still be counted.
- The app does not yet distinguish between a relaxed hand and a hand holding a vape-like object.

This tradeoff was intentional for the initial version in order to validate the core detection and feedback loop.

---

## Future goals

Planned improvements include:

- **Vape-specific hand pose detection**  
  Detecting the characteristic hand formation used when holding a vape, so only true vaping gestures are counted.

- **Reduced false positives**  
  Ensuring that casual or accidental hand-to-mouth movements are ignored.

- **Better normalization**  
  Making proximity thresholds adaptive to face size and camera distance.

- **Long-term habit tracking**  
  Logging events over time to visualize progress and reduction trends.

---

## Why this project

HabitQuit started as a personal experiment in applying computer vision to something immediately useful. Beyond the technical aspects, it has genuinely helped reduce unconscious vaping behavior by making those moments visible in real time. As usage has decreased, the system has needed to intervene less — which is the intended outcome.

---
