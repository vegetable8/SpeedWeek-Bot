from discord.ext import commands

from .api import LeagueAPI
from db import DB

class LeagueCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = DB(1, 10)
        self.league_api = LeagueAPI()

    @commands.command()
    async def createleague(self, ctx):
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        await ctx.send('Enter the name of the league.')
        league_name = await self.bot.wait_for('message', check=check)

        await ctx.send('Enter your Garage61 team ID.\n\n*Hint: Open Garage61, open your Garage61 team and copy the URL. The team ID is the last part of the URL.*')

        msg = await self.bot.wait_for('message', check=check)
        team_id = msg.content

        lap_check_data = await self.league_api.search_for_team(team_id)
        
        if not any(team['slug'] == team_id for team in lap_check_data['teams']): #check to see if team exists within teams array
            await ctx.send('Invalid team ID.')
            return
        
        conn = self.db.get_conn()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO leagues (name, g61_team_id, first_day_of_week) values (%s, %s, %s)', (league_name.content, team_id, 1))
        conn.commit()
        self.db.release_conn(conn)

        await ctx.send(f'Creating league {league_name.content}... {team_id}')

    @commands.command()
    async def viewleagues(self, ctx):
        conn = self.db.get_conn()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM leagues')
        leagues = cursor.fetchall()
        self.db.release_conn(conn)
        print(leagues)
        msg = 'League: {0}, Team ID: {1}, League ID: {2}\n'
        
        for league in leagues:
            await ctx.send(msg.format(league[1], league[2], league[0]))

        
        await ctx.send('Viewing leagues...')

    @commands.command()
    async def joinleague(self, ctx):
        pass

    @commands.command()
    async def editleague(self, ctx, league_id):
        await ctx.send(f'Editing league {league_id}...')

    @commands.command()
    async def deleteleague(self, ctx, league_id):
        await ctx.send(f'Deleting league {league_id}...')