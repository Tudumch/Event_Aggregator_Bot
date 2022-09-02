discord_bot_token_filePath = "discord_token"

urls_for_parsing = ["http://www.klin-park.ru/afisha/"] 
# какая-то проблема при парсиге https://www.klincity.ru/events/

def readTokenFromFile(filePath):
    """Bot-tokens should be saved in external file for security reasons, 
    not in code."""

    with open(filePath, "r") as file:
        return file.read().rstrip()
        breakpoint()

token_discord = readTokenFromFile(discord_bot_token_filePath)
