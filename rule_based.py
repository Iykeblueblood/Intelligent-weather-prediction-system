def forward_chaining(facts):
    """
    A simple forward-chaining inference engine for weather prediction.

    Args:
        facts (dict): A dictionary of weather data (temperature, humidity, etc.).

    Returns:
        list: A list of derived conclusions about the weather.
    """
    rules = get_weather_rules()
    conclusions = []
    
    for rule in rules:
        conditions_met = True
        for condition in rule['if']:
            # Check if the fact exists and the condition is met
            if condition[0] not in facts or not condition[1](facts[condition[0]]):
                conditions_met = False
                break
        
        if conditions_met:
            conclusions.append(rule['then'])
            
    return conclusions

def get_weather_rules():
    """
    Defines 20 rules for the weather expert system.
    Each rule is a dictionary with 'if' (conditions) and 'then' (conclusion).
    """
    rules = [
        # Temperature-based rules
        {'if': [('temp', lambda x: x > 35)], 'then': 'Extremely Hot'},
        {'if': [('temp', lambda x: 30 <= x <= 35)], 'then': 'Very Hot'},
        {'if': [('temp', lambda x: 10 <= x <= 20), ('clouds', lambda x: x < 20)], 'then': 'Pleasant and Sunny'},
        {'if': [('temp', lambda x: x < 0)], 'then': 'Freezing Cold'},
        
        # Humidity and Rain rules
        {'if': [('humidity', lambda x: x > 85), ('temp', lambda x: x > 25)], 'then': 'High Chance of Thunderstorms'},
        {'if': [('humidity', lambda x: x > 80), ('wind_speed', lambda x: x < 10)], 'then': 'Fog or Mist Likely'},
        {'if': [('precipitation_prob', lambda x: x > 70)], 'then': 'Heavy Rain Expected'},
        {'if': [('precipitation_prob', lambda x: 40 <= x <= 70)], 'then': 'Light Rain or Drizzle'},
        
        # Wind-based rules
        {'if': [('wind_speed', lambda x: x > 50)], 'then': 'Strong Wind Warning'},
        {'if': [('wind_speed', lambda x: 25 <= x <= 50)], 'then': 'Windy Conditions'},
        
        # Cloud-based rules
        {'if': [('clouds', lambda x: x > 80)], 'then': 'Overcast Skies'},
        {'if': [('clouds', lambda x: x < 10)], 'then': 'Clear Skies'},
        
        # Combination rules
        {'if': [('temp', lambda x: x < 5), ('precipitation_prob', lambda x: x > 50)], 'then': 'Snowfall Likely'},
        {'if': [('wind_speed', lambda x: x > 30), ('precipitation_prob', lambda x: x > 50)], 'then': 'Stormy Weather'},
        {'if': [('clouds', lambda x: x > 60), ('temp', lambda x: x > 20)], 'then': 'Cloudy and Warm'},
        {'if': [('humidity', lambda x: x < 30), ('temp', lambda x: x > 25)], 'then': 'Dry and Hot Conditions'},
        {'if': [('visibility', lambda x: x < 1000)], 'then': 'Low Visibility'},
        
        # UV Index rules
        {'if': [('uv_index', lambda x: x > 8)], 'then': 'High UV Index: Use Sun Protection'},
        
        # Pressure rules
        {'if': [('pressure', lambda x: x < 1000)], 'then': 'Low Pressure System: Possible Storms'},
        {'if': [('pressure', lambda x: x > 1020)], 'then': 'High Pressure System: Fair Weather Expected'}
    ]
    return rules