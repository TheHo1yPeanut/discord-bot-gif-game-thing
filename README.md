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
  <ul>!GIFgame command</ul>
 </p>
</ul>
