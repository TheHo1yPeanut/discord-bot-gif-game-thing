# discord bot gif game thing
<h1>Commands</h1>
<ul>
 <li><i>!GIFgame</i> - initializes the game, 30s timeout timer</li>
 <li><i>!userINFO</i> - returns games played by user, games won by user and user's winrate</li>
</ul>
<hr>
<h1>Description</h1>
<p>When the command <i>!GIFgame</i> is called the bot sends a random gif into the channel where the command was initialized. The bot then asks the user who initialized the command for the name of the GIF. The next response by the user is recieved as the answer (no prefix needed). If <i>You win!</i> is not displayed after the user's answer that means that the user lost (or there was an out of bounds exception but that is rare). <i>!userINFO</i> command fetches the tagged user's games played and games won and then returns them in an embed with a winrate% calculated by simply doing (games won)/(games played).</p>
<hr>
<h1>Report</h1>
<h3>Please note: this entire repository is part of a school project, this README file aims to describe and explain the code behind the bot.</h3>
<ul>
 <li><h2>Dependencies</h2></li>
 <p><ul>
  <li>discord</li>
  <li>asyncio</li>
  <li>aiohttp</li>
  <li>pymongo</li>
  <li>BeatifulSoup</li>
  <li>requests</li>
 </ul><br>
<i>discord</i> is a library that allows for work with discord's bot systems. <i>asyncio</i> is used to manage asyncronous functions which are necessary when dealing with processes that cannot reliably be performed (such as api calls due to server or connection issues). It is used to allow for asyncronous code execution. <i>aiohttp</i> is a library built upon the <i>asyncio</i> library and it allows for asyncronous http request handling. <i>pymongo</i> is the python library for MongoDB services such as reading and writing to a MongoDB cluster. <i>BeatifulSoup</i> makes it possible to fetch and inspect html documents from websites. <i>requests</i> is a simple syncronous api library.
</p>
 <hr>
 <li><h2>Taskflow</h2></li>
 <p>
  <h3>!GIFgame command</h3>
 The command makes an API request to the following link "https://random-word-api.herokuapp.com/word" where it then awaits a .json response contaning a single random word (what database of words is used is unknown to me). This happens in the get_word() async function. After this happens the word is passed into getHTMLdocument() which snatches the HTML document from the following link f"https://tenor.com/search/{word}". This link refers to tenor.com which is the website from which the code gets it's GIFs. ../search is the path to the search page of tenor.com which then recieves the random word. The document is passed into BeutifulSoup() which turns it into a parsable document by the BeatifulSoup library. The first GIF link is found through the html structure (find() returns the first instance of the sought after HTML element, in this case it is -> figure -> a). The GIF link gets sent into the chat followed by "What is this GIF called?". This concludes the first stage og the command. The bot then immidietly starts watching the chat for messages and using the check() function it makes sure that the message is sent by the same user that initiated the command. This is done in order to prevent other users from "hijacking" the game from the original user. If the user does not send any further messages in the following 30 seconds the bot terminates the command and responds with "You took too long to respond. Please try again.". However if the user responds their response is used in the ..search/ path on tenor.com. A loop checks if the original randomly picked GIF is contained in the first 20 GIFs on the search page. If the GIF is found the winstatus variable is set to true and the bot sends "You win!" along with a userDataHandler() call with the second parameter set to True. The userDataHandler function simply checks for the existence of a given user in the MongoDB collection and if it does not exist it creates an empty object with three key-value pair ("user":id, "games": 0, "wins": 0). This is possible thanks to the discord user ids being unique, immutable and publicly accessible. The user id is passed through the first parameter and the winstatus of the game is passed through the second. The winstatus is used in order to correctly attribute a "win" to the user's object in the collection. If the GIF is not found in the first 20 a elements on the search page the bot sends "You lose ;(" along with a userDataHandler() call with the second parameter set to False. It can be the case that the search page does not contain 20 GIFs, if this happens the except IndexError kicks in and informs the user about the failed state of the command, the command is then terminated. This does not affect the user's winrate.
 </p>
 <p>
  <h3>!userINFO</h3>
 This command is far simpler than the former. It expects the user parameter in the form of a discord tag (@user), an if statement checks if the user argument is Null and if it is not the function continues (otherwise the bot sends "Please tag a user." and the function is terminated). Afterwards the next if statement checks for the existence of the user in the collection. If the user is nonexistant the bot sends "This user has not played before." and the function temrinates. If all checks are passed the function creates an embed with with three fields; how many games the user has played, how many wins the user has and what the winrate is (calculated through wins/games). Both of these values are fetched from the user's object in the collection.
 </p>
 <p>
  <h3>!drSwag</h3>
  This is a rather simple function that does nothing other than send a sigle predetermined GIF. This was used in order to test the ability of the bot to send gifs. I never removed the command, because i didn't feel like it. The GIF that gets sent is the following: "https://tenor.com/view/dr-house-dr-gregory-house-dr-gregory-gif-13514172004559334125". 
 </p>
 <hr>
 <li><h2>Vulnerabilities</h2></li>
 <p>The bot handles most exceptions well without crashes, however there are some things that can be improved on. Firstly the random word that is generated can simply not exist in the search on tenor.com. This leads to no response from the bot and can leave the user confused. Secondly the bot relies on two different websites to function, if any of these go offline or cease to function the bot practically becomes useless (apart from the !userINFO which has almost certani 100% uptime thanks to the databse being hosted by me personally).</p>
 <hr>
 <li><h2>Get it for yourself</h2></li>
 <p>Add the bot to your own server: https://discord.com/oauth2/authorize?client_id=874011077166374962&permissions=0&integration_type=0&scope=bot</p>
</ul>
