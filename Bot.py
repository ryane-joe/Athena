import interactions
from interactions import slash_command, SlashContext
from interactions import *
import mysql.connector
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "ATHENS"
}
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()
bot = Client(intents= Intents.ALL)
def Intitialize():
    games = ['Minecraft', 'Fortnite', 'CODM', 'Valorant']  # Reorder the games
    for game in games:
        table_name = game
        create_table_sql = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INT AUTO_INCREMENT PRIMARY KEY,
            squad_name VARCHAR(255) NOT NULL,
            squad_leader_ign VARCHAR(255) NOT NULL,
            squad_leader_discord_username VARCHAR(255) NOT NULL,
            squad_member_1_ign VARCHAR(255) DEFAULT 'notadded',
            squad_member_1_discord_username VARCHAR(255) DEFAULT 'notadded',
            squad_member_2_ign VARCHAR(255) DEFAULT 'notadded',
            squad_member_2_discord_username VARCHAR(255) DEFAULT 'notadded',
            squad_member_3_ign VARCHAR(255) DEFAULT 'notadded',
            squad_member_3_discord_username VARCHAR(255) DEFAULT 'notadded',
            squad_member_4_ign VARCHAR(255) DEFAULT 'notadded',
            squad_member_4_discord_username VARCHAR(255) DEFAULT 'notadded'
        )
        """


        cursor.execute(create_table_sql)
        print(f"Table '{table_name}' created successfully with 4 squad members, IGN, and discord_username.")

def is_squad_exists(game, squad_name, squad_leader_ign, squad_leader_discord):

    # Define the SQL statement to check if the squad already exists
    check_squad_sql = f"""
    SELECT COUNT(*) FROM {game}
    WHERE squad_name = %s
    OR squad_leader_ign = %s
    OR squad_leader_discord_username = %s
    """

    values = (squad_name, squad_leader_ign, squad_leader_discord)

    cursor.execute(check_squad_sql, values)
    result = cursor.fetchone()[0]
    return result > 0

#TODO:
#create guild
#database
#sqd checking
@slash_command(
    name="makesquad",
    description="make your squad!",
    group_name="mksqd",
    group_description="sqd makers",
    sub_cmd_name="game",
    sub_cmd_description="choose game",
    scopes= [1138789385375059998]
)
@slash_option(
    name = 'game',
    description='Choose game: Fortnite, Valorant, CODM, Minecraft',
    required= True,
    opt_type= OptionType.STRING 
)
@slash_option(
    name= 'squadsname',
    description='Name your squad',
    required= True,
    opt_type= OptionType.STRING,
)
@slash_option(
    name = 'squadleaderdiscord',
    description= 'enter squad leader discord ID',
    required= True,
    opt_type= OptionType.STRING # Use STRING type for discord username
)
@slash_option(
    name ='squadleaderign',
    description='Enter squad leaders IGN',
    required= True,
    opt_type= OptionType.STRING 
)
async def makesqd(ctx: SlashContext, game: str, squadsname: str, squadleaderdiscord: str, squadleaderign: str):
    if game.lower() in ['fortnite', 'valorant', 'minecraft', 'codm']:
        if not is_squad_exists(game, squadsname, squadleaderign, squadleaderdiscord):
            # Use %s as placeholders for values in the SQL query
            cursor.execute(
                f"INSERT INTO {game} (squad_name, squad_leader_ign, squad_leader_discord_username) VALUES (%s, %s, %s)",
                (squadsname, squadleaderign, squadleaderdiscord)
            )
            conn.commit()
            await ctx.send('Squad created successfully! To add squad members, use /addmembers. Only the squad leader can add new members!')
        else:
            await ctx.send('This squad leader or name is already registered!')
    else:
        await ctx.send('Invalid game selection. Choose from Fortnite, Valorant, CODM, Minecraft.')
Intitialize()
bot.start("")
