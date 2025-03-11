import discord      
#acces la toate functiile de baza din modulul discord
from discord.ext import commands        
#acces la toate comenzile din modulul discord
import youtube_dl       
#pentru melodii
import os       
#pentru crearea, ascunderea cheilor, stergerea si accesarea fisierului audio pentru melodii
import openai       
#pentru integrarea API-ului si a functiilor din openai(sursa chatGPT)
import time     
#pentru creare intentionata a unui delay

from dotenv import load_dotenv
load_dotenv()
discord_token=os.getenv('DISCORD_TOKEN_BOT')
openai_key=os.getenv('OPEN_AI_KEY')
#pentru pastrarea cheilor in siguranta

client=commands.Bot(command_prefix='!', intents=discord.Intents.all())    
#prefixul comenzilor '!' si acces permis la toate intentiile

openai.api_key=str(openai_key)
#introducerea cheii de acces pentru API-ul de la chatGPT (openai)

@client.event       
#eveniment ce ne arata in terminal daca executia blocului de instructiuni a fost produsa cu succes si daca bot-ul functioneaza corespunzator
async def on_ready():
    print('Marcel este pregatit de actiune.')
    print('--------------------------------')


@client.command(pass_context=True)       
#comanda simpla ce afiseaza un simplu raspuns al bot-ului in chat pentru autor
async def hello(ctx):
    await ctx.send(f'Salut, {ctx.message.author}! Marcel e pe zona!')



@client.event       
#comanda ce trimite un mesaj pe chat-ul unui canal ales cand cineva a intrat in server
async def on_member_join(member):
    channel = member.guild.get_channel(1163446828746944574)
    await channel.send(f"Bine ai venit in cartierul nostru, {member}!")



@client.event      
#comanda ce trimite un mesaj pe chat-ul unui canal ales cand cineva paraseste server-ul
async def on_member_remove(member):
    channel = member.guild.get_channel(1163446828746944574)     #id canal general server Suferintasejoaca
    await channel.send(f"A plecat un tradator dintre noi, {member}!")



@client.command()      
#comanda ce face bot-ul sa intre/sa se mute in canalul audio din care face parte autorul comenzii
async def join(ctx):
    if ctx.author.voice:
    # daca autorul este prezent intr-un canal audio
        channel = ctx.author.voice.channel

        if ctx.voice_client:
        #daca bot-ul este deja intr-un canal audio       
            if ctx.voice_client.channel == channel:
            #daca bot-ul este in acelasi canal audio cu autorul comenzii     
                await ctx.send('Sunt deja aici, nu ma vezi?')
                return
            await ctx.voice_client.move_to(channel)
            #altfel bot-ul este mutat in alt canal audio in care este prezent autorul comenzii    
            await ctx.send(f'M-am suparat! M-am mutat in canalul {channel.name}.')
        else:
            await channel.connect()
            #daca bot-ul nu este prezent in niciun canal audio   
            await ctx.send(f'Am fost invocat! M-am conectat la canalul {channel.name}.')
    else:
        #daca autorul comenzii nu este in niciun canal audio
        await ctx.send('Nu esti in niciun canal, nebunule!')        



@client.command()       
#comanda ce face ca bot-ul sa iasa din orice canal audio este activ la momentul comenzii
async def leave(ctx):
    if ctx.voice_client:
    #daca bot-ul este prezent intr-un canal audio        
        await ctx.voice_client.disconnect()
        await ctx.send('La culcare, ingerasi!')
    else:
    #daca bot-ul nu este prezent intr-un canal audio
        await ctx.send('Cine cuteaza sa-l cheme pe stapanul stapanilor, pe creatorul intunericului?')       



