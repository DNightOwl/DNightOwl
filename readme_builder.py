import codingame
import pathlib
import re

root = pathlib.Path(__file__).parent.resolve()

# get a codingamer from their pseudo or public handle

def replace_readme(content, marker, chunk, inline=False):
    r = re.compile(
        r'<!\-\- {} starts \-\->.*<!\-\- {} ends \-\->'.format(marker, marker),
        re.DOTALL,
    )
    if not inline:
        chunk = '\n{}\n'.format(chunk)
    chunk = '<!-- {} starts -->{}<!-- {} ends -->'.format(marker, chunk, marker)
    return r.sub(chunk, content)

def fetch_codingame_stats():
    client = codingame.Client()
    codingamer = client.get_codingamer("DNightOwl")
    level = codingamer.level
    rank = codingamer.rank
    clash_of_code_rank = codingamer.get_clash_of_code_rank()
    #test = '<hr><br>'
    #test += 'Level: {}</br>Rank: {}\n'.format(level,rank)   
    svg = f'''
    <svg xmlns="http://www.w3.org/2000/svg" width="250" height="40">
        <rect width="250" height="40" fill="#222"/>
        <text x="10" y="25" font-size="14" fill="#fff">Codingame: Level {level}, Rank {rank}</text>
    </svg>
    '''
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "image/svg+xml",
            "Cache-Control": "no-cache"
        },
        "body": svg
    }
    #return test

# Execution the code
if __name__ == '__main__':
    readme_path = root/'README.md'
    readme = readme_path.open().read()
    stats = fetch_codingame_stats();
    # Update entries
    rewritten_stats = replace_readme(readme, 'Codingame', stats)
    readme_path.open('w').write(rewritten_stats)


