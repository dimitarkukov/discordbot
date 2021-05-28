#todos
# - command to add messages
# - check author/role so only mods can delete
#testing commit to github


import discord #discord stuff
import requests #allow to make https requests to api
import json #api returns json
import random
import sqlite3


client = discord.Client()

#sqlite3 database stuff
conn = sqlite3.connect("mydb.db") #in the project root dir
cursor = conn.cursor()
#creating the table use only once otherwise error. maybe make a check statement
#cursor.execute("""CREATE TABLE encourage (
 #       enc_text text
  #      )""")

#cursor.execute("INSERT INTO encourage VALUES('this is an enc message2')")
#cursor.execute("SELECT * FROM encourage")
#print(cursor.fetchall()) #returns first found result from query

conn.commit()
#conn.close()

sad_words = ["sad", "unhappy"] #sad word list to trigger bot response
enc_words = ["cheer up","hang in there", "hang in there"] #list for the job to choose from

def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    #convert response to json
    json_data = json.loads(response.text)
    quote = json_data[0]['q']  + " -" + json_data[0]['a']
    return(quote)    
        
@client.event
async def on_ready():
    print("we have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    #do nothing if the message is a normal user generated message
    if message.author == client.user:
        return
    #just var for ease of use
    msg = message.content

        #get quote from website
    if message.content.startswith("$inspire"):
        quote = get_quote()
        await message.channel.send(quote)
        
        #bot sends encouragement when it sees a word from the sad_words list
    if any(word in msg for word in sad_words):
        query = cursor.execute("SELECT * FROM encourage ORDER BY RANDOM()")
        query_result = query.fetchone()
        #convert tuple returned from query to string 
        bot_answer = ''.join(query_result) 
        await message.channel.send(bot_answer)
        

        #just list encouragements
    if message.content.startswith("$list"):
        query = cursor.execute("SELECT rowid, enc_text FROM encourage")
        query_result = query.fetchall()
        #returs list of tuples
        bot_answer = str(query_result) 
        await message.channel.send(bot_answer)
        

        # delete encouragements
    if message.content.startswith("$del"):
        query = cursor.execute("SELECT rowid, enc_text FROM encourage")
        query_result = query.fetchall()
        #returs list of tuples
        bot_answer = str(query_result) 
        await message.channel.send(bot_answer)
        await message.channel.send("type ID of message you want to delete")
        message_id = await client.wait_for('message') # type is <class 'discord.message.Message'>
        message_id = message_id.content
        query = cursor.execute("DELETE FROM encourage WHERE ROWID=?", (message_id))
        conn.commit()
        
        await message.channel.send("succesfully deleted message with id: " + message_id)


#running the bot with its token
client.run("ODQzMTEzMDQ2MTU1MzI5NTY3.YJ_INg.UZnO73lKiYW7YZX8T3C1-d2SRTw")