@client.command()       
#comanda ce da play la o melodie, dupa url(descarca audio-ul intr-un fisier si este decodat cu fmmpeg pt play (nu merge pe yt, dar merge cu soundcloud))      
async def play(ctx, url : str):
    song_there=os.path.isfile("song.mp3")       
    #luam acest fisier pentru a descarca melodiile in locul acestuia (va purta mereu numele "song.mp3")
    try:
        if song_there:
            #daca deja este un alt fisier din urma(cu continutul audio anterior)
            os.remove("song.mp3")
            #il stergem              
    except PermissionError:
        await ctx.send("Asteapta lautarii sa-si termine piesa sau spune-le stop!")
        #daca nu avem posibilitatea de a sterge fisierul inseamna ca inca este folosit pentru redare     
        return

    if ctx.voice_client:
        #daca bot-ul este conectat la un canal audio        
        voice=discord.utils.get(client.voice_clients, guild=ctx.guild)      
        #luam aceasta variabila ce are acces la comenzile de vorbit ale bot-ului
        ydl_opts={
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',         
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        #facem acest dictionar pentru a indica decoder-ului(FFmpeg) ce preferinte avem in legatura cu calitatea clipului ce urmeaza a fi descarcat si citit de program
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            #descarcam clipul cu url-ul dat         
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, "song.mp3")
                #cautam in directorul proiectului iar daca gasim un fisier audio cu un titlu de clip oarecare il vom redenumi in "song.mp3"
        voice.play(discord.FFmpegPCMAudio("song.mp3"))
                #de aici incepe redarea clipului
    else:
        await ctx.send("Nu sunt in niciun canal!")
        #se va afisa asta daca bot-ul nu este prezent intr-un canal audio



@client.command()       
#pune pauza melodiei
async def pause(ctx):
    voice=discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        #daca vocea bot-ului este in functionare
        voice.pause()
        #va pune pauza si va astepta urmatoarea comanda
        await ctx.send("Ai pus pauza!")
    else:
        await ctx.send("Nu asculti nimic!")



@client.command()       
#continua melodia
async def resume(ctx):
    voice=discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        #daca melodia este pusa in pauza
        voice.resume()
        #piesa continua de unde a ramas
        await ctx.send("Continui petrecerea!")
    else:
        await ctx.send("N-ai pus pauza!")
        #altfel va afisa doar acest mesaj



@client.command()       
#pune stop melodiei(iese de tot din fisier)
async def stop(ctx):
    voice=discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()
    #opreste de tot melodia(nu se mai tine cont de locul in care s-a oprit la alte comenzi)




queue=[]        #lista vida (coada de melodii(url-uri))



@client.command()       
#afiseaza melodiile din coada de melodii
async def print_queue(ctx):
    if queue:
        #daca exista macar o piesa in lista
        print("Coada:")
        await ctx.send("Piese in asteptare:")
        for it in queue:
            print(it)
            #afiseaza fiecare piesa(dupa url)
            await ctx.send(it)
    else:
        #daca nu exista piese in lista
        print("Coada e goala!")
        await ctx.send("Coada e goala!")



@client.command()       
#sterge toate url-uri din coada
async def clear_queue(ctx):
    if queue:
        #daca exista macar o piesa in lista
        queue.clear()
        #se vor sterge toate existente
        print("Coada este acum goala!")
        await ctx.send("Coada este acum goala!")
    else:
        #daca nu exista macar o piesa in lista
        print("Coada este deja goala!")
        await ctx.send("Coada este deja goala!")



@client.command()       
#adauga o melodie in coada
async def add_queue(ctx,url : str):
    queue.append(url)
    #se adauga noul url in lista
    print("Piesa adaugata cu succes!")
    await ctx.send("Piesa adaugata cu succes!")



