"""Constants."""

PLAYER_ICONS = ("🔵", "🔴")
BUTTON_ARROW = "⬇️"

HEADER_CONTENT = """
<h1>Connect 4</h1>
<p>
    Click the button where to slide down your disc, the AI will automatically move after you did!
    {player0_name} plays with {player0_icon}, {player1_name} with {player1_icon}.<br>
    Its currently {turn}'s turn.
</p>
{over_message}
""".lstrip()

OVER_MESSAGE_CONTENT = """
<hr>
<p>
    <div style="color: orange; font-weight: bold; font-size: 1.5rem">{text}</div>
    <em>Re-run the code-cell to play again!</em>
</p>
""".lstrip()
