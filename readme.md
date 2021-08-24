# ASCII-GAME-ENGINE

Long ago during a boring meeting I started doodling in Microsoft Notepad. I used the basic ASCII and ASNI characters to draw funny characters and backgrounds...and before I knew it I had the idea for a game. A game rendered entirely with text. I didn't want this game to be a text-adventure like Zork or have the abstract ascii-graphics from games like Nethack or Dwarf Fortress. I wanted ACTUAL graphics inspired by 2D pixel side scrollers.


![](ascii-quest-joke.gif)


That when I started this project! I needed a game engine complete with Textures, Sprites, Animations, Layers, Input Control, etc. capable of rendering everything as text. Currently, this game engine is a work-in-progress! I've been having great fun implementing new features and learning game-engine and game-design programming!

## Texture
Textures in this game engine are literally TEXT-ures. They're literally `.txt.` files containing the ASCII art. For examples see the `/sprites` folder.

## Animation
An animation is a sequence of sprites that plays in order to show motion. A better name might be "Animated Texture" because as far as the other engine objects are concerned it *is* Texture.

## Sprite
Almost everything on-screen is a "Sprite". A sprite displays a Texture or Animation and has a position on screen. Most in-game objects (characters, platforms, props, etc.) inherit from Sprites.

## Screenbuffer
Screenbuffers are the canvas onto which individual sprites are drawn. The engine supports any number of screenbuffers to be layers on-top of each other. In my demos, I found four layers to be sufficient; foreground, background, object-layer and ui-layer.

## Controller
The controller implements basic input control that works with standard keyboard-interrupts. Works transparently on Windows and Posix.