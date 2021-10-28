Humanizer project brief -

The aim of this project is to take real human midi input and use the 'errors' in timing (groove) to generate a dynamic midi groove.
The dynamic MIDI groove should capture the push and pull of the real human input and should be constant moving in and out of sync like a real human player.
Using the term 'dynamic' groove is meant to convey that each midi track which is recieving input from the humanizer has a groove which is independant from the other tracks but is influenced by them, similar to the way a group of musicians play.

Steps

Prototype Program
1. Process quantised MIDI to create a groove
2. Read in a groove from a human player
	-Communicate when human is playing
	-Record message timings
	-Calculate timing 'errors' against a grid (32nd notes?)
	-Create augmented grid   
3. Apply augmented grid to incoming messages
	-Identify a quantised message with its augmented equivalent
	-Send the message with the altered timing

