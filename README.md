# Game-of-Life-no-not-again-
a finger exercise to learn Python

An implementation of Conway Game of Life pure to learn Python classes, definitions, pygame
Core was borrowed from redevined/conway

Use:
 
 python GOL_exercise [configfile [patternfile]]
 
   - note if no first argument is given the program uses the default file data/config.txt
   - if no second argument is given the program uses the patternfile as defined in the configfile
   
 Following input is possible:
 
 Space  = pause or run
 b      = set border to blue
 o      = set border to orange
 c      = clears the field
 l      = load patternfile
 s      = save patternfile ! note it will overwrite the original patternfile
 Escape = leave program

 if mouse if clicked inside the action window then a new cell will either be created or deleted depending if cell was life or not
 
 Author: Bruno Vermeulen
 Email: bruno_vermeulen2001yahoo.com
 
