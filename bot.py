import discord
import sqlite3

client = discord.Client()

conn = sqlite3.connect('database.sqlite3')

"""
conn.execute(''' CREATE TABLE IF NOT EXISTS prodigy_discs(
                NAME TEXT PRIMARY KEY NOT NULL,
                CLASS TEXT NOT NULL,
                SPEED DECIMAL NOT NULL,
                GLIDE DECIMAL NOT NULL,
                TURN DECIMAL NOT NULL,
                FADE DECIMAL NOT NULL
                                            ) ''')
"""

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('.disc'):
        await search_disc_by_name(message.content[6:],message)
        
    
    if message.content.startswith('.adddisc'):
        discinfo = message.content[8:].split()
        await add_disc(discinfo, message)                                 
                                            
async def add_disc(discinfo, message):
    conn.execute(''' INSERT INTO prodigy_discs(NAME,CLASS,SPEED,GLIDE,TURN,FADE)
                        VALUES(?,?,?,?,?,?)''',    (discinfo[0],
                                                    discinfo[1],
                                                    discinfo[2],
                                                    discinfo[3],
                                                    discinfo[4],
                                                    discinfo[5]))
    conn.commit()
    await message.channel.send("Added")
    
async def search_disc_by_name(name, message):
    name = name.lower()
    
    out_message = "```"
    cur = conn.cursor()
    try:
        
        cur.execute(f''' SELECT * FROM prodigy_discs WHERE NAME=?''',(name,))
        disc = cur.fetchall()[0]
        out_message += f'''Name: {disc[0]}\nClass: {disc[1]}\nSpeed: {disc[2]}\nGlide: {disc[3]}\nTurn: {disc[4]}\nFade: {disc[5]}'''
        out_message += "```"
    except:
        out_message = "Disc not found."
    await message.channel.send(out_message)

keyfile = open('key.txt')
key = keyfile.readline()         
client.run(key)