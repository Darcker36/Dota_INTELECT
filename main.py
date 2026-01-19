import requests
import json
import time
import sys
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# --- CONFIG ---
RULES_FILE = 'dota_rules.json'

# --- LOCALIZATION (texts dictionary) ---
TEXTS = {
    'en': {
        'welcome': "\n=== Dota 2 Impact Analyzer v1.0 ===\n   Developed by Darcker",
        'choose_matches': "How many matches to analyze?",
        'options': "20 (~30 sec)\n50 (~1 min)\n100 (~3 min)",
        'enter_count': "Enter number (20, 50, 100): ",
        'enter_my_id': "Enter YOUR Steam ID: ",
        'enter_friend_id': "Enter FRIEND'S Steam ID: ",
        'searching': "\n📡 Searching for joint matches for ID {} & {}...",
        'found': "✅ Found {} joint matches.",
        'starting': "\n🚀 Starting analysis (this may take a while)...",
        'error_api': "❌ API Error: {}",
        'error_no_matches': "❌ No joint matches found (or profiles are private).",
        'done': "\n✅ Analysis complete!",
        'result_my': "Your Average Score: {:.1f}",
        'result_friend': "Friend's Score:     {:.1f}",
        'win_msg': "🏆 YOU are {:.1f}% more effective!",
        'loss_msg': "🥈 Friend is {:.1f}% more effective. Time to train!",
        'saved': "\n📊 Chart saved to 'result_battle.png'. Check it out!",
        'choose_matches': "How many matches to analyze?",
        'options': " 20  (~30 sec)\n 50  (~1 min)\n 100 (~3 min)",
        'enter_count': "Enter number (e.g. 20): ",
    },
    'ru': {
        'welcome': "\n=== Dota 2 Impact Analyzer v1.0 ===\n   Разработано Darcker",
        'choose_matches': "Сколько матчей анализировать?",
        'options': "20 (~30 сек)\n50 (~1 мин)\n100 (~3 мин)",
        'enter_count': "Введите число (20, 50, 100): ",
        'enter_my_id': "Введите ВАШ Steam ID: ",
        'enter_friend_id': "Введите Steam ID ДРУГА: ",
        'searching': "\n📡 Поиск совместных игр для ID {} и {}...",
        'found': "✅ Найдено {} совместных игр.",
        'starting': "\n🚀 Начинаю анализ (это займет время)...",
        'error_api': "❌ Ошибка API: {}",
        'error_no_matches': "❌ Совместных игр не найдено (или профили скрыты).",
        'done': "\n✅ Анализ завершен!",
        'result_my': "Ваш средний Score: {:.1f}",
        'result_friend': "Score друга:       {:.1f}",
        'win_msg': "🏆 ВЫ играете на {:.1f}% эффективнее!",
        'loss_msg': "🥈 Друг играет на {:.1f}% эффективнее. Пора тренироваться!",
        'saved': "\n📊 График сохранен в 'result_battle.png'. Открывай!",
        'choose_matches': "Сколько матчей анализировать?",
        'options': " 20  (~30 сек)\n 50  (~1 мин)\n 100 (~3 мин)",
        'enter_count': "Введите число (например, 20): ",
    }
}

# Global variable for language choice
CURRENT_LANG = 'en'

def t(key, *args):
    """Функция-переводчик. Берет текст из словаря и вставляет переменные."""
    text = TEXTS[CURRENT_LANG].get(key, key)
    if args:
        return text.format(*args)
    return text

def select_language():
    print("Select Language / Выберите язык:")
    print("1. English")
    print("2. Русский")
    while True:
        choice = input(">>> ")
        if choice == '1': return 'en'
        if choice == '2': return 'ru'

# --- Main functions ---

