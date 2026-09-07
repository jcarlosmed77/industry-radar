import feedparser
import json
import os
from datetime import datetime

# Fuentes RSS públicas y gratuitas de la industria
FEEDS = [
    {"source": "AdExchanger", "tag": "AdTech & Medios", "url": "https://adexchanger.com/feed/"},
    {"source": "Digiday", "tag": "Estrategia Digital", "url": "https://digiday.com/feed/"},
    {"source": "TechCrunch AI", "tag": "Inteligencia Artificial", "url": "https://techcrunch.com/category/artificial-intelligence/feed/"}
]

def obtener_noticias():
    articulos = []
    
    for feed_info in FEEDS:
        try:
            feed = feedparser.parse(feed_info["url"])
            if feed.entries:
                entry = feed.entries[0]
                # Limpiar resumen básico
                resumen = entry.get("summary", entry.get("description", ""))
                # Limpieza rápida de etiquetas html si existieran
                if "<" in resumen and ">" in resumen:
                    import re
                    resumen = re.sub('<[^<]+?>', '', resumen)
                
                resumen_corto = (resumen[:220] + "...") if len(resumen) > 220 else resumen
                
                articulos.append({
                    "tag": feed_info["tag"],
                    "time": "Hoy",
                    "title": entry.title,
                    "summary": resumen_corto,
                    "link": entry.link,
                    "source": feed_info["source"]
                })
        except Exception as e:
            print(f"Error leyendo {feed_info['source']}: {e}")
            
    # Guardar en archivo radar.json
    datos_radar = {
        "updated_at": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "articles": articulos[:3]
    }
    
    with open("radar.json", "w", encoding="utf-8") as f:
        json.dump(datos_radar, f, ensure_ascii=False, indent=2)
        
    print("radar.json generado exitosamente con 3 noticias frescas.")

if __name__ == "__main__":
    obtener_noticias()
