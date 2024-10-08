﻿<h1>DelhitesDiscord Server Bot</h1>

<p>This repository contains the source code for the Discord bot used in the Delhites community server.</p>

<p>Join our community server: <a href="https://discord.com/invite/delhites">Delhites Discord Server</a></p>

<h2>Features</h2>

<ul>
  <li><strong>Fun Commands:</strong> Includes commands like dice rolling, coin flipping, quotes, and more.</li>
  <li><strong>Utility Commands:</strong> Provides utility commands like avatar display, server info, member count, etc.</li>
  <li><strong>Role Management:</strong> Commands to create, delete, and assign roles to users.</li>
  <li><strong>Miscellaneous:</strong> Additional commands for sending direct messages, fetching message time differences, and more.</li>
</ul>

<h2>Installation</h2>

<ol>
  <li>Clone the repository:
    <pre><code>git clone https://github.com/Nuu-maan/discord-bot.git
cd discord-bot
    </code></pre>
  </li>
  <li>Install dependencies:
    <pre><code>pip install -r requirements.txt
    </code></pre>
  </li>
  <li>Set up your bot token and prefix:
    <ul>
      <li>Rename <code>config_example.py</code> to <code>config.py</code>.</li>
      <li>Replace <code>your_bot_token_here</code> in <code>config.py</code> with your actual bot token.</li>
      <li>Set your preferred bot prefix in <code>config.py</code> (e.g., <code>PREFIX = '!'  # Replace with your prefix</code>).</li>
    </ul>
  </li>
  <li>Run the bot:
    <pre><code>python bot.py
    </code></pre>
  </li>
</ol>

<h2>Commands</h2>

<h3>Fun Commands</h3>
<ul>
  <li><code>!roll_dice [num_dice] [num_sides]</code>: Rolls a dice with the specified number of sides.</li>
  <li><code>!coinflip</code>: Flips a coin and returns heads or tails.</li>
  <li><code>!choose option1 option2 ...</code>: Chooses one option from the provided choices.</li>
  <li><code>!quote</code>: Sends a random quote.</li>
  <li><code>!rps choice</code>: Play rock-paper-scissors against the bot.</li>
</ul>

<h3>Utility Commands</h3>
<ul>
  <li><code>!avatar [user]</code>: Displays the avatar of the specified user.</li>
  <li><code>!banner [user]</code>: Shows the banner of the specified user in the guild.</li>
  <li><code>!servericon</code>: Displays the icon of the current server.</li>
  <li><code>!serverbanner</code>: Shows the banner of the current server.</li>
  <li><code>!ping</code>: Checks the bot's latency.</li>
  <li><code>!membercount</code>: Displays the total member count in the server.</li>
  <li><code>!inrole [role]</code>: Shows the number of members with the specified role.</li>
</ul>

<h3>Role Management</h3>
<ul>
  <li><code>!createrole role_name</code>: Creates a new role with the specified name.</li>
  <li><code>!deleterole role</code>: Deletes the specified role.</li>
  <li><code>!addrole member role</code>: Adds a role to the specified member.</li>
</ul>

<h3>Miscellaneous</h3>
<ul>
  <li><code>/timediff message_id1 message_id2</code>: Checks the time difference between two message IDs.</li>
  <li><code>/dm user message</code>: Sends a direct message to the mentioned user.</li>
  <li><code>/say message</code>: Makes the bot say the specified message.</li>
  <li><code>/embed message</code>: Makes the bot send an embedded message.</li>
  <li><code>/connect channel</code>: Connects to the specified voice channel.</li>
  <li><code>/gossip message</code>: Sends an anonymous gossip to a private channel.</li>
</ul>

<h2>Contributing</h2>

<p>Contributions are welcome! If you'd like to add more features, improve existing ones, or fix issues, feel free to fork the repository and submit a pull request.</p>

<h2>License</h2>

<p>This project is licensed under the MIT License - see the LICENSE file for details.</p>