def load_rules():
    try:
        with open(RULES_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {RULES_FILE} not found.")
        sys.exit()

def get_valid_limit():
    print(t('choose_matches'))
    print(t('options'))
    
    while True:
        val = input(t('enter_count'))
        if val.isdigit():
            count = int(val)
            if 1 <= count <= 100: 
                return count
            else:
                print("Please enter a number between 1 and 100 / Введите число от 1 до 100")
        else:
            print("Digits only! / Только цифры!")

def get_input(prompt_key):
    while True:
        val = input(t(prompt_key))
        if val.isdigit():
            return int(val)
        print("Digits only! / Только цифры!")

def get_joint_matches(id1, id2, limit):
    print(t('searching', id1, id2))
    url = f"https://api.opendota.com/api/players/{id1}/matches?included_account_id={id2}&limit={limit}"
    try:
        r = requests.get(url)
        if r.status_code != 200:
            print(t('error_api', r.status_code))
            return []
        matches = r.json()
        print(t('found', len(matches)))
        return [m['match_id'] for m in matches]
    except Exception as e:
        print(f"Connection Error: {e}")
        return []

def calculate_score(player_stats, match_averages, role_weights):
    if not player_stats: return 0
    def safe_div(a, b): return a / max(1, b)

    gpm_r = safe_div(player_stats.get('gold_per_min', 0), match_averages['gpm'])
    xpm_r = safe_div(player_stats.get('xp_per_min', 0), match_averages['xpm'])
    dmg_r = safe_div(player_stats.get('hero_damage', 0), match_averages['dmg'])
    kills_r = safe_div(player_stats.get('kills', 0), match_averages['kills'])
    deaths_r = safe_div(player_stats.get('deaths', 0), match_averages['deaths'])
    assists_r = safe_div(player_stats.get('assists', 0), match_averages['assists'])
    lh_r = safe_div(player_stats.get('last_hits', 0), match_averages['last_hits'])

    score = (
        gpm_r * role_weights['gpm_ratio'] +
        xpm_r * role_weights['xpm_ratio'] +
        dmg_r * role_weights['dmg_ratio'] +
        kills_r * role_weights['kills'] +
        assists_r * role_weights['assists'] +
        lh_r * role_weights['last_hits'] - 
        (deaths_r * role_weights['deaths'])
    )
    return score

def main():
    global CURRENT_LANG
    CURRENT_LANG = select_language()
    print(t('welcome'))
    
    weights = load_rules()
    
    match_limit = get_valid_limit()
    
    my_id = get_input('enter_my_id')
    friend_id = get_input('enter_friend_id')
    
    match_ids = get_joint_matches(my_id, friend_id, match_limit)
    
    if not match_ids:
        print(t('error_no_matches'))
        input("Enter...")
        return

    results = []
    print(t('starting'))
    print("Progress: ", end="")

    for mid in match_ids:
        try:
            r = requests.get(f"https://api.opendota.com/api/matches/{mid}")
            if r.status_code != 200: continue
            data = r.json()
            
            if 'players' not in data: continue
            players = data['players']
            
            avg_stats = {
                'gpm': np.mean([p.get('gold_per_min', 0) for p in players]),
                'xpm': np.mean([p.get('xp_per_min', 0) for p in players]),
                'dmg': np.mean([p.get('hero_damage', 0) for p in players]),
                'kills': np.mean([p.get('kills', 0) for p in players]),
                'deaths': np.mean([p.get('deaths', 0) for p in players]),
                'assists': np.mean([p.get('assists', 0) for p in players]),
                'last_hits': np.mean([p.get('last_hits', 0) for p in players]),
            }

            p1 = next((p for p in players if p.get('account_id') == my_id), None)
            p2 = next((p for p in players if p.get('account_id') == friend_id), None)

            if p1 and p2:
                role1 = 'Core' if p1.get('last_hits', 0) > avg_stats['last_hits'] else 'Support'
                role2 = 'Core' if p2.get('last_hits', 0) > avg_stats['last_hits'] else 'Support'

                s1 = calculate_score(p1, avg_stats, weights[role1])
                s2 = calculate_score(p2, avg_stats, weights[role2])

                results.append({
                    'Score P1': s1, 'Score P2': s2,
                    'Win': 'Win' if p1.get('win') else 'Loss'
                })
                print("█", end="", flush=True)
            
            time.sleep(1.1)
            
        except Exception:
            continue

    print(t('done'))
    
    if not results: return

    df = pd.DataFrame(results)
    avg1 = df['Score P1'].mean()
    avg2 = df['Score P2'].mean()

    print("\n=== RESULTS ===")
    print(t('result_my', avg1))
    print(t('result_friend', avg2))
    
    diff = ((avg1 / avg2) - 1) * 100 if avg2 > 0 else 0
    if avg1 > avg2:
        print(t('win_msg', diff))
    else:
        print(t('loss_msg', abs(diff)))

    plt.figure(figsize=(10, 8))
    sns.set_style("whitegrid")
    sns.scatterplot(data=df, x='Score P1', y='Score P2', hue='Win', style='Win', s=200, palette={'Win':'green', 'Loss':'red'})
    
    mx = max(df['Score P1'].max(), df['Score P2'].max()) + 10
    mn = min(df['Score P1'].min(), df['Score P2'].min()) - 10
    plt.plot([mn, mx], [mn, mx], '--', color='grey', label='Equal Impact')
    
    plt.title('Dota 2: Impact Analysis', fontsize=16)
    plt.xlabel('Your Score')
    plt.ylabel("Friend's Score")
    plt.legend()
    plt.savefig('result_battle.png')
    print(t('saved'))
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()