def check_queue(ctx):       
    #o functie ce se apeleaza recursiv cand se termina o melodie din coada(va fi automat apelata dupa comanda "!play_queue")
    if queue:
        
        song_there=os.path.isfile("song.mp3")
        if song_there:
            os.remove("song.mp3")


        if ctx.voice_client:
            voice=discord.utils.get(client.voice_clients, guild=ctx.guild)

            ydl_opts={
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }

            url=queue[0]
            queue.pop(0)
            #se preia url-ul de pe prima pozitie si se sterge ulterior

            print(f'played url:{url}')
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            for file in os.listdir("./"):
                if file.endswith(".mp3"):
                    os.rename(file, "song.mp3")
            voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda x=None :check_queue(ctx))
            #aceasta functie incepe redarea clipului iar la finalul actiunii va apela functia lambda creata in argumentul de mai sus
        else:
            return
    
    else:
        return



@client.command()       
#comanda ce da play melodiilor din coada(identica cu fct de de mai sus, deoarece apelul recursiv nu functioneaza pt functii asincrone(comenzi de bot))
async def play_queue(ctx):
   
    if queue:
        
        song_there=os.path.isfile("song.mp3")
        if song_there:
            os.remove("song.mp3")

        if ctx.voice_client:
            voice=discord.utils.get(client.voice_clients, guild=ctx.guild)

            ydl_opts={
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }

            url=queue[0]
            queue.pop(0)
            #se preia url-ul de pe prima pozitie si se sterge ulterior

            print(f'played url:{url}')
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            for file in os.listdir("./"):
                if file.endswith(".mp3"):
                    os.rename(file, "song.mp3")
            await ctx.send("Redare din coada!")
            voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda x=None :check_queue(ctx))
            #aceasta functie incepe redarea clipului iar la finalul actiunii va apela functia lambda creata in argumentul de mai sus
        else:
            await ctx.send("Nu sunt in niciun canal!")
            return
    
    else:
        await ctx.send("Coada este goala!")
        return



@client.command()       
#trece la melodia urmatoare din coada
async def skip(ctx):
    if queue:
        #daca exista o piesa disponibila in coada
        voice=discord.utils.get(client.voice_clients, guild=ctx.guild)
        voice.stop()
        #bot-ul va opri redarea fisierului
        time.sleep(1)
        #este nevoie de acest delay ca functia check_play sa aiba timpul necesar de a detecta ca fisierul "song.mp3" nu mai este in folosire si il va putea sterge ulterior
        await ctx.send("Se trece la urmatoarea piesa din coada!")
        #se apeleaza iarasi functia check_queue ce trece la urmatoarea piesa
        check_queue(ctx)
    else:
        #daca nu exista o piesa in coada
        await ctx.send("Coada este goala!")



@client.event       
#detecteaza in fiecare mesaj daca apare prefixul "!ask" si trimite raspunsul creat de openai la textul mesajului
async def on_message(message):
    if message.author == client.user:
        #opreste generarea raspunsului daca prefixul(apelul comenzii transmis) este trimis de bot
        return
  
    if message.content.startswith('!ask'):
        #daca continutul mesajului incepe cu "!ask"
        user_message = message.content[5:].strip()
        #se va crea un nou string cu continutul intrebarii adresate dupa prefixul "!ask"
        try:
            #se genereaza un raspuns dupa urmatoarele preferinte
            response = openai.Completion.create(
                engine="gpt-3.5-turbo-instruct",
                #alegerea bot-ului petnru raspuns
                prompt=user_message,
                #mesajul nostru este transmis catre API
                max_tokens=150,
                #numarul maxim de caractere generat in raspuns
                temperature=0.7,
                #cat de "aspru" poate fi raspunsul in legatura cu intrebarea
            )

            await message.channel.send(response['choices'][0]['text'])
            #va alege si trimite primul raspuns generat in chat
        except Exception as e:
            print(f"Eroare la raspuns: {e}")
            #se va afisa in terminal eroarea la raspunsul negenerat

        await client.process_commands(message)
            #va procesa urmatoarele comenzi apelate si va trece peste detectarea prefixului in cazul apelarii unei alte comenzi  
        return

    await client.process_commands(message) 




client.run(str(discord_token))
#initierea bot-ului cu ajutorul token-ului sau privat (mereu se trece la sfarsit de program)