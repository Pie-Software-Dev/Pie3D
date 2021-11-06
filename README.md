# Pie3D

A 3D engine made with Panda3D and Pygame

Hi! Thanks for checking out Pie3D!

## Quickstart

Download the git repo and copy the `/pie3D` folder to your new project directory. Then, create a config file called `config.json`. Now, let's add some data about the game.

```json
{
    "gameSettings": {
        "title": "My New Pie3D game!",
        "level1": "levels/level.egg"
    }
}
```

This defines your game title (In this case, `My New Pie3D game!`) and your base level (Can be exported using blender with [Chicken for Blender](http://chicken-export.sourceforge.net/)).

Now, let's add some player settings. Add this to your config file.

```json
"playerSettings": {
    "walkSpeed": 50,
    "PlayerHeight": 0.9
}
```

This sets your player's stats. These are pretty self-explanetory values, so I'm not gonna go in-depth here.

Just a bit more...

```json
"screenSettings":{
    "tooltip": "Welcome to my pie3D demo!"
}
```

This will display a tooltip in the top left corner of the screen with the text you define.

Now, it's just a matter of making a new python program and putting this code in it:

```python
from pie3d.pie3dmenuutil import launchMenu

launchMenu()
```

Now, run your python file. You just made a basic game with Pie3D