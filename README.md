# custom-hitster

I liked the game Hitster (https://hitstergame.com/en-us/, https://hitstergame.com/de-de/)
but I was not fully satisfied with their music selection, so I wanted to create my own.

This code creates a pdf file, ready to print with alternating spotify codes on one page and the corresponding songs on the second one.

Ready to be printed in an A4 sheet (could be ajusted to any format with the page_width and page_height in pixels variable). To scan the songs you need the spotify app, to recognize the spotify codes.

Here is an example of some spotify codes:

![Alt text](images/front.png?raw=true "Front")

Here is an example of the back of some cards:

![Alt text](images/back.png?raw=true "Back")

I put a lot of efford in the making of the playlist: https://open.spotify.com/playlist/6AeFzelGKQQWNDP9ONzOa7
and it contains songs from 1954 - 2023. It is way more Classic Rock and Rock focused than the original one.
It also contains some german songs ( maybe i will add a option to filter them out)

When you replace the "pl" variable with your own playlist id you can print out any playlist you want.

To use this you need a spotify developer account that is easy accessable for everyone. You just have to register you normal account.
This generates you 
client_id = 'XXXX'
client_secret = 'XXXX'

I will update this with a tutorial later on.

Feel free to write suggestions. I will pack this in the future in an executable.
