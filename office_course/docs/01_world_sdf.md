# Lesson 01 — Worlds, links, visuals, and collisions

A Gazebo **world** contains physics, gravity, lighting and models. **Models** contain links; **visual** geometry controls what you see while **collision** geometry determines physical contacts. A **pose** consists of x, y, z, roll, pitch, yaw (metres and radians). Static desks and walls do not move.

```bash
python3 office_course/scripts/generate_office_world.py
bash office_course/scripts/start_office_only.sh
```

Try selecting north_wall and the desks in Gazebo's Entity Tree. Change `room.width_m` in `config/office_example.json`, regenerate, and relaunch.

Why are wall collision heights 2.8 m even when their visible heights are only 1.35 m? Explain the camera cutaway and the physical implications.

**Log:** prediction, modified JSON value, observed difference, and screenshot.
