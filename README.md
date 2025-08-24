How This System Works
- This project uses a unique two-step AI process to create smart weather forecasts.

1. The Logical Analyst (Rule-Based System):
- First, a Rule-Based Expert System scans the raw weather data (temperature, wind, humidity, etc.). Using a knowledge base of over 20 meteorological rules, it draws simple, logical conclusions like "Overcast Skies," "Windy Conditions," or "High UV Index."

1. The Skilled Reporter (Generative AI):
- Next, these conclusions—along with the original data—are handed over to Google's Gemini AI. This AI acts as a weather reporter, weaving all the structured information into a single, easy-to-read narrative. It explains what the weather will actually feel like and gives helpful, context-aware advice.

This hybrid approach combines the logical precision of an expert system with the fluent communication of a large language model.


```mermaid
graph LR
    subgraph "1. Input & Data Fetching"
        User[User Enters City] --> UI[Streamlit UI] --> Data[Fetch Data via<br>OpenWeatherMap API] --> RawData{Raw Weather Data};
    end

    subgraph "2. Parallel AI Processing"
        RawData --> RuleEngine[Rule-Based System] --> Conclusions[Logical Conclusions];
        RawData --> AI_Module[Generative AI Module];
        Conclusions --> AI_Module;
    end
    
    subgraph "3. AI Generation & Final Output"
        AI_Module -- Calls API --> Gemini((Google Gemini API)) --> AIForecast[AI Narrative];
        RawData --> Display[Final Report Display];
        Conclusions --> Display;
        AIForecast --> Display;
    end
