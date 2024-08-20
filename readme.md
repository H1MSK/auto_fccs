# AutoFCCS

Automatically play First-Class Customer Service(FCCS) of a game.

## Usage

1. Start game and script
2. If position is calibrated, goto step 6
3. Point your cursor at the inner edge(or a little bit more inner) of the hit ring
4. Focus at the **script window** (to capture input)
5. Press `Ctrl+Shift+Alt+W` to calibrate position
6. If color is calibrated, goto step 12
7. Start game
8. Focus at the **script window** (to capture input)
9. When nothing is on the hit ring, press `Ctrl+Shift+Alt+E` to calibrate color
10. You can calibrate the position and color for multiple times to improve accuracy
11. Reset the game
12. Press `Ctrl+Shift+Alt+S` to start the runner process, it will wait till the game starts
13. Start the game
14. Focus at the **game window** (to send input to the game)
15. Wait for S+
16. If it is S+, press `Ctrl+Shift+Alt+S` in the script window to stop the runner process, and then press `Ctrl+Shift+Alt+Q` to quit the script, end this flow
17. If all the inputs are sent late, or all are early, press `Ctrl+Shift+Alt+S` in the script window to stop the runner process, move cursor with respect to the preformance, and go to step 4