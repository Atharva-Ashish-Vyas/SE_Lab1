# Prompts used (Lab 4: Dig Dug Repair Lab)

Chat history link: PASTE SHARED CHAT LINK HERE

## Task prompts

**1. Fix enemy pathfinding (commit: "Task 1: fix BFS in bfs_path (pop -> popleft)")**
> Here is my game.py. Enemies reach the player through long winding tunnels instead of the shortest path. Find the bug in bfs_path and explain why it behaves like DFS. Give me only the corrected lines.

**2. dirt_color(row) (commit: "Task 2: implement dirt_color with distinct row bands")**
> Implement dirt_color(row) in my game.py to return a distinct color per row band (4 bands across rows 1-13) instead of a smooth gradient. Return None for any row outside the bands. Don't change anything else.

**3. on_enemy_popped (commit: "Task 3: implement on_enemy_popped particle burst")**
> Implement on_enemy_popped(enemy, score) as a particle burst at enemy.cell. The function is called from pump() and its return value is ignored, so use a module-level PARTICLES list and show me the minimal edits needed in Game.update and Game.draw to move and render them.

**4. enemy_speed_multiplier (commit: "Task 4: implement enemy_speed_multiplier (faster per level)")**
> Implement enemy_speed_multiplier(level) so enemies get gradually faster each level. It's used as a divisor on the step delay, so a higher value means faster movement. Return 1 + 0.1 * level.

## Follow-up requests in the same chat
- "do everything for me" (all changes applied, tested, packaged as patches)
- "now tell me step by step what to do on my github"
- "create all these" (PDF report, prompts, submission checklist)
