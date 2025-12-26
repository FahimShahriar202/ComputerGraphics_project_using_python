Cube Collector 

Overview

A 3D platformer game where the player controls a cube character that moves across floating platforms, collects colored cubes for points, and avoids obstacles to progress through 3 levels.


Player Mechanics (5 features)
Player Movement - W/S keys move forward/backward using sin/cos math identical to bullet direction calculation in our gun code from assignment 3(from course material). A/D keys strafe left/right on the same axis.

Player Jumping - Space key applies upward velocity. Gravity constant decrements vertical speed each frame, exactly like how bullets move with direction vectors.

Player Lives - Start with 3 lives. Decrement when hitting obstacles or falling below map. Game over when lives reach 0. 

Player Collision Detection - Circle-based collision: check distance between player position and obstacle/platform. If distance < player_radius + obstacle_radius, collision occurs. Same math as your bullet-enemy collision.

Camera Following - Third-person camera using gluLookAt() positioned behind player. Camera moves toward player position each frame for smooth following.




Level & World (5 features)
Platform System - Floating platforms drawn as scaled cubes at fixed positions. Store platform data (position, size) in arrays.

Level Loading - Three level layouts stored as separate data arrays. When level number changes, load corresponding array. Reset all object positions when new level starts.

Level Progression - When player collects all red cubes in current level, increment level counter and load next level's data. Display level number in HUD.

Obstacle Types - Three obstacle types: (1) Bouncing cylinders using sin(time) for vertical movement, (2) Spinning spheres using rotation, (3) Linear sliding cubes. All drawn using glutSolidCube/gluCylinder/gluSphere.
Dynamic Obstacles - Update obstacle positions each frame based on their movement pattern. Using same time-based animation as our enemy pulsing animation (global timer variable).




Collectibles (4 features)  
Collectible Cubes - Array of colored cubes with positions. Draw each using glutSolidCube() at stored coordinates. Three colors: red (score), blue (life), green (bonus).

Cube Collection - When player collides with cube, check color: red adds 10 points to score, blue adds 1 life, green adds temporary speed boost. Remove collected cube from array.

Cube Animation - Rotate cubes slowly using (time.time()) for time-based rotation. Apply glRotatef() before drawing each cube.

Cube Respawning - After collecting all cubes in a level, spawn new cube set for next level from data array.




Game Systems (6 features)
Score System - Integer variable tracking points. Red cubes add 10 points. Display in HUD using draw_text() at fixed screen position, identical to our lives/score display.

HUD Display - Draw text showing: current score, remaining lives, current level number. Using exact same draw_text() function and screen positions as our original game.

Game Over Screen - When lives <= 0, display "GAME OVER" and "Press R to Restart" text at center screen.
Level Complete Screen - When all cubes collected, display "LEVEL COMPLETE" .

Restart System - R key resets: lives to 3, score to 0, level to 1. Clear all object arrays and reload level 1 data. Same as your init_game() reset logic.

Main Menu - Display "3D CUBE COLLECTOR" and "Press ENTER to Start" at game start. Transition to level 1 when player presses space